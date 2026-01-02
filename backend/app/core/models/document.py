from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class ProcessingState(str, Enum):
    INGESTED = "ingested"
    PROCESSED = "processed"
    TRIAGED = "triaged"


class SignalType(str, Enum):
    LOW_CONFIDENCE = "low_confidence"
    UNKNOWN = "unknown"
    MISSING_PREDICTION = "missing_prediction"


@dataclass(frozen=True)
class Document:
    id: str
    source: str
    raw_metadata: Dict[str, Any]
    created_at: datetime
    state: ProcessingState


@dataclass(frozen=True)
class Prediction:
    label: Optional[str]
    confidence: Optional[float]
    model_version: Optional[str]


@dataclass(frozen=True)
class Signal:
    type: SignalType
    severity: int
    description: Optional[str] = None


@dataclass(frozen=True)
class TriageResult:
    requires_human_review: bool
    signals: List[Signal]
