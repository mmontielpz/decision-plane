from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any


class ProcessedRecord(BaseModel):
    document_id: str
    ingestion_timestamp: datetime
    source_system: str

    processing_timestamp: datetime
    processor_version: str

    extraction_method: str
    normalized_text: str
    raw_path: str


class FeatureRecord(BaseModel):
    document_id: str
    feature_timestamp: datetime
    feature_version: str

    features: Dict[str, float]
    processed_path: str
