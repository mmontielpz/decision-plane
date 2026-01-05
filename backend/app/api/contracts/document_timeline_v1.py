from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class TimelineEventV1(BaseModel):
    timestamp: str
    event_type: str
    description: str
    metadata: Optional[dict]

    model_config = ConfigDict(
        extra="forbid"
    )


class DocumentTimelineV1(BaseModel):
    document_id: str
    events: List[TimelineEventV1]

    model_config = ConfigDict(
        extra="forbid"
    )
