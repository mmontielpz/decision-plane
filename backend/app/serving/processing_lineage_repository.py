from app.db.database import get_connection


def list_processing_steps_for_document(document_id: str) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            step_name,
            status,
            metadata_json,
            error_message,
            created_at
        FROM processing_steps
        WHERE document_id = ?
        ORDER BY created_at ASC
        """,
        (document_id,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "step": r[0],
            "status": r[1],
            "metadata": r[2],
            "error": r[3],
            "created_at": r[4],
        }
        for r in rows
    ]


def record_processing_step(
    *,
    document_id: str,
    run_id: str,
    step_name: str,
    status: str,
    metadata_json: str | None = None,
    error_message: str | None = None,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO processing_steps (
            document_id,
            run_id,
            step_name,
            status,
            metadata_json,
            error_message,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            document_id,
            run_id,
            step_name,
            status,
            metadata_json,
            error_message,
            datetime.utcnow().isoformat(),
        ),
    )

    conn.commit()
    conn.close()
