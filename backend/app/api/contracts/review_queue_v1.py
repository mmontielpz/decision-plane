from typing import Optional, Literal
from pydantic import BaseModel


ReviewReason = Literal["low_confidence", "unknown", "missing_prediction"]


class ReviewQueueItemV1(BaseModel):
    """
    V1 contract — do not change without version bump.
    """
    document_id: str
    reason: ReviewReason
    score: Optional[float]
    threshold: Optional[float]
    last_activity_at: Optional[str]

    class Config:
        extra = "forbid"
