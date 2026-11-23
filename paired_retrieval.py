"""Compute percentile intervals by resampling held-out answerable base intents."""
import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from dataset import read_jsonl
from encoder import E5Encoder
from qa import Retriever


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("benchmark"))
    parser.add_argument("--metrics", type=Path, default=Path("results/benchmark/metrics.json"))
    args = parser.parse_args()
    measurements = json.loads(args.metrics.read_text())
    alpha = measurements["alpha"]
    encoder = E5Encoder(measurements["encoder"])
    index = Retriever(read_jsonl(args.data / "passages.jsonl"), encoder)
    differences = defaultdict(list)
    for row in read_jsonl(args.data / "questions.jsonl"):
        if row["split"] != "test" or not row["answerable"]:
            continue
        gold = set(row["gold_passage_ids"])
        reciprocal_ranks = {}
        for method in ("hybrid", "bm25"):
            matches = index.rank(row["question"], method, 10, alpha)
            reciprocal_ranks[method] = next(
                (1 / i for i,p in enumerate(matches, 1) if p["passage_id"] in gold), 0)
        differences[row["base_id"]].append(reciprocal_ranks["hybrid"] - reciprocal_ranks["bm25"])
    group_means = np.array([np.mean(values) for values in differences.values()])
    rng = np.random.default_rng(42)
    bootstrap = rng.choice(group_means, size=(2000, len(group_means)), replace=True).mean(axis=1)
    print(json.dumps({
        "comparison": "Hybrid minus BM25 MRR@10",
        "base_intents": len(group_means), "resamples": len(bootstrap),
        "mean_difference": float(group_means.mean()),
        "paired_percentile_ci_95": np.quantile(bootstrap, [.025,.975]).tolist(),
    }, indent=2))


if __name__ == "__main__":
    main()
