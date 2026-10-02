# Product Documentation - Badminton AI Coach

## Persona
**Kai**, a beginner recreational badminton player who plays weekly and does not have regular coach access. After a session, Kai can describe what went wrong (for example, "my clear is short" or "I reach the rear corner late") but may not know whether the likely cause is technique, footwork or equipment, nor which corrective action is supported by the available notes.

## Input
A short natural-language description of a beginner badminton problem.

## Output
- predicted category: `technique`, `footwork`, or `equipment`
- classifier confidence and class probabilities
- retrieved note IDs and similarity scores
- concise grounded `likely_issue` and `drill`
- explicit abstention when retrieved notes do not support a useful answer
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

The same pipeline can be invoked through `demo.py` (CLI) or `api.py` (FastAPI HTTP wrapper). These are interface/service wrappers only; the measured AI logic lives in `app/`.

## Own vs rent

| Layer | Decision | Reason |
|---|---|---|
| 75-question labelled dataset | Own | Defines the bounded classification task |
| 20-note badminton knowledge base | Own | Provides traceable grounding evidence |
| TF-IDF classifier | Own/local | Cheap, inspectable and no per-query API fee |
| Retrieval logic | Own/local | Controls which evidence reaches generation |
| Prompt and abstention rule | Own | Defines acceptable generation behaviour |
| GPT-4o-mini | Rent | Foundation model adds value for concise language synthesis |
| OpenRouter | Rent | Commodity model-serving layer |
| FastAPI wrapper | Own | Optional backend service interface; does not change the experiment |

## Why this architecture
The bounded classification task is cheap and testable locally, while the foundation model is reserved for natural-language synthesis. Retrieval constrains generation to the project knowledge base. The system is deliberately a **workflow rather than a fully autonomous agent** because the sequence is fixed: classify -> retrieve -> generate.

## Metrics targeted in the original project plan
- Primary: held-out classification accuracy should outperform a simple baseline.
- Secondary engineering measures: latency and per-query/API cost.
- Responsible behaviour: reduce silent failure and avoid presenting unsupported advice as certain.

The Week 3 plan discussed both a keyword-rule baseline and, in its success-metric section, a majority-class baseline. The final evaluation uses the **majority-class baseline** as the reproducible reference. A classifier confidence threshold was proposed as later work; confidence is exposed in the final backend, but automatic threshold-based routing fallback is not implemented.

## Additional final outcome metrics
To evaluate the complete advice pipeline rather than classification alone, the final project adds a fixed 10-case end-to-end test with:
- route correctness
- evidence recall@3
- abstention rate
- token use
- three project-defined human marks: drill specificity, support by retrieved notes, and no unsupported invention

## Metrics reached
- Majority-class baseline: **33.3%**.
- Local TF-IDF classifier: **70.4% (19/27)**.
- GPT-4o-mini classification result: **100.0% (27/27)** in the preserved executed run.
- Route correctness: **7/10 (70%)**.
- Evidence recall@3: **7/10 (70%)**.
- Abstentions: **4/10 (40%)**.
- Advice specificity: **6/10 (60%)**.
- Advice supported by notes: **6/10 (60%)**.
- No unsupported invention: **10/10 (100%)**.
- Final advice run token use: **2,338 input / 570 output**.

Interpretation: the grounding guardrail was strong on unsupported invention, while usefulness remained limited by routing errors, retrieval coverage and conservative abstention.

## Explicit non-use
The system is not intended to diagnose pain or injury, provide medical advice, verify body mechanics, or replace qualified coaching. It is an academic text-based training-support prototype.
