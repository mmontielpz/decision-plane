from app.db.database import get_connection

# Product Read Model — do not reuse for writes or internal pipelines


def get_document_detail(document_id: str) -> dict | None:
    """
    Read-only document detail view for Product/UI.

    Returns:
        None if document does not exist.

        dict with keys:
            id, filename, document_type, ingestion_status, created_at,
            processing, artifacts, signals, latest_prediction
    """

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # Core document + processing status
    # -------------------------
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
        LEFT JOIN document_processing_status ps
            ON d.id = ps.document_id
        WHERE d.id = ?
        """,
        (document_id,),
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

    # Normalize processing state for product semantics
    if document["processing"]["status"] is None:
        document["processing"] = None

    # -------------------------
    # Artifacts
    # -------------------------
    cursor.execute(
        """
        SELECT
            artifact_type,
            content_ref,
            created_at
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

    # -------------------------
    # Signals
    # -------------------------
    cursor.execute(
        """
        SELECT
            signal_type,
            signal_value,
            confidence,
            created_at
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

    # -------------------------
    # Latest prediction (by run creation time)
    # -------------------------
    cursor.execute(
        """
        SELECT
            pe.score,
            pe.threshold,
            pe.decision,
            pe.created_at,
            pr.model_name,
            pr.model_version,
            pr.feature_version
        FROM prediction_events pe
        JOIN prediction_runs pr
            ON pe.run_id = pr.id
        WHERE pe.document_id = ?
        ORDER BY pr.created_at DESC, pe.created_at DESC
        LIMIT 1
        """,
        (document_id,),
    )

    pred = cursor.fetchone()
    if pred:
        document["latest_prediction"] = {
            "score": pred[0],
            "threshold": pred[1],
            "decision": pred[2],
            "created_at": pred[3],
            "model_name": pred[4],
            "model_version": pred[5],
            "feature_version": pred[6],
        }

    conn.close()
    return document
