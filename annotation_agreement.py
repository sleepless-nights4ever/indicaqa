"""Score independently filled answers and citations without imputing missing votes."""
import argparse
import csv
import json
from pathlib import Path

from sklearn.metrics import cohen_kappa_score

from dataset import read_jsonl
from qa import tokenize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("annotations", type=Path)
    parser.add_argument("--gold", type=Path, default=Path("benchmark/questions.jsonl"))
    args = parser.parse_args()
    gold = {row["qid"]: row for row in read_jsonl(args.gold)}
    first, second, evidence, answers = [], [], [], []
    seen = set()
    with args.annotations.open(encoding="utf-8-sig", newline="") as stream:
        for review in csv.DictReader(stream):
            label = review["annotator_answerable"].strip().casefold()
            if not label:
                continue
            qid = review["qid"]
            if qid in seen or qid not in gold or label not in {"yes","no","true","false","1","0"}:
                raise ValueError(f"Invalid or duplicate reviewed row: {qid}")
            seen.add(qid)
            original = gold[qid]
            vote = label in {"yes","true","1"}
            first.append(original["answerable"])
            second.append(vote)
            if vote and original["answerable"]:
                ids = set(review["annotator_evidence"].replace(","," ").split())
                if ids:
                    evidence.append(ids == set(original["gold_passage_ids"]))
                if review["annotator_answer"].strip():
                    answers.append(tokenize(review["annotator_answer"]) == tokenize(original["gold_answer"]))
    result = {"reviewed": len(first), "total": len(gold), "joint_evidence_reviews": len(evidence),
              "joint_answer_reviews": len(answers)}
    if first:
        result["answerability_agreement"] = sum(a == b for a,b in zip(first,second)) / len(first)
        if len(set(first + second)) > 1:
            result["answerability_kappa"] = cohen_kappa_score(first, second)
    if evidence:
        result["exact_evidence_agreement"] = sum(evidence) / len(evidence)
    if answers:
        result["normalized_answer_exact_agreement"] = sum(answers) / len(answers)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
