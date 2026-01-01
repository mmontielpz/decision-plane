# app/adapters/document_adapter.py

from app.db.database import get_connection
from app.serving.document_detail_repository import get_document_detail


class DocumentAdapter:
    """
    Product-facing adapter for document views.

    Responsibilities:
    - Delegate read-model assembly to serving layer
    - Expose stable, UI-oriented shapes
    - Contain NO business logic
    """

    def list_documents(self):
        """
        Lightweight list view for product UI.

        Source of truth:
        documents + document_processing_status
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
                ps.updated_at AS processed_at
            FROM documents d
            LEFT JOIN document_processing_status ps
                ON d.id = ps.document_id
            ORDER BY d.created_at DESC
            """
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
                "processed_at": r[6],
            }
            for r in rows
        ]

    def get_document_by_id(self, document_id: str):
        """
        Full document detail view.

        Delegates to the canonical read-model repository.
        """
        return get_document_detail(document_id)
