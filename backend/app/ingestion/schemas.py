from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class IngestionRequest(BaseModel):
    """
    Request schema for document ingestion.

    This schema mirrors the existing ingestion pipeline contract.
    Validation is intentionally permissive; semantic checks occur downstream.
    """

    document_id: str
    ingestion_timestamp: datetime
    source_system: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
