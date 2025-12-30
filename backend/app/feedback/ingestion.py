# app/feedback/ingestion.py

from typing import Optional
from app.feedback.repository import FeedbackRepository


def ingest_feedback(
    *,
    external_id: str,
    source: str,
    feedback_value: str,
    prediction_event_id: Optional[int] = None,
    confidence: Optional[float] = None,
    notes: Optional[str] = None,
) -> int:
    """
    Ingests feedback and optionally links it to a prediction event.
    """
    repo = FeedbackRepository()

    feedback_id = repo.insert_feedback_event(
        external_id=external_id,
        source=source,
        feedback_value=feedback_value,
        confidence=confidence,
        notes=notes,
    )

    if prediction_event_id is not None:
        repo.link_feedback_to_prediction(
            feedback_id=feedback_id,
            prediction_event_id=prediction_event_id,
        )

    return feedback_id
