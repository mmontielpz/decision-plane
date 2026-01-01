from app.db.database import get_connection

VISIBLE_PROCESSING_STATUSES = ("processed", "indexed")


def get_dashboard_summary() -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    # Total visible documents
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM document_processing_status
        WHERE status IN (?, ?)
        """,
        VISIBLE_PROCESSING_STATUSES,
    )
    total_visible = cursor.fetchone()[0]

    # Processed documents (v1 == visible)
    processed = total_visible

    # Needs review (v1 placeholder)
    needs_review = 0

    # Latest activity
    cursor.execute(
        """
        SELECT MAX(updated_at)
        FROM document_processing_status
        WHERE status IN (?, ?)
        """,
        VISIBLE_PROCESSING_STATUSES,
    )
    latest_activity = cursor.fetchone()[0]

    conn.close()

    return {
        "total_visible_documents": total_visible,
        "processed_documents": processed,
        "documents_needing_review": needs_review,
        "latest_activity_at": latest_activity,
    }
