"""Inspect benchmark cases using their saved ranks and refusal decisions."""
import csv
from pathlib import Path

root = Path("results")
with (root / "cases.csv").open(encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream))
lines = ["# Pilot error analysis", "",
         "BM25 validation-tuned score gate. Expected evidence and refusal outcomes "
         "are evaluated against the frozen paraphrased corpus.", ""]
for row in rows:
    gold = row["gold"]
    ids = row["top_passages"].split()
    refused = row["score_gate_refuses"] == "True"
    if not gold:
        outcome = ("Correct refusal" if refused else
                   "Missed refusal: lexical overlap passed the gate despite missing evidence")
    elif row["gold_evidence_found"] == "False":
        outcome = "Retrieval miss: top five omit the gold passage"
        if refused:
            outcome += " and the system refused"
    elif refused:
        outcome = "False refusal: the gold passage was retrieved but the score was below the cut"
    else:
        rank = ids.index(gold) + 1
        outcome = f"Gold evidence at rank {rank}; score gate passed"
    if row["language"] == "hindi":
        observation = "Devanagari query against English evidence. Examine ties from zero overlap."
    elif row["language"] == "hinglish":
        observation = "Roman-script code mixing. Examine shared English words and spelling variants."
    else:
        observation = "English query. Examine year, programme, procedure, or award qualifiers."
    lines.extend([f"## {row['qid']}", row["question"], "",
                  f"{outcome}. {observation}",
                  f"Gold {gold or 'absent'}. Retrieved {' '.join(ids)}.", ""])
(root / "error_analysis.md").write_text("\n".join(lines), encoding="utf-8")
