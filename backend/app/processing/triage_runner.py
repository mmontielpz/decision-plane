from datetime import datetime

from app.db.database import get_connection
from app.core.models.document import Document, ProcessingState
from app.core.triage.engine import evaluate
from app.serving.repository import PredictionRepository

REVIEW_QUEUE_CONFIDENCE_THRESHOLD = 0.80


def _load_document(document_id: str) -> Document:
    """
    Minimal document loader for triage.
    Loads only the fields required by the core Document model.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, created_at
        FROM documents
        WHERE id = ?
        """,
        (document_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise ValueError(f"Document not found: {document_id}")

    return Document(
        id=row[0],
        source="unknown",
        raw_metadata={},
        created_at=datetime.fromisoformat(row[1]),
        state=ProcessingState.PROCESSED,
    )


def triage_document(document_id: str):
    """
    Orchestrates document triage:
    - loads minimal document data
    - loads latest prediction
    - evaluates deterministic triage
    """

    document = _load_document(document_id)

    prediction_repo = PredictionRepository()
    prediction = prediction_repo.get_latest_prediction(document_id)

    return evaluate(document, prediction, confidence_threshold=REVIEW_QUEUE_CONFIDENCE_THRESHOLD)
