# app/adapters/document_adapter.py

from app.db.database import get_connection
from app.serving.document_detail_repository import get_document_detail


VISIBLE_PROCESSING_STATUSES = ("processed", "indexed")


class DocumentAdapter:
    """
    Product-facing adapter for document views.

    Responsibilities:
    - Define product visibility semantics
    - Delegate read-model assembly to repositories
    - Expose stable, UI-oriented shapes
    - Contain minimal SQL, no business logic
    """

    def list_documents(self):
        """
        Lightweight list view for product UI.

        Canonical visibility rule:
            A document is visible iff its processing_status ∈ ('processed', 'indexed')
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
                dps.status AS processing_status
            FROM documents d
            JOIN document_processing_status dps
                ON d.id = dps.document_id
            WHERE dps.status IN (?, ?)
            ORDER BY dps.updated_at DESC
            """,
            VISIBLE_PROCESSING_STATUSES,
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "filename": r[1],
                "document_type": r[2],
                "ingestion_status": r[3],
                "created_at": r[4],
                "processing_status": r[5],
            }
            for r in rows
        ]

    def get_document_by_id(self, document_id: str):
        """
        Full document detail view.

        Visibility enforcement for detail is handled at the repository level
        or by the calling endpoint (404 if not visible).
        """
        return get_document_detail(document_id)
