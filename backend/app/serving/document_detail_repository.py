from app.db.database import get_connection

VISIBLE_PROCESSING_STATUSES = ("processed", "indexed")


def get_document_detail(document_id: str) -> dict | None:
    """
    Read-only document detail view for Product/UI.

    Visibility rule:
        Document must have processing_status ∈ ('processed','indexed')
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            d.id,
            d.filename,
            d.document_type,
            d.ingestion_status,
            d.created_at,

            ps.status AS processing_status,
            ps.processed_path,
            ps.feature_path,
            ps.updated_at AS processed_at
        FROM documents d
        JOIN document_processing_status ps
            ON d.id = ps.document_id
        WHERE d.id = ?
          AND ps.status IN (?, ?)
        """,
        (document_id, *VISIBLE_PROCESSING_STATUSES),
    )

    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    document = {
        "id": row[0],
        "filename": row[1],
        "document_type": row[2],
        "ingestion_status": row[3],
        "created_at": row[4],
        "processing": {
            "status": row[5],
            "processed_path": row[6],
            "feature_path": row[7],
            "updated_at": row[8],
        },
        "artifacts": [],
        "signals": [],
        "latest_prediction": None,
    }

    # Artifacts
    cursor.execute(
        """
        SELECT artifact_type, content_ref, created_at
        FROM document_artifacts
        WHERE document_id = ?
        ORDER BY created_at ASC
        """,
        (document_id,),
    )
    document["artifacts"] = [
        {
            "artifact_type": r[0],
            "content_ref": r[1],
            "created_at": r[2],
        }
        for r in cursor.fetchall()
    ]

    # Signals
    cursor.execute(
        """
        SELECT signal_type, signal_value, confidence, created_at
        FROM document_signals
        WHERE document_id = ?
        ORDER BY created_at ASC
        """,
        (document_id,),
    )
    document["signals"] = [
        {
            "signal_type": r[0],
            "signal_value": r[1],
            "confidence": r[2],
            "created_at": r[3],
        }
        for r in cursor.fetchall()
    ]

    conn.close()
    return document
