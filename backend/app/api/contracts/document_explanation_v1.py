from typing import List, Optional
from pydantic import BaseModel


class ExplanationSignalV1(BaseModel):
    type: str
    severity: int
    confidence: Optional[float]
    origin: str

    class Config:
        extra = "forbid"


class ExplanationPredictionV1(BaseModel):
    model_version: str
    score: float
    threshold: float
    decision: str

    class Config:
        extra = "forbid"


class ExplanationProcessingStepV1(BaseModel):
    step_name: str
    status: str

    class Config:
        extra = "forbid"


class DocumentExplanationV1(BaseModel):
    """
    V1 Decision Explanation Contract (Read-Only).

    This contract is intentionally descriptive, not inferential.
    """
    document_id: str
    final_decision: str
    decision_source: str
    summary: str

    signals: List[ExplanationSignalV1]
    prediction: Optional[ExplanationPredictionV1]
    processing_steps: List[ExplanationProcessingStepV1]

    class Config:
        extra = "forbid"
