# Data

## `badminton_questions.csv`
75 manually authored beginner-badminton questions: 25 technique, 25 footwork, 25 equipment.
The fixed original split uses `test_size=0.35`, `random_state=0`, `stratify=label`, giving **48 training** and **27 held-out test** examples (9 per class).

**Important limitation:** all 75 examples were written by one author. The test set is held out from model fitting, but not independent in writing style. Therefore the measured accuracy estimates within-author generalisation, not population-level performance on real players.

## `badminton_notes.json`
20 short, self-authored knowledge notes used for grounded retrieval. No user records or scraped personal data are included. Each note is tagged with one of the three routing categories.

## `split_manifest.csv`
Records the deterministic 48/27 split so another reader can reproduce the exact evaluation population.
