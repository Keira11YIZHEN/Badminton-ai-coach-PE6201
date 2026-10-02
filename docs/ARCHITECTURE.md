# Backend architecture

```text
+--------------------------+
|  Natural-language input  |
+------------+-------------+
             |
             v
+--------------------------+
| TF-IDF + Logistic Reg.   |
| category + confidence    |
+------------+-------------+
             |
             v
+--------------------------+
| Category-filtered RAG    |
| MiniLM / TF-IDF fallback |
| top-3 evidence notes     |
+------------+-------------+
             |
             v
+--------------------------+
| GPT-4o-mini / OpenRouter |
| grounded JSON advice     |
+------------+-------------+
             |
             v
+--------------------------+
| likely_issue + drill +   |
| evidence_note_ids        |
+--------------------------+
```

## Interfaces

- `demo.py` — command-line demonstration.
- `api.py` — optional FastAPI HTTP service (`GET /health`, `POST /analyse`).
- `app/` — measured core AI workflow used by both interfaces.
