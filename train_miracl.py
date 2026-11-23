"""Adapt E5 on public MIRACL training triples, independently of Bennett."""
import argparse
import json
from pathlib import Path

from encoder import E5Encoder


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-language", type=int, default=128)
    parser.add_argument("--output", type=Path, default=Path("checkpoints/miracl-e5"))
    parser.add_argument("--parquet", action="append", required=True,
                        metavar="LANG=PATH", help="Official MIRACL training parquet, one flag per language")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.per_language < 1:
        parser.error("--per-language must be positive.")
    import random

    import torch
    from datasets import load_dataset

    torch.manual_seed(args.seed)
    encoder = E5Encoder("intfloat/multilingual-e5-small")
    encoder.model.train()
    encoder.model.requires_grad_(False)
    top = encoder.model.encoder.layer[-1]
    top.requires_grad_(True)
    optimizer = torch.optim.AdamW(top.parameters(), lr=2e-5)
    triples = []
    counts = {}
    for item in args.parquet:
        language, path = item.split("=", 1)
        count = 0
        rows = load_dataset("parquet", data_files=path, split="train", streaming=True)
        for row in rows.shuffle(seed=args.seed, buffer_size=256):
            positive, negative = row["positive_passages"], row["negative_passages"]
            if not positive or not negative:
                continue
            triples.append((row["query"], positive[0]["text"], negative[0]["text"]))
            count += 1
            if count == args.per_language:
                break
        if not count:
            raise ValueError(f"No MIRACL training triples available for {language}.")
        counts[language] = count
    random.Random(args.seed).shuffle(triples)

    def embeddings(texts):
        inputs = encoder.tokenizer(texts, padding=True, truncation=True,
                                   max_length=192, return_tensors="pt").to(encoder.device)
        hidden = encoder.model(**inputs).last_hidden_state
        mask = inputs.attention_mask.unsqueeze(-1)
        return torch.nn.functional.normalize((hidden * mask).sum(1) / mask.sum(1), dim=1)

    losses = []
    for offset in range(0, len(triples), 4):
        q, p, n = zip(*triples[offset:offset+4])
        optimizer.zero_grad()
        queries = embeddings(["query: " + text for text in q])
        passages = embeddings(["passage: " + text for text in (*p, *n)])
        similarities = queries @ passages.T / 0.05
        loss = torch.nn.functional.cross_entropy(
            similarities, torch.arange(len(q), device=encoder.device))
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    args.output.mkdir(parents=True, exist_ok=True)
    encoder.model.save_pretrained(args.output)
    encoder.tokenizer.save_pretrained(args.output)
    (args.output / "training.json").write_text(json.dumps(dict(
        seed=args.seed, training_triples=counts, batch_size=4, learning_rate=2e-5,
        max_length=192, trainable_layers="final transformer block", step_losses=losses), indent=2))


if __name__ == "__main__":
    main()
