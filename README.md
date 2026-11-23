# IndicRAG-QA

University regulations and scholarship question answering in English, Hindi and Roman-script Hinglish.

This package contains the Bennett pilot corpus and benchmark, source code, reproducible experiments and submission materials. See SUBMISSION_STATUS.md for coverage and remaining work.

## Data files

- `sources.csv` records source provenance and redistribution status. Add one row per official public document.
- `passages.jsonl` takes one JSON object per line with `passage_id`, `document_id`, `section` and `text`. Preserve clause boundaries, table labels, units and footnotes. Example passage ID is `DOC03_P012`.
- `base_questions.jsonl` takes one object per base question. Include `base_id`, `questions` (an object keyed by `english`, `hindi` and `hinglish`), `answerable`, `gold_answer`, `gold_passage_ids`, `question_type` and `answer_type`. For unanswerable questions use an empty answer, an empty list of evidence IDs, a null answer type and an `absence_check` note describing the corpus checks. Question types are `number`, `date`, `condition`, `procedure` and `yes/no`. Use `phrase` as the answer type for textual answers.

Once those data files are present, run with Python 3.12.

```sh
python dataset.py data/passages.jsonl data/base_questions.jsonl data/questions.jsonl
```

The script checks schema basics and evidence references, assigns a reproducible validation/test split grouped by base question and stratified by answerability, and prints dataset statistics. It cannot verify semantic equivalence, passage sufficiency or answer absence on its own.

For 100 answerable and 40 unanswerable base questions, the split yields 84 validation records and 336 test records. Tune hybrid α and the refusal threshold on validation. Reserve the test set for final comparisons. Record independent reviewer judgments before resolving disagreements and report agreement from those original judgments.

## Run a query

Install the Python dependencies using `python -m pip install -r requirements.txt`.
With your corpus present, run `python qa.py data/passages.jsonl "Exam rechecking kaise karu?" --method hybrid`.
Use `--method bm25` or `--method tfidf` for lexical retrieval and `--method dense` for semantic retrieval. Dense and hybrid require model weights, available from a model hub or a local checkpoint. The optional `--generator` expects an instruction-tuned causal model with a chat template. Tune the refusal threshold and hybrid weight on validation before using them for evaluation. The citation check verifies retrieved IDs. Evidence entailment and multilingual answer quality still require evaluation.

The course PDF requires six modules. The project supports lexical retrieval, language slices and score-gate evaluation. The evaluation script also supports dense/hybrid retrieval and direct/RAG generation with pretrained weights. The 420-record benchmark is documented below. A small Hindi MIRACL adaptation was run separately.

## CSET 346 pilot

From this folder, `python evaluate.py` reproduces the saved lexical pilot and BM25 score-gate metrics.
Run `python analyze.py` to regenerate the test-case walkthrough.
Run `python qa.py data/passages.jsonl "How long do I have to request re-evaluation?" --method bm25` for the searchable citation demo.
Use `python evaluate.py --encoder intfloat/multilingual-e5-small --generator Qwen/Qwen2.5-0.5B-Instruct --output results/model_final` for pretrained dense, hybrid, direct generation and RAG evaluation once model weights are available. Use a separate run with a MIRACL-adapted local E5 checkpoint for adaptation comparisons.
The pilot has 16 base questions and 48 records (9 validation, 39 test). The passages are paraphrased facts from public documents. Unanswerability is bounded to these nine passages. Scores are preliminary and rank ties matter on such a small corpus. The dataset has not undergone independent human review.

## Public-data adaptation

`python train_miracl.py --parquet hi=hi.parquet --per-language 128` fine-tunes E5 on a supplied MIRACL training split using retrieval triples. The command does not read the Bennett dataset. It saves weights and a training log under `checkpoints/miracl-e5`. Evaluate that checkpoint separately using `python evaluate.py --encoder checkpoints/miracl-e5 --output results/adapted`. The official converted Hindi training file is available at https://huggingface.co/datasets/miracl/miracl/resolve/refs%2Fconvert%2Fparquet/hi/train/0000.parquet. Add another --parquet flag when a second language training file is available.

The experimental JSON stores confusion-matrix counts, retrieval metrics and, when a generator is provided, direct-versus-RAG QA scores. Each run also writes test cases and can store raw predictions. Heuristic language detection is used in the demo and benchmark slices use the annotated language column.

## Extend the evidence collection

Extract each public PDF locally with `pdftotext -layout input.pdf DOC01.txt` or copy the relevant plain text from the public HTML page where its terms permit. Review OCR, footers, line breaks and table associations manually. Put each heading on a line beginning with `## ` and format table rows as complete statements with units and labels. Keep sources in `data/sources.csv` and run `python segment.py data/sources.csv raw/text data/passages.jsonl`. Revalidate gold references and absence before regenerating the split after corpus changes.

## Recorded demonstrations

- `results/demo_answer.json` shows the model returning “After 15 days” with the re-evaluation passage citation.
- `results/demo_refusal.json` illustrates the refusal path with a deliberately strict 0.99 dense-score cutoff. This cutoff is illustrative and differs from the validation-selected one.
- `results/demo_missed_refusal.json` shows the model echoing an unsupported question with a structurally valid citation. Citation ID validation alone does not establish entailment.

The adaptation pilot used `--parquet hi=hi.parquet --per-language 16` and updated only the final transformer block. Its training log and held-out results are under `results/adapted`. The English conversion was unavailable at the attempted official path. Model weights can be recreated with the saved training command and seed.

To run the full CLI demo with the learned pilot threshold, use:

```sh
python qa.py data/passages.jsonl "How long after results do I have to request re-evaluation?" --method hybrid --alpha .5 --threshold .778934 --generator Qwen/Qwen2.5-0.5B-Instruct
```

`data/candidate_sources.csv` contains further official documents to review for the larger corpus. `data/independent_annotation.csv` is the blinded review worksheet. It contains no fabricated second-annotator labels.

The first 39-query direct/RAG run is under `results/model` and used strict JSON parsing. To reproduce it, add `--strict-json` to the generation evaluation command. Some valid-looking JSON appeared inside Markdown fences, which the initial parser rejected. The demo accepts fenced JSON. Generated-answer exact match and token F1 compare against English gold strings, so valid Hindi or Hinglish wording can score low. The citation audit measures matching gold passage IDs and does not establish answer entailment.

## Expanded benchmark

Run these commands from the project root. The original pilot uses `data/` and is retained for comparison.

```sh
python expand_benchmark.py
python evaluate.py --data benchmark --encoder intfloat/multilingual-e5-small --output results/benchmark
python evaluate.py --data benchmark --encoder intfloat/multilingual-e5-small --generator Qwen/Qwen2.5-0.5B-Instruct --batch-size 12 --max-new-tokens 52 --output results/benchmark_qa
python audit_citations.py results/benchmark_qa/predictions.json --questions benchmark/questions.jsonl
python review_benchmark.py
```

The QA run compares prompts with and without evidence using the same model and token budget. The corpus, generated labels and limitations are documented in `BENCHMARK_STATUS.md`. To score a completed independent review, run `python annotation_agreement.py reviewed_annotations.csv`. Blank rows are excluded. The script does not assign values to missing ratings.

Run the expanded demonstration with its validation-selected lexical weight and score threshold:

```sh
python qa.py benchmark/passages.jsonl "What is the minimum course attendance across lectures, tutorials and labs?" --method hybrid --alpha .25 --threshold .841867 --generator Qwen/Qwen2.5-0.5B-Instruct
```

The answer and insufficient-evidence examples are saved under `results/benchmark/demo_*.json`.

`python paired_retrieval.py` reproduces the paired bootstrap comparison of hybrid and BM25 MRR@10. It resamples answerable base intents so that translations of a single question do not count as independent observations.
