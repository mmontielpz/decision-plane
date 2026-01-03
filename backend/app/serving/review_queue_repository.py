from app.db.database import get_connection
from app.processing.triage_runner import triage_document

DEFAULT_REVIEW_SCORE = 0.50
DEFAULT_REVIEW_THRESHOLD = 0.80


def get_review_queue() -> list[dict]:
    """
    Read-only review queue (Product V1).

    Contract:
    - Stable, minimal, prediction-oriented
    - No internal metadata leakage
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            d.id AS document_id,
            MAX(dps.updated_at) AS last_activity_at
        FROM documents d
        JOIN document_processing_status dps
            ON d.id = dps.document_id
        WHERE d.ingestion_status IN ('processed', 'indexed')
        GROUP BY d.id
        ORDER BY last_activity_at DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    review_queue: list[dict] = []

    for document_id, last_activity_at in rows:
        result = triage_document(document_id)

        if not result.requires_human_review:
            continue

        for signal in result.signals:
            review_queue.append(
                {
                    "document_id": document_id,
                    "score": DEFAULT_REVIEW_SCORE,
                    "threshold": DEFAULT_REVIEW_THRESHOLD,
                    "reason": signal.type.value,
                    "last_activity_at": last_activity_at,
                }
            )

    return review_queue


def get_review_reason_for_document(document_id: str) -> str | None:
    """
    Product-level invariant helper.
    """
    for item in get_review_queue():
        if item["document_id"] == document_id:
            return item["reason"]
    return None
