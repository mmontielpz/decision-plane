from app.db.database import get_connection

CONFIDENCE_THRESHOLD = 0.80


def get_review_queue() -> list[dict]:
    """
    Read-only review queue for Accounts Payable (v1).

    A document appears in the review queue if:
    - ingestion_status is processed or indexed
    - AND (
        document_type = 'unknown'
        OR prediction confidence < CONFIDENCE_THRESHOLD
        OR missing prediction
      )

    Scope:
    - PDFs digitales
    - Clases: invoice | unknown
    - No OCR
    - No writes
    """

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # Latest prediction per document
    # -------------------------
    cursor.execute(
        """
        WITH latest_predictions AS (
            SELECT
                pe.document_id,
                pe.score,
                pe.threshold,
                pe.created_at,
                ROW_NUMBER() OVER (
                    PARTITION BY pe.document_id
                    ORDER BY pe.created_at DESC
                ) AS rn
            FROM prediction_events pe
        )
        SELECT
            d.id AS document_id,
            d.document_type,
            d.ingestion_status,

            lp.score,
            lp.threshold,

            MAX(
                COALESCE(lp.created_at, ''),
                COALESCE(dps.updated_at, '')
            ) AS last_activity_at

        FROM documents d
        JOIN document_processing_status dps
            ON d.id = dps.document_id

        LEFT JOIN latest_predictions lp
            ON d.id = lp.document_id
           AND lp.rn = 1

        WHERE d.ingestion_status IN ('processed', 'indexed')
          AND (
                d.document_type = 'unknown'
                OR lp.document_id IS NULL
                OR lp.score < ?
          )

        ORDER BY last_activity_at DESC
        """,
        (CONFIDENCE_THRESHOLD,),
    )

    rows = cursor.fetchall()
    conn.close()

    review_queue = []

    for r in rows:
        document_id = r[0]
        document_type = r[1]
        ingestion_status = r[2]
        score = r[3]
        threshold = r[4]
        last_activity_at = r[5]

        # -------------------------
        # Reason prioritization (deterministic)
        # -------------------------
        if score is None:
            reason = "missing_prediction"
        elif document_type == "unknown":
            reason = "unknown"
        elif score < CONFIDENCE_THRESHOLD:
            reason = "low_confidence"
        else:
            # Should not happen due to WHERE clause
            continue

        review_queue.append(
            {
                "document_id": document_id,
                "document_type": document_type,
                "ingestion_status": ingestion_status,
                "reason": reason,
                "score": score,
                "threshold": CONFIDENCE_THRESHOLD,
                "last_activity_at": last_activity_at,
            }
        )

    return review_queue
