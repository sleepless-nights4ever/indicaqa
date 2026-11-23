"""Measure gold-evidence citation coverage for non-refused RAG answers."""
import argparse
import json
from pathlib import Path

from dataset import read_jsonl
from qa import UNANSWERABLE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--questions", type=Path, default=Path("data/questions.jsonl"))
    args = parser.parse_args()
    predictions = json.loads(args.predictions.read_text(encoding="utf-8"))
    rows = [r for r in read_jsonl(args.questions) if r["qid"] in predictions]
    result = {}
    for language in ("overall", "english", "hindi", "hinglish"):
        group = [r for r in rows if language in ("overall", r["language"])]
        answered = [r for r in group if predictions[r["qid"]]["rag"] != UNANSWERABLE["answer"]]
        complete = sum(bool(r["gold_passage_ids"]) and
                       set(r["gold_passage_ids"]) <= set(predictions[r["qid"]]["citations"])
                       for r in answered)
        result[language] = dict(responses=len(group), answered=len(answered),
                                complete_gold_citations=complete,
                                coverage_among_answered=complete / len(answered) if answered else None,
                                unsupported_questions_answered=sum(not r["answerable"] for r in answered))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
