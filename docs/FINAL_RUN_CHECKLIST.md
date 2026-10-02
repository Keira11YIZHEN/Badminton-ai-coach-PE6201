# Final run status

## Completed evidence
- [x] 75-question dataset exported to CSV.
- [x] Fixed split documented: **48 train / 27 test**, 9 test cases per category.
- [x] Majority baseline reproduced: **33.3%**.
- [x] Local TF-IDF result reproduced: **70.37% (19/27)**.
- [x] GPT-4o-mini classification measurement preserved: **100% on 27/27**.
- [x] 20-note RAG corpus exported and tagged.
- [x] Earlier retrieval failure documented.
- [x] 10 fixed advice evaluation cases written before the final rerun.
- [x] Final 10-case API evaluation completed.
- [x] Human marks completed.
- [x] Final advice metrics: **6/10 specificity, 6/10 support, 10/10 no invention**.
- [x] Automatic diagnostics: **route 7/10, evidence recall@3 7/10, abstentions 4/10**.
- [x] Final token use: **2,338 input / 570 output**.
- [x] Final report generated with no placeholders and prepared for separate submission.
- [x] Individual GitHub repository created and project files uploaded.
- [x] `requirements.txt` and `.gitignore` added.
- [x] README, code imports and documented paths aligned with the current `APP/` and `DATA/` repository layout.

## Remaining submission checks
- [ ] From a clean environment, run `python -m evals.eval_classifier`.
- [ ] Test `python demo.py` or the optional FastAPI backend with a fresh runtime API key.
- [ ] Confirm no API key or secret appears in GitHub commit history.
- [ ] Record and submit the final 5–6 minute face + screen demonstration video.
- [ ] Submit the written report separately as required.

The final measured files are already stored in `results/`. Do not rerun the final advice evaluation merely to improve the score; the purpose is to preserve the measured evidence honestly.
