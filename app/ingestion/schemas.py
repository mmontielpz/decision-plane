from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class IngestionRequest(BaseModel):
    document_id: str = Field(..., description="Unique document identifier")
    ingestion_timestamp: datetime
    document_type: Optional[str] = None
    source_system: Optional[str] = None
