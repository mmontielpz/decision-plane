from typing import List, Optional
from pydantic import BaseModel


class ReplayArtifactV1(BaseModel):
    artifact_type: str
    content_ref: str

    class Config:
        extra = "forbid"


class ReplayProcessingStepV1(BaseModel):
    step_name: str
    status: str
    created_at: str
    metadata_json: Optional[str]
    error_message: Optional[str]

    class Config:
        extra = "forbid"


class ReplayPredictionV1(BaseModel):
    decision: str
    score: float
    threshold: float
    model_version: str
    created_at: str

    class Config:
        extra = "forbid"


class DocumentReplayV1(BaseModel):
    """
    V1 replay contract — immutable, read-only, deterministic.
    """
    document_id: str

    ingestion_timestamp: str
    source_system: Optional[str]

    processing_steps: List[ReplayProcessingStepV1]
    artifacts: List[ReplayArtifactV1]

    prediction: Optional[ReplayPredictionV1]

    class Config:
        extra = "forbid"
