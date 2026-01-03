from typing import Optional
from pydantic import BaseModel


class DashboardSummaryV1(BaseModel):
    """
    V1 contract — do not change without version bump.
    """
    total_visible_documents: int
    processed_documents: int
    documents_needing_review: int
    latest_activity_at: Optional[str]

    class Config:
        extra = "forbid"
