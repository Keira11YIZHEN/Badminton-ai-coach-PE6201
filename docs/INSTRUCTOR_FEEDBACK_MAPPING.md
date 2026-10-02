# Instructor feedback -> concrete project change

| Instructor feedback | What changed in this repository | Evidence |
|---|---|---|
| “75 questions… held-out split… fix the split size and report it as counts.” | Exact deterministic split documented as **48 train / 27 test**, with 9 test items per class. Same-author phrasing bias is stated as a limitation. | `data/badminton_questions.csv`, `data/split_manifest.csv`, `data/README.md` |
| “Accuracy measures the classifier… nothing scores the advice.” | Added a fixed **10-case end-to-end advice evaluation** and completed the final run. | `evals/advice_eval.csv`, `results/advice_eval_final.csv` |
| “Is the drill specific?” | Added a manual 0/1 specificity rubric; final result **6/10**. | `evals/README.md`, `results/final_eval_summary.json` |
| “Is it supported by the notes?” | Each output records retrieved note IDs; final manual support result **6/10**. | `evals/eval_advice.py`, `results/advice_eval_final.csv` |
| “Does it invent anything?” | Prompt forbids unsupported facts/timings/diagnoses; final no-invention result **10/10**. | `app/advisor.py`, `results/final_eval_summary.json` |
| “Class 1 baseline is named but not run: run it.” | Majority-class baseline reproduced on the same held-out test population: **33.3%**. | `evals/eval_classifier.py`, `results/classifier_local_reproduction.json` |
| “All six touched, 4 not raised.” | Final report explicitly applies the Class 4 workflow-vs-agent distinction and explains why a fixed workflow is more appropriate; agentic re-query is future work. | `docs/PE6201_Final_Report_FINAL.*`, `docs/PRODUCT.md` |
| “Data & evals: transparently check-in the data… explainer files.” | Separate data/evals folders with README explainers and fixed ground truth. | `data/README.md`, `evals/README.md` |
| “README… enough instructions for me/TA to run.” | Clone/setup/evaluation/CLI/API instructions and repository map included. | `README.md` |
| “Code documented at file & module level.” | Core Python modules contain module-level documentation and clear responsibilities. | `app/*.py`, `evals/*.py`, `api.py` |
| “Product Documentation: Persona, Input, Output, Architecture, metrics targeted/reached.” | Dedicated backend product documentation and architecture description. | `docs/PRODUCT.md`, `docs/ARCHITECTURE.md` |
| “Report… reasoning depth… critique outcomes, evals, difficulties, tuning, rough edges.” | Final report focuses on trade-offs, same-author limitation, routing/retrieval/generation failures, unsuccessful prompt tuning and future path. | `docs/PE6201_Final_Report_FINAL.*` |
| “Demo… face visible + screen; precision, articulation, succinctness.” | Timed 5–6 minute backend demo script with happy path, failure case, metrics, trade-off and limitation. | `docs/VIDEO_SCRIPT.md` |
| “How your project made the world different vs today / problem significance.” | Current-market context included without claiming category novelty; the narrower gap is text-first, low-cost and auditable note-grounded advice. | `docs/EXTERNAL_CONTEXT.md`, final report section 1 |
| “Metrics performance critique / evals critique.” | Measurement provenance distinguishes reproduced and preserved measurements; final advice run records route correctness, evidence recall@3, tokens and abstention. | `results/README.md`, `results/metric_provenance.csv`, `results/final_eval_summary.json` |
