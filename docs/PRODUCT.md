# Product Documentation — Badminton AI Coach

## Persona
**Mei**, a beginner recreational badminton player practising without a full-time coach. After a session she can describe what went wrong (for example, “my clear is short” or “I reach the rear corner late”) but may not know whether the root issue is technique, footwork or equipment, nor which drill is supported by reliable notes.

## Input
A short natural-language description of a beginner badminton problem.

## Output
- predicted category: `technique`, `footwork`, or `equipment`
- classifier confidence and class probabilities
- retrieved note IDs and similarity scores
- concise grounded `likely_issue` and `drill`
- explicit abstention when the notes do not support a useful answer
- token usage for the rented LLM call

## High-level backend architecture

```text
Player text
    |
    v
Local TF-IDF + Logistic Regression classifier
    | category + confidence
    v
Category-filtered local retrieval
(MiniLM sentence embeddings; TF-IDF fallback)
    | top-3 evidence notes
    v
GPT-4o-mini grounded advisor via OpenRouter
    |
    v
JSON advice + evidence note IDs
```

The same pipeline can be invoked through `demo.py` (CLI) or `api.py` (FastAPI HTTP wrapper). These are presentation/service wrappers only; the measured AI logic lives in `app/`.

## Own vs rent

| Layer | Decision | Reason |
|---|---|---|
| 75-question labelled dataset | Own | Defines the bounded classification task |
| 20-note badminton knowledge base | Own | Domain grounding evidence |
| TF-IDF classifier | Own/local | Cheap, inspectable, no per-query API fee |
| Retrieval logic | Own/local | Controls which evidence reaches generation |
| Prompt and abstention rule | Own | Defines acceptable advice behaviour |
| GPT-4o-mini | Rent | Natural-language synthesis is the part where a foundation model adds value |
| OpenRouter | Rent | Commodity model-serving layer |
| FastAPI wrapper | Own | Optional backend service interface; does not change the experiment |

## Why this architecture
The bounded classification problem is cheap and testable locally; the generative model is reserved for the task where natural-language synthesis adds value. Retrieval constrains generation to the author's badminton notes. The system is deliberately a **workflow rather than a fully autonomous agent** because its step sequence is known in advance.

## Metrics targeted
- Classification accuracy > majority-class baseline (33.3%).
- Advice specificity: target >= 80% of 10 hand-marked cases.
- Advice support by notes: target >= 90%.
- No unsupported invention: target >= 90%.
- Secondary diagnostics: route correctness, evidence recall@3, token use and abstention rate.

## Metrics reached
- Majority-class baseline: **33.3%**.
- Local TF-IDF classifier: **70.4% (19/27)**.
- GPT-4o-mini classification baseline: **100.0% (27/27)** in the preserved original run.
- Route correctness: **7/10 (70%)**.
- Evidence recall@3: **7/10 (70%)**.
- Abstentions: **4/10 (40%)**.
- Advice specificity: **6/10 (60%)**.
- Advice supported by notes: **6/10 (60%)**.
- No unsupported invention: **10/10 (100%)**.
- Final advice run token use: **2,338 input / 570 output**.

The system met the no-invention target but missed specificity and support targets. The primary product implication is to improve routing/fallback retrieval and reduce unnecessary abstention before adding more autonomy.

## Explicit non-use
The system is not intended to diagnose pain or injury, provide medical advice, or replace qualified coaching. Text input cannot verify body mechanics.
