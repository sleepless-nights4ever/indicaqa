"""Build the 420-row source-bounded benchmark from the pilot and curated facts."""
import csv
import json
import random
import re
from pathlib import Path

from dataset import build, read_jsonl, stats, write_jsonl


def versions(en, hi, mix, index):
    forms = (
        (f"What is the {en[0].lower()}{en[1:]}?", f"{hi} क्या है?", f"{mix} kya hai?"),
        (f"Can you confirm the {en[0].lower()}{en[1:]}?", f"कृपया बताएँ: {hi} क्या है?", f"{mix} bata sakte ho?"),
        (f"Please specify the {en[0].lower()}{en[1:]}.", f"{hi} बताइए।", f"{mix} bata do."),
    )
    return dict(zip(("english", "hindi", "hinglish"), forms[index % len(forms)]))


def main():
    root = Path("benchmark")
    pilot = Path("data")
    passages = read_jsonl(pilot / "passages.jsonl")
    base = read_jsonl(pilot / "base_questions.jsonl")
    with (pilot / "sources.csv").open(encoding="utf-8", newline="") as stream:
        sources = {row["document_id"]: row["source_url"] for row in csv.DictReader(stream)}
    fold = []
    doc = section = ""

    def flush():
        for offset in range(0, len(fold), 3):
            group = fold[offset:offset+3]
            pid = f"{doc}_P{len(passages) + 1:03}"
            passages.append(dict(passage_id=pid, document_id=doc, section=section,
                                 source_url=sources[doc],
                                 text=". ".join(f"{en}: {a}" for a,en,_,_ in group) + "."))
            for a,en,hi,mix in group:
                category = ("date" if re.search(r"\b(?:January|June|July|August|September) \d{4}\b",a)
                            else "number" if re.match(r"^(?:[₹\d]|up to|at least)",a,re.I)
                            else "condition")
                idx = len(base) + 1
                base.append(dict(base_id=f"Q{idx:03}",answerable=True,gold_answer=a,
                    gold_passage_ids=[pid], question_type=category,
                    answer_type="short factual answer",questions=versions(en,hi,mix,idx)))
        fold.clear()

    for line in (root / "facts.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("@"):
            flush()
            doc, section = line[1:].split("|")
        else:
            fold.append(line.split("|"))
    flush()

    for line in (root / "missing.txt").read_text(encoding="utf-8").splitlines():
        idx = len(base) + 1
        en,hi,mix = line.split("|")
        base.append(dict(base_id=f"Q{idx:03}",answerable=False,gold_answer="",
            gold_passage_ids=[],question_type="condition",answer_type="none",
            questions=versions(en,hi,mix,idx),
            absence_check=f"Closed-corpus check: no benchmark passage gives the requested {en[0].lower()}{en[1:]}."))

    rows = build(passages, base, 42)
    assert len(rows) == 420
    assert sum(row["answerable"] for row in rows) == 300
    assert len({r["question"].casefold() for r in rows}) == len(rows)
    for name, records in (("passages",passages),("base_questions",base),("questions",rows)):
        write_jsonl(root / f"{name}.jsonl", records)
    (root / "statistics.json").write_text(json.dumps(stats(passages, rows), indent=2) + "\n")
    with (root / "independent_annotation.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["qid","language","question","annotator_answerable","annotator_answer","annotator_evidence"])
        random.Random(72).shuffle(rows)
        writer.writerows((r["qid"],r["language"],r["question"],"","","") for r in rows)


if __name__ == "__main__":
    main()
