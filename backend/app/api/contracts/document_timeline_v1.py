from typing import List, Optional
from pydantic import BaseModel


class TimelineEventV1(BaseModel):
    timestamp: str
    event_type: str
    description: str
    metadata: Optional[dict]

    class Config:
        extra = "forbid"


class DocumentTimelineV1(BaseModel):
    document_id: str
    events: List[TimelineEventV1]

    class Config:
        extra = "forbid"
