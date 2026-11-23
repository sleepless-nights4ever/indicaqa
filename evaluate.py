"""Tune on validation, then evaluate retrieval and optional generation on test."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from statistics import mean

from dataset import read_jsonl
from qa import Retriever, answer, evidence_prompt, tokenize


def retrieval(rows, rankings, k):
    per_question = []
    for row in rows:
        gold = set(row["gold_passage_ids"])
        if not gold:
            continue
        hits = rankings[row["qid"]][:k]
        matches = [p["passage_id"] in gold for p in hits]
        count = sum(matches)
        per_question.append((count / len(gold), count / k, bool(count),
                             next((1 / i for i, hit in enumerate(matches, 1) if hit), 0),
                             count == len(gold)))
    keys = ("recall", "precision", "hit_rate", "mrr", "complete_evidence")
    return {key: mean(values) for key, values in zip(keys, zip(*per_question))}


def classification(rows, predictions):
    counts = Counter((not row["answerable"], predictions[row["qid"]]) for row in rows)
    tp, fp, tn, fn = (counts[pair] for pair in ((True, True), (False, True),
                                              (False, False), (True, False)))
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    return dict(tp=tp, fp=fp, tn=tn, fn=fn, accuracy=(tp + tn) / len(rows),
                precision=precision, recall=recall,
                f1=2 * precision * recall / (precision + recall) if precision + recall else 0,
                balanced_accuracy=(recall + (tn / (tn + fp) if tn + fp else 0)) / 2)


def grade(predicted, gold):
    a, b = tokenize(predicted), tokenize(gold)
    overlap = sum((Counter(a) & Counter(b)).values())
    return int(a == b), 2 * overlap / (len(a) + len(b)) if a or b else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--encoder", help="A multilingual E5 checkpoint")
    parser.add_argument("--strict-json", action="store_true", help="Reject fenced JSON in RAG output")
    parser.add_argument("--generator", help="Instruction-tuned causal LM with a chat template")
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--max-new-tokens", type=int, default=160)
    parser.add_argument("--batch-size", type=int, default=1)
    args = parser.parse_args()
    if args.batch_size < 1 or args.max_new_tokens < 1:
        parser.error("--batch-size and --max-new-tokens must be positive.")
    passages = read_jsonl(args.data / "passages.jsonl")
    rows = read_jsonl(args.data / "questions.jsonl")
    val = [r for r in rows if r["split"] == "validation"]
    test = [r for r in rows if r["split"] == "test"]
    if not val or not test or len({r["answerable"] for r in val}) != 2:
        parser.error("Validation needs both labels and the test set must be nonempty.")
    if {r["base_id"] for r in val} & {r["base_id"] for r in test}:
        parser.error("A base question occurs in both splits.")
    encoder = None
    if args.encoder:
        from encoder import E5Encoder
        encoder = E5Encoder(args.encoder)
    index = Retriever(passages, encoder)
    k = min(5, len(passages))

    if encoder:
        from functools import lru_cache

        encode = encoder.encode

        @lru_cache(maxsize=2 * len(rows))
        def cached_encode(texts, normalize_embeddings):
            return encode(list(texts), normalize_embeddings=normalize_embeddings)

        encoder.encode = lambda texts, normalize_embeddings=True: cached_encode(
            tuple(texts), normalize_embeddings)

    def rank(method, alpha=0.5):
        return {r["qid"]: index.rank(r["question"], method, 10, alpha) for r in rows}

    rankings = {name: rank(name) for name in ("tfidf", "bm25")}
    alpha = None
    if encoder:
        rankings["dense"] = rank("dense")
        candidates = [(a, rank("hybrid", a)) for a in (0.25, 0.5, 0.75)]
        alpha, rankings["hybrid"] = max(candidates, key=lambda pair: (
            retrieval(val, pair[1], k)["recall"], -abs(pair[0] - 0.5)))
    selected = "hybrid" if encoder else "bm25"
    confidence = rankings["dense"] if encoder else rankings[selected]
    scores = {qid: hits[0]["score"] for qid, hits in confidence.items()}
    val_scores = sorted({scores[r["qid"]] for r in val})
    cuts = [val_scores[0] - 1, *val_scores]
    threshold = max(cuts, key=lambda cut: classification(
        val, {q: s <= cut for q, s in scores.items()})["balanced_accuracy"])
    groups = {"overall": test}
    groups.update({language: [r for r in test if r["language"] == language]
                   for language in ("english", "hindi", "hinglish")})
    groups.update({f"type/{typ}": [r for r in test if r["question_type"] == typ]
                   for typ in sorted({r["question_type"] for r in test})})
    report = dict(encoder=args.encoder, generator=args.generator, strict_json=args.strict_json, k=k, alpha=alpha,
                  threshold=threshold, threshold_method="dense cosine" if encoder else "BM25",
                  validation=len(val), test=len(test), retrieval={}, score_gate={})
    for group, subset in groups.items():
        if not subset:
            continue
        report["retrieval"][group] = {
            name: {**retrieval(subset, ranks, k), "mrr_at_10": retrieval(subset,ranks,10).get("mrr")}
            for name, ranks in rankings.items()}
        report["score_gate"][group] = classification(subset, {q: s <= threshold for q, s in scores.items()})

    if args.generator:
        from transformers import pipeline
        generator = pipeline("text-generation", model=args.generator)

        generator.tokenizer.padding_side = "left"
        if generator.tokenizer.pad_token is None:
            generator.tokenizer.pad_token = generator.tokenizer.eos_token
        outputs = {}
        report["max_new_tokens"] = args.max_new_tokens
        args.output.mkdir(parents=True, exist_ok=True)
        for start in range(0, len(test), args.batch_size):
            batch = test[start:start + args.batch_size]
            prompts, owners = [], []
            for row in batch:
                qid, question = row["qid"], row["question"]
                prompts.append("Answer the question briefly. If you cannot answer it, return UNANSWERABLE.\n" + question)
                owners.append((qid, "direct", None))
                outputs[qid] = {"rag": "UNANSWERABLE", "citations": []}
                if scores[qid] > threshold:
                    hits = [{**p, "score": scores[qid]} for p in rankings[selected][qid][:k]]
                    prompts.append(evidence_prompt(question, hits))
                    owners.append((qid, "rag", (question, hits)))
            messages = [[{"role": "user", "content": prompt}] for prompt in prompts]
            predictions = generator(messages, batch_size=args.batch_size,
                                    max_new_tokens=args.max_new_tokens, do_sample=False,
                                    return_full_text=False)
            for (qid, kind, inputs), items in zip(owners, predictions, strict=True):
                raw = items[0]["generated_text"].strip()
                if kind == "direct":
                    outputs[qid]["direct"] = raw
                else:
                    result = answer(*inputs, lambda _: raw, threshold,
                                    allow_fences=not args.strict_json)
                    outputs[qid].update(rag=result["answer"], citations=result["citations"])
            (args.output / "progress.json").write_text(
                json.dumps({"completed": len(outputs), "total": len(test)}))
        report["qa"] = {}
        for group, subset in groups.items():
            if not subset:
                continue
            report["qa"][group] = {}
            for name in ("rag", "direct"):
                grades = [grade(outputs[r["qid"]][name], r["gold_answer"])
                          for r in subset if r["answerable"]]
                report["qa"][group][name] = dict(
                    exact_match=mean(g[0] for g in grades) if grades else None,
                    token_f1=mean(g[1] for g in grades) if grades else None,
                    answerability=classification(subset, {
                        qid: item[name].strip().upper() == "UNANSWERABLE"
                        for qid, item in outputs.items()}))
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "predictions.json").write_text(json.dumps(outputs, ensure_ascii=False, indent=2),
                                                       encoding="utf-8")

    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    with (args.output / "cases.csv").open("w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(["qid", "language", "question", "gold", "top_passages",
                         "gold_evidence_found", "score_gate_refuses"])
        for row in test:
            qid = row["qid"]
            ids = [p["passage_id"] for p in rankings[selected][qid][:k]]
            gold = row["gold_passage_ids"]
            writer.writerow([qid,row["language"],row["question"]," ".join(gold)," ".join(ids),
                             set(gold) <= set(ids) if gold else "",scores[qid] <= threshold])


if __name__ == "__main__":
    main()
