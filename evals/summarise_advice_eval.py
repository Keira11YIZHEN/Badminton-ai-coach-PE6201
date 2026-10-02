"""Summarise automatic diagnostics and hand-marked advice evaluation results."""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((ROOT / "evals" / "advice_eval.csv").open(encoding="utf-8")))
summary = {"n_cases": len(rows)}

for column in ["category_correct_0_1", "evidence_hit_0_1", "abstained_0_1"]:
    vals = [int(r[column]) for r in rows if r.get(column) in ("0", "1")]
    summary[column] = {
        "marked": len(vals),
        "passes": sum(vals),
        "rate": (sum(vals) / len(vals) if vals else None),
    }

for column in ["prompt_tokens", "completion_tokens"]:
    vals = [int(r[column]) for r in rows if (r.get(column) or "").isdigit()]
    summary[column] = sum(vals) if vals else None

for column in ["specific_0_1", "supported_0_1", "no_invention_0_1"]:
    vals = [int(r[column]) for r in rows if r.get(column) in ("0", "1")]
    summary[column] = {
        "marked": len(vals),
        "passes": sum(vals),
        "pass_rate": (sum(vals) / len(vals) if vals else None),
    }

print(json.dumps(summary, indent=2))
(ROOT / "results" / "advice_eval_summary.json").write_text(
    json.dumps(summary, indent=2), encoding="utf-8"
)
