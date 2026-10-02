# Results and measurement provenance

This folder distinguishes **reproduced measurements**, **preserved measurements from the original executed notebooks**, and the **final measured advice run**.

## Reproduced locally
`python -m evals.eval_classifier` reproduces the deterministic 48/27 split, 33.3% majority baseline and 70.4% TF-IDF accuracy. Runtime latency can differ by machine.

## Preserved original measurements
GPT-4o-mini classifier accuracy/latency/cost, the five RAG knowledge checks, the earlier retrieval failure, and the Part 3 L1/L2 results are preserved from executed cells in `notebooks/original/`.

## Final ten-case advice run
Files:
- `advice_eval_final.csv` — case-level model outputs and the three hand marks;
- `final_eval_summary.json` — compact final counts;
- `advice_eval_summary.json` — expanded machine-readable summary.

Final results:
- route correctness: **7/10**;
- evidence recall@3: **7/10**;
- abstentions: **4/10**;
- specificity: **6/10**;
- supported by notes: **6/10**;
- no unsupported invention: **10/10**;
- tokens: **2,338 input / 570 output**.

See `metric_provenance.csv` for the audit trail.
