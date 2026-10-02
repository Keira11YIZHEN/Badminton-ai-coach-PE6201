"""Run the ten fixed end-to-end advice cases and write model outputs.

This script intentionally does NOT assign the three human quality marks. The
course instructor explicitly requested hand marking. After running, open
``evals/advice_eval.csv``, read each output beside its retrieved notes, and enter
0/1 for specificity, note support, and no unsupported invention.

Automatic diagnostics (routing accuracy, evidence recall@3, token counts and
abstention) are recorded separately so the manual outcome labels remain human.
"""
from pathlib import Path
import csv
import json
from app.pipeline import BadmintonCoach

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "evals" / "advice_eval.csv"
rows = list(csv.DictReader(path.open(encoding="utf-8")))
coach = BadmintonCoach(top_k=3)

prompt_tokens = 0
completion_tokens = 0
for i, row in enumerate(rows, 1):
    print(f"[{i}/10] {row['case_id']}: {row['input']}")
    out = coach.run(row["input"])
    retrieved_ids = [h["id"] for h in out["retrieved"]]
    advice = out["advice"]

    row["model_category"] = out["category"]
    row["category_correct_0_1"] = str(int(out["category"] == row["expected_category"]))
    row["classifier_confidence"] = f"{out['classifier_confidence']:.4f}"
    row["retrieval_backend"] = out["retrieval_backend"]
    row["retrieved_note_ids"] = ";".join(retrieved_ids)
    row["evidence_hit_0_1"] = str(int(row["required_evidence"] in retrieved_ids))
    row["model_advice"] = json.dumps(advice, ensure_ascii=False)

    usage = out.get("usage") or {}
    pt = usage.get("prompt_tokens") or 0
    ct = usage.get("completion_tokens") or 0
    row["prompt_tokens"] = str(pt)
    row["completion_tokens"] = str(ct)
    prompt_tokens += pt
    completion_tokens += ct

    drill = str(advice.get("drill", "")) if isinstance(advice, dict) else ""
    row["abstained_0_1"] = str(int("notes do not say" in drill.lower()))
    # Reset marker note on a fresh model run. The human can write it afterwards.
    row["marker_notes"] = ""

    print(
        f"  route={row['model_category']} expected={row['expected_category']} "
        f"evidence_hit={row['evidence_hit_0_1']} notes={row['retrieved_note_ids']}"
    )

fields = list(rows[0].keys())
for name in [
    "category_correct_0_1",
    "classifier_confidence",
    "retrieval_backend",
    "evidence_hit_0_1",
    "prompt_tokens",
    "completion_tokens",
    "abstained_0_1",
]:
    if name not in fields:
        fields.append(name)

with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

category_correct = sum(int(r["category_correct_0_1"]) for r in rows)
evidence_hits = sum(int(r["evidence_hit_0_1"]) for r in rows)
abstentions = sum(int(r["abstained_0_1"]) for r in rows)
print("\nSaved model outputs to", path)
print(
    f"Automatic diagnostics: route {category_correct}/10, "
    f"evidence recall@3 {evidence_hits}/10, abstentions {abstentions}/10"
)
print(f"Tokens: {prompt_tokens} input / {completion_tokens} output")
print("Now hand-mark the three requested 0/1 quality columns. Do not replace them with an LLM judge.")
