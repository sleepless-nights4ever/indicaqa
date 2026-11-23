"""Turn cleaned, headed UTF-8 source files into a passage JSONL corpus."""
import argparse
import csv
import re
import unicodedata
from pathlib import Path

from dataset import write_jsonl


def chunks(body, target=150, maximum=200):
    paragraphs = [re.sub(r"(?<!\n)\n(?!\n)", " ", p).strip()
                  for p in re.split(r"\n\s*\n", body) if p.strip()]
    current = []
    size = 0
    for paragraph in paragraphs:
        if len(paragraph.split()) > maximum:
            units = re.split(r"(?<=[.!?।])\s+", paragraph)
        else:
            units = [paragraph]
        for unit in units:
            words = len(unit.split())
            if current and size + words > maximum:
                yield "\n\n".join(current)
                current, size = [], 0
            current.append(unit)
            size += words
            if size >= target:
                yield "\n\n".join(current)
                current, size = [], 0
    if current:
        yield "\n\n".join(current)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("sources", type=Path)
    p.add_argument("texts", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    rows = []
    with args.sources.open(encoding="utf-8", newline="") as stream:
        for source in csv.DictReader(stream):
            did = source["document_id"]
            data = unicodedata.normalize("NFC", (args.texts / f"{did}.txt").read_text(encoding="utf-8"))
            number = 0
            sections = re.split(r"^## (.+)$", data, flags=re.M)
            for title, body in zip(["Introduction", *sections[1::2]], sections[::2]):
                for chunk in chunks(body):
                    number += 1
                    rows.append(dict(passage_id=f"{did}_P{number:03}", document_id=did,
                                     section=title, text=chunk, source_url=source["source_url"]))
    write_jsonl(args.output, rows)


if __name__ == "__main__":
    main()
