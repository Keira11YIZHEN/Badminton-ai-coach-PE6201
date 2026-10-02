# Evaluations

## Classifier evaluation
Run:

```bash
python -m evals.eval_classifier
```

It reports the majority-class baseline and the TF-IDF classifier on the identical 27-item held-out test set. The saved A1 API result is retained separately in `results/classifier_saved_results.json`.

## Advice evaluation
`advice_eval.csv` contains **10 fixed cases** selected before the final API rerun. Run:

```bash
python -m evals.eval_advice
```

The script first records **automatic diagnostics** that do not replace the human rubric: route correctness, evidence recall@3, input/output token counts and whether the model abstained. Then **hand-mark** every case using the instructor's three requested dimensions:

1. **Specific** - Is the drill concrete/actionable rather than generic encouragement?
2. **Supported** - Are the factual claims and drill instructions supported by the retrieved notes?
3. **No invention** - Did the model avoid adding unsupported timings, repetitions, diagnoses, safety claims or facts?

Use `1=pass, 0=fail` in the three mark columns, add a short marker note for failures, then run:

```bash
python -m evals.summarise_advice_eval
```

This manual step is intentional: the instructor asked for hand marking. An LLM judge is not substituted for the human labels. Run `python -m evals.summarise_advice_eval` afterwards to write `results/advice_eval_summary.json` containing both automatic diagnostics and the human pass rates.
