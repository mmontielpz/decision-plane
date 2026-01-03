from app.db.database import get_connection
from app.processing.triage_runner import triage_document


def get_review_queue() -> list[dict]:
    """
    Read-only review queue (framework-level).

    Selection:
    - Documents with ingestion_status processed or indexed

    Decision:
    - Delegated to core triage engine
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            d.id AS document_id,
            d.document_type,
            d.ingestion_status,
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

    for r in rows:
        document_id = r[0]
        document_type = r[1]
        ingestion_status = r[2]
        last_activity_at = r[3]

        result = triage_document(document_id)

        if not result.requires_human_review:
            continue

        for signal in result.signals:
            review_queue.append(
                {
                    "document_id": document_id,
                    "document_type": document_type,
                    "ingestion_status": ingestion_status,
                    "reason": signal.type.value,
                    "severity": signal.severity,
                    "last_activity_at": last_activity_at,
                }
            )

    return review_queue


def get_review_reason_for_document(document_id: str) -> str | None:
    """
    Returns the review reason for a document if it is currently in the review queue.
    """
    queue = get_review_queue()
    for item in queue:
        if item["document_id"] == document_id:
            return item["reason"]
    return None
