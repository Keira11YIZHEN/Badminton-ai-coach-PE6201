# Project origin and final-deliverable alignment

This file replaces the earlier feedback-mapping note. It is intentionally based only on the **Week 3 Project Problem Statement** and the instructor's **final project deliverable guidance** supplied for the end-of-course submission.

## 1. Alignment with the Week 3 Problem Statement

| Week 3 intent | Final implementation | Evidence in repository |
|---|---|---|
| Text-based support for beginner/recreational badminton players | Backend accepts a short natural-language badminton problem and returns grounded advice | `demo.py`, `api.py`, `app/pipeline.py` |
| Three problem types: technique, footwork, equipment | Local TF-IDF + logistic-regression router predicts the three categories | `app/classifier.py`, `data/badminton_questions.csv` |
| Use narrow ML + foundation model + RAG | Final workflow combines local classification, local retrieval and GPT-4o-mini generation | `app/`, `docs/ARCHITECTURE.md` |
| Build domain-specific layers; rent commodity model serving | Data, classifier, retrieval, prompt and evals are project-owned; GPT-4o-mini is accessed through OpenRouter | `docs/PRODUCT.md` |
| 75 labelled questions + custom badminton notes | 75 questions and 20-note grounding corpus are checked in with explainers | `data/` |
| Primary success metric: held-out classification accuracy against a simple baseline | Fixed 48/27 split; majority baseline 33.3%; TF-IDF 70.4% | `evals/eval_classifier.py`, `results/classifier_local_reproduction.json` |
| Secondary engineering measures: latency / cost | Preserved executed measurements are tagged by provenance | `results/metric_provenance.csv` |
| Risk of silent failure and unsuitable advice | Final system exposes confidence/evidence and uses grounded generation with abstention | `app/advisor.py`, `README.md` |
| Confidence-threshold abstention proposed for later iterations | Confidence is exposed, but classifier-level threshold fallback is **not yet implemented** | `app/classifier.py`, final report |

### Transparent design evolution
The Week 3 document mentions a keyword-matching rule as a possible non-AI baseline, while its success-metric section specifies comparison with a majority-class baseline. The final evaluation standardises on the **majority-class baseline** because it is deterministic, reproducible and directly comparable on the fixed held-out set. The repository does not claim that a keyword-rule baseline was executed.

The final project also adds a 10-case end-to-end advice evaluation. This is a **project-defined extension** beyond classification accuracy, used to test route correctness, evidence retrieval, abstention and the quality of generated advice.

## 2. Alignment with final project deliverable guidance

| Final guidance | How this repository addresses it |
|---|---|
| Report around 1,200 words with reasoning depth and critique | Final report is ~1,200 words and covers intended change, trade-offs, performance critique, eval critique, tuning, rough edges and future path | `docs/PE6201_Final_Report_FINAL.*` |
| Well-structured report | Six numbered analytical sections plus a compact headline-metrics table | final report |
| Demo: face + screen, 5 +/- 3 minutes, precise/articulate/succinct | Backend-focused 5-6 minute demo plan | `docs/VIDEO_SCRIPT.md` |
| Check in data and evals with explainer files | Separate `data/` and `evals/` folders, each with README documentation | `data/README.md`, `evals/README.md` |
| README/run instructions for TA | Environment setup, classifier reproduction, CLI demo and optional FastAPI instructions | `README.md` |
| Code documented at file/module level | Core modules and evaluation scripts include module-level responsibilities/docstrings | `app/*.py`, `evals/*.py`, `api.py` |
| Product documentation: Persona, Input, Output, Architecture, Metrics targeted/reached | Dedicated product document and architecture note | `docs/PRODUCT.md`, `docs/ARCHITECTURE.md` |

## 3. Final project position
The final system remains intentionally narrow: a backend-only academic prototype for text-based badminton problem triage and grounded practice advice. It does not claim to replace coaching, diagnose injury, or perform motion analysis. Its main value is that data, code, evidence, metrics and failure cases are all auditable in the repository.
