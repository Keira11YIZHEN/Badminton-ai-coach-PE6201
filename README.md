# Badminton AI Coach — PE6201 Project

A **backend-only AI prototype** for beginner badminton training. A natural-language problem is routed by a local **TF-IDF + logistic-regression classifier**, grounded against a **20-note badminton knowledge base**, and passed to **GPT-4o-mini via OpenRouter** only for the final advice-generation step.

The repository is intentionally modest: the core contribution is the **measured hybrid AI workflow and its evaluation**, not a front-end interface.

## What the system does

```text
User question
    |
    v
Local TF-IDF + Logistic Regression
    |  category + confidence
    v
Category-filtered retrieval
MiniLM sentence embeddings (TF-IDF fallback)
    |  top-3 evidence notes
    v
GPT-4o-mini via OpenRouter
    |
    v
Grounded JSON advice + evidence note IDs
```

This is a **workflow, not a full autonomous agent**: the sequence is known in advance, so extra autonomy would add cost and failure modes without solving a demonstrated need.

## Final measured results

### Classification

| System | Held-out accuracy | Runtime cost | Saved latency |
|---|---:|---:|---:|
| Majority-class baseline | **33.3%** | $0 | ~0 ms |
| Local TF-IDF classifier | **70.4% (19/27)** | $0 API | 0.08 ms/item |
| GPT-4o-mini classification baseline | **100.0% (27/27)** | recurring API | 789 ms/item |

The fixed stratified split contains **48 training examples and 27 held-out test examples**, with 9 test items in each of the three classes. All 75 questions were written by the same author, so the held-out score is a **within-author generalisation** result, not a population-wide benchmark.

### Final 10-case end-to-end advice evaluation

| Metric | Result |
|---|---:|
| Drill specificity | **60% (6/10)** |
| Supported by retrieved notes | **60% (6/10)** |
| No unsupported invention | **100% (10/10)** |
| Route correctness | **70% (7/10)** |
| Evidence recall@3 | **70% (7/10)** |
| Abstentions | **40% (4/10)** |
| Token use | **2,338 input / 570 output** |

Interpretation: the grounding guardrail prevented unsupported invention in all ten hand-marked cases, but routing errors and conservative abstention reduced usefulness.

## Repository map

```text
app/          core classifier, retrieval, advisor and pipeline modules
data/         75 labelled questions, 20 notes and split manifest
evals/        reproducible classifier eval + fixed 10-case advice eval
results/      measured outputs and provenance/audit trail
notebooks/    original evidence + revised final-run notebooks
docs/         report, product documentation, video plan and feedback mapping
api.py        optional FastAPI HTTP wrapper
demo.py       command-line end-to-end demo
requirements.txt
```

## Quick start

### 1. Create an environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Reproduce the local classifier evaluation

No API key is needed:

```bash
python -m evals.eval_classifier
```

Expected headline results:

```text
Total: 75 | train: 48 | test: 27
Majority baseline: 33.3%
TF-IDF accuracy: 70.4% (19/27)
```

### 3. Run the command-line backend demo

Set your own OpenRouter key locally. **Never commit it to GitHub.**

macOS / Linux:

```bash
export OPENROUTER_API_KEY='your-key-here'
python demo.py
```

Windows PowerShell:

```powershell
$env:OPENROUTER_API_KEY='your-key-here'
python demo.py
```

If no environment variable is present, `demo.py` will request the key through a hidden terminal input.

### 4. Optional: run as an HTTP backend

```bash
uvicorn api:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Analyse a badminton problem:

```bash
curl -X POST http://127.0.0.1:8000/analyse \
  -H "Content-Type: application/json" \
  -d '{"question":"My net shot keeps hitting the tape because I push too hard."}'
```

Interactive API documentation is available locally at `/docs` when FastAPI is running.

## Evaluation

Classifier evaluation:

```bash
python -m evals.eval_classifier
```

LLM-backed advice evaluation:

```bash
python -m evals.eval_advice
```

The final ten outputs are hand-marked on the instructor-requested dimensions:

1. **Specific** — is the drill concrete and actionable?
2. **Supported** — are the advice and factual claims supported by retrieved notes?
3. **No invention** — did the model avoid unsupported facts, timings, repetitions, diagnoses or safety claims?

The measured case-level results are stored in `results/advice_eval_final.csv`; the summary is in `results/final_eval_summary.json`.

## Known failure modes

1. **Routing errors propagate.** Retrieval is category-filtered. If the TF-IDF classifier chooses the wrong category, the correct evidence can become unreachable.
2. **Over-conservative abstention.** In some cases relevant evidence was retrieved, but the generator still returned `The notes do not say`.
3. **Generalisation is limited.** All 75 classification questions were written by the same author.
4. **Text cannot observe mechanics.** The system cannot verify actual body movement or diagnose injury.

These failures are documented rather than hidden; they motivate confidence-based fallback retrieval and broader independent evaluation before adding autonomy.

## Responsible-use boundary

This prototype is a learning aid for beginner practice. It is **not** a medical diagnostic system and does not replace qualified coaching. The generator is instructed to use only retrieved notes and to abstain when the evidence does not support an answer.

## Measurement provenance

Every headline number is tagged as either **reproduced** or **preserved from an executed notebook**. See:

- `results/metric_provenance.csv`
- `results/README.md`
- `notebooks/original/`
- `notebooks/revised/PE6201_Final_API_Run_v3_NoSecret.ipynb`

## Security

- No API key is committed in this repository.
- `.env`, `*.key`, and common secret files are ignored by `.gitignore`.
- If a key is ever exposed in a screenshot or commit, revoke it and create a new one.
