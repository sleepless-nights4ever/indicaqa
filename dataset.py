"""Build and validate parallel questions from manually reviewed base records."""
import argparse
import json
import random
from collections import Counter
from pathlib import Path
from statistics import mean

LANGUAGES = ("english", "hindi", "hinglish")
TYPES = {"number", "date", "condition", "procedure", "yes/no"}


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")


def build(passages, base_rows, seed):
    passage_ids = set()
    for row in passages:
        pid = row["passage_id"]
        if pid in passage_ids or not all(row[k].strip() for k in
                                         ("document_id", "section", "text")):
            raise ValueError(f"Invalid or duplicate passage: {pid}")
        passage_ids.add(pid)

    base_ids = set()
    for row in base_rows:
        bid = row["base_id"]
        questions = row["questions"]
        if bid in base_ids or set(questions) != set(LANGUAGES) or not all(
            question.strip() for question in questions.values()
        ):
            raise ValueError(f"Duplicate ID or missing language version: {bid}")
        base_ids.add(bid)
        if row["question_type"] not in TYPES or type(row["answerable"]) is not bool:
            raise ValueError(f"Invalid question type or answerability: {bid}")
        evidence = row["gold_passage_ids"]
        answer = row["gold_answer"].strip()
        if row["answerable"]:
            if not answer or not 1 <= len(evidence) <= 2 or len(set(evidence)) != len(evidence):
                raise ValueError(f"Answer and one or two distinct passages required: {bid}")
            if not set(evidence) <= passage_ids:
                raise ValueError(f"Unknown gold passage: {bid}")
        elif answer or evidence or not row.get("absence_check", "").strip():
            raise ValueError(f"Empty gold fields and documented absence check required: {bid}")

    rng = random.Random(seed)
    validation = set()
    for answerable in (True, False):
        ids = sorted(row["base_id"] for row in base_rows if row["answerable"] == answerable)
        rng.shuffle(ids)
        validation.update(ids[:round(len(ids) * 0.2)])

    rows = []
    for row in base_rows:
        bid = row["base_id"]
        for language in LANGUAGES:
            rows.append({
                "qid": f"{bid}_{language}", "base_id": bid, "language": language,
                "question": row["questions"][language], "answerable": row["answerable"],
                "gold_answer": row["gold_answer"], "gold_passage_ids": row["gold_passage_ids"],
                "question_type": row["question_type"], "answer_type": row.get("answer_type"),
                "split": "validation" if bid in validation else "test",
            })
    return rows


def stats(passages, rows):
    return {
        "documents": len({p["document_id"] for p in passages}),
        "passages": len(passages),
        "average_passage_words": mean(len(p["text"].split()) for p in passages),
        "question_types": Counter(r["question_type"] for r in rows),
        "splits": Counter(r["split"] for r in rows),
        "languages": {
            language: {
                "count": len(group),
                "answerable": sum(r["answerable"] for r in group),
                "unanswerable": sum(not r["answerable"] for r in group),
                "average_question_words": mean(len(r["question"].split()) for r in group),
            }
            for language in LANGUAGES
            if (group := [r for r in rows if r["language"] == language])
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("passages", type=Path)
    parser.add_argument("bases", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    passages, bases = read_jsonl(args.passages), read_jsonl(args.bases)
    if not passages or not bases:
        parser.error("Both inputs must contain data.")
    rows = build(passages, bases, args.seed)
    write_jsonl(args.output, rows)
    print(json.dumps(stats(passages, rows), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
