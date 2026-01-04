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
