from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class LatestPredictionV1(BaseModel):
    label: str
    confidence: float
    model_version: str

    class Config:
        extra = "forbid"


class ProcessingInfoV1(BaseModel):
    status: str
    processed_path: Optional[str]
    feature_path: Optional[str]
    updated_at: Optional[str]

    class Config:
        extra = "forbid"


class ArtifactV1(BaseModel):
    artifact_type: str
    content_ref: str
    created_at: str

    class Config:
        extra = "forbid"


class SignalV1(BaseModel):
    signal_type: str
    signal_value: str
    confidence: Optional[float]
    created_at: str

    class Config:
        extra = "forbid"


class DocumentDetailV1(BaseModel):
    """
    V1 contract — do not change without version bump.
    """
    id: str
    filename: str
    document_type: str
    ingestion_status: str
    created_at: str

    processing: ProcessingInfoV1
    artifacts: List[ArtifactV1]
    signals: List[SignalV1]

    latest_prediction: Optional[LatestPredictionV1]
    review_reason: Optional[str]

    class Config:
        extra = "forbid"
