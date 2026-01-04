# backend/app/processing/lineage/models.py

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass(frozen=True)
class ProcessingRun:
    """
    Represents a single deterministic processing execution.
    """
    run_id: str
    document_id: str
    pipeline_version: str
    started_at: datetime
    completed_at: Optional[datetime]
    status: str  # SUCCESS | FAILED
    error_message: Optional[str] = None


@dataclass(frozen=True)
class ProcessingStep:
    """
    Represents a single step within a processing run.
    """
    run_id: str
    step_name: str
    step_version: str
    started_at: datetime
    completed_at: Optional[datetime]
    status: str  # SUCCESS | FAILED
    metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


@dataclass(frozen=True)
class ProcessingArtifactRef:
    """
    Immutable reference to an artifact produced by processing.
    """
    run_id: str
    step_name: str
    artifact_type: str
    content_ref: str
    created_at: datetime
