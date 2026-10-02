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
- `backend_api.py` — optional FastAPI HTTP service (`GET /health`, `POST /analyse`).
- `APP/` — measured core AI workflow used by both interfaces.
- `DATA/` — labelled classification questions and the 20-note grounding knowledge base.
