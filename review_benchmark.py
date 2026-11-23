"""Write a reproducible qualitative shortlist using held-out predictions."""
import csv
import json
from pathlib import Path

from dataset import read_jsonl


def main():
    root = Path("results/benchmark")
    qa_root = Path("results/benchmark_qa")
    gold = {r["qid"]: r for r in read_jsonl(Path("benchmark/questions.jsonl"))}
    evidence = {r["passage_id"]: r for r in read_jsonl(Path("benchmark/passages.jsonl"))}
    pred_path = qa_root / "predictions.json"
    predictions = json.loads(pred_path.read_text()) if pred_path.exists() else {}
    with (root / "cases.csv").open(encoding="utf-8", newline="") as stream:
        cases = list(csv.DictReader(stream))
    selected = set()
    lines = ["# Review of 15 difficult benchmark queries", "",
             "Five held-out cases per language, with distinct base intents. Cases are selected for retrieval misses, false refusals and missing information.", ""]
    for lang in ("english", "hindi", "hinglish"):
        lines += [f"## {lang.title()}", ""]
        pools = [
            [r for r in cases if r["gold"] and r["gold_evidence_found"] == "False"],
            [r for r in cases if r["gold"] and r["gold_evidence_found"] == "True" and r["score_gate_refuses"] == "True"],
            [r for r in cases if not r["gold"] and r["score_gate_refuses"] == "False"],
        ]
        for turn in range(5):
            for shift in range(3):
                pool = pools[(turn + shift) % 3]
                row = next((r for r in pool if r["language"] == lang and gold[r["qid"]]["base_id"] not in selected), None)
                if row:
                    break
            qid = row["qid"]
            selected.add(gold[qid]["base_id"])
            top = row["top_passages"].split()[0]
            label = row["gold"]
            if not label:
                diagnosis = "The score gate accepted a topical match whose passage does not contain the requested detail."
            elif row["gold_evidence_found"] == "False":
                diagnosis = "The expected passage was absent from the top five. A generator limited to those passages cannot cite it."
            else:
                diagnosis = "The expected passage was retrieved, but the validation-tuned threshold rejected the question before generation."
            lines += [f"### {qid}", "", row["question"], "",
                      f"- Expected answer: {gold[qid]['gold_answer'] or 'UNANSWERABLE'}.",
                      f"- Expected evidence: {label or 'none'}. Top result: {top}, {evidence[top]['section']}.",
                      f"- Observation: {diagnosis}"]
            if qid in predictions:
                p = predictions[qid]
                for field in ("direct","rag"):
                    lines.append(f"- {field.upper()} output: {p[field].replace(chr(10), ' ')}")
            lines.append("")
    (root / "qualitative_review.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
