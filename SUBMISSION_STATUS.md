# CSET 346 original pilot status

| Brief requirement | Evidence in this package |
| --- | --- |
| Lexical versus multilingual dense | Pilot held-out metrics for TF-IDF, BM25 and multilingual E5 |
| Language comparison | English monolingual, Hindi-to-English, and Hinglish-to-English slices |
| Lexical, dense and hybrid | Saved pilot comparison with validation-selected hybrid weight |
| Direct LLM versus RAG | 39-query strict-JSON pilot comparison and run logs under results/model |
| Unanswerable questions | 15 pilot records and score-gate confusion matrices |
| At least 15 difficult cases | 16 case-by-case pilot observations with actual ranks and gate decisions |
| Source code and instructions | Python source and README, ready to place in the team's GitHub repository |
| Paper and slides | Editable Word paper, PDF and PowerPoint |
| Dataset | 48 pilot records, source register, passages, and dataset statistics |
| Working demonstration | Command-line query with source metadata, optional model-generated answer and citations |

The expanded 420-row release is tracked in BENCHMARK_STATUS.md. The pilot's compact paraphrased passages and single-corpus absence checks do not establish that a missing detail is unavailable across Bennett University. Independent annotation is pending. No course submission or public repository was created.

The public-data adaptation used 16 Hindi MIRACL training triples. It produced the same held-out MRR@10 as the original model at the displayed precision. This small run does not establish the effect of larger English-plus-Hindi training.
