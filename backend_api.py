"""Optional FastAPI service wrapper for the Badminton AI Coach backend.

This file exposes the existing Python pipeline through HTTP without changing the
classifier, retrieval, grounding, or evaluation logic used in the project.

Run locally:
    export OPENROUTER_API_KEY='...'
    uvicorn backend_api:app --reload

Then POST JSON to /analyse:
    {"question": "My net shot keeps hitting the tape."}
"""
from __future__ import annotations

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from APP.pipeline import BadmintonCoach


app = FastAPI(
    title="Badminton AI Coach API",
    version="1.0.0",
    description="PE6201 backend: local routing + grounded retrieval + LLM advice.",
)


class AnalyseRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)


class AnalyseResponse(BaseModel):
    question: str
    category: str
    classifier_confidence: float
    class_probabilities: dict[str, float]
    retrieval_backend: str
    retrieved: list[dict]
    advice: dict
    usage: dict


def _runtime_key() -> str | None:
    return os.environ.get("OPENROUTER_API_KEY") or os.environ.get("MY_PRIVATE_OPENROUTER_KEY")


@app.get("/health")
def health() -> dict:
    """Cheap health check; does not call the LLM."""
    return {
        "status": "ok",
        "service": "badminton-ai-coach",
        "llm_key_configured": bool(_runtime_key()),
    }


@app.post("/analyse", response_model=AnalyseResponse)
def analyse(payload: AnalyseRequest) -> dict:
    """Run the complete classification → retrieval → grounded-advice pipeline."""
    api_key = _runtime_key()
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OPENROUTER_API_KEY is not configured on the server.",
        )

    try:
        coach = BadmintonCoach(top_k=3, api_key=api_key)
        return coach.run(payload.question.strip())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {type(exc).__name__}") from exc
