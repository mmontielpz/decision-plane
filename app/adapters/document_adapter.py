# app/adapters/document_adapter.py

from typing import List, Dict
from app.db.database import get_connection


class DocumentAdapter:
    """
    Product-facing adapter for document listing.

    Hides internal pipeline complexity and exposes
    a simplified, stable view for UI consumers.
    """

    def list_documents(self) -> List[Dict]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                ie.document_id,
                dps.status,
                pe.decision,
                pe.score,
                pe.created_at
            FROM ingestion_events ie
            LEFT JOIN document_processing_status dps
                ON ie.document_id = dps.document_id
            LEFT JOIN (
                SELECT
                    document_id,
                    decision,
                    score,
                    created_at
                FROM prediction_events
                WHERE id IN (
                    SELECT MAX(id)
                    FROM prediction_events
                    GROUP BY document_id
                )
            ) pe
                ON ie.document_id = pe.document_id
            ORDER BY pe.created_at DESC
            """
        )

        rows = cursor.fetchall()
        conn.close()

        results = []
        for r in rows:
            results.append(
                {
                    "document_id": r[0],
                    "status": r[1] or "unknown",
                    "decision": r[2],
                    "score": r[3],
                    "last_updated": r[4],
                }
            )

        return results

    def get_document_by_id(self, document_id: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                ie.document_id,
                COALESCE(dps.status, 'unknown') AS status,
                pe.decision,
                pe.score,
                pe.created_at AS last_updated,
                dps.processed_path,
                dps.feature_path,
                ie.source_system
            FROM ingestion_events ie
            LEFT JOIN document_processing_status dps
              ON ie.document_id = dps.document_id
            LEFT JOIN prediction_events pe
              ON ie.document_id = pe.document_id
            WHERE ie.document_id = ?
            ORDER BY pe.created_at DESC
            LIMIT 1
            """,
            (document_id,),
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return dict(row)
