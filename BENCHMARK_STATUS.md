# CSET 346 expanded benchmark status

- 420 query records are grouped into 140 base intents (100 answerable and 40 unanswerable). Each has English, Hindi and Roman-script Hinglish variants.
- 84 validation rows and 336 test rows share no base intent across splits. The corpus contains 42 curated passages from three public Bennett sources.
- The original pilot remains under `data/`. The expanded benchmark and its sources are under `benchmark/`.
- Lexical, dense and hybrid scores, thresholds, language slices and per-query retrieval outcomes are under `results/benchmark/` and `results/benchmark_adapted/`. The adapted checkpoint used 16 Hindi MIRACL triples in the prior pilot and no Bennett questions.
- `results/benchmark/qualitative_review.md` gives 15 difficult held-out cases. Cite source URLs and academic years when interpreting historical notices. Unanswerable labels refer to absence in the included corpus.
- The 420-row set was assembled from curator-authored records and checked for schema, gold spans, source links and split integrity. Independent human labels are absent. The blank review sheet and agreement script are included.
- Source history can be imported locally from the Git bundle. Publication needs a GitHub repository and authenticated access.
- Many expanded queries share wording with the passage descriptions. Treat these numbers as controlled benchmark results, with limited evidence of performance on naturally phrased, unseen questions or a broader set of university documents.

The expanded hybrid system was also tested interactively on a 75% course-attendance question and a question about accessible parking omitted from the corpus. It returned the cited attendance figure and refused the missing parking detail. Both outputs are saved with retrieval diagnostics.

## Course deliverables

| Item | Location |
| --- | --- |
| Data collection and questions | `benchmark/sources.csv`, `benchmark/passages.jsonl`, and `benchmark/questions.jsonl` |
| Lexical, dense and hybrid retrieval | `results/benchmark/metrics.json` |
| English, Hindi and Hinglish comparison | Language sections of the same metrics file |
| Small MIRACL adaptation comparison | `results/benchmark_adapted/metrics.json` |
| Answerability gate | `score_gate` section of the benchmark metrics |
| Direct LLM versus RAG | `results/benchmark_qa/metrics.json`, `predictions.json`, and `citation_coverage.json` |
| Difficult-case analysis | `results/benchmark/qualitative_review.md` |
| Demonstration | `qa.py` and saved results in `results/benchmark/` |
| Paper and presentation | `deliverables/` |
