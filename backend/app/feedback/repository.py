# app/feedback/repository.py

from datetime import datetime
from typing import Optional

from app.db.database import get_connection


class FeedbackRepository:
    """
    Persistence layer for human/external feedback.

    Guarantees:
    * Idempotent feedback events per (source, external_id)
    * Explicit linkage to prediction_events
    * Append-only semantics
    """

    def insert_feedback_event(
        self,
        *,
        external_id: str,
        source: str,
        feedback_value: str,
        confidence: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> int:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO feedback_events (
                created_at,
                external_id,
                source,
                feedback_value,
                confidence,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                external_id,
                source,
                feedback_value,
                confidence,
                notes,
            ),
        )

        conn.commit()

        cursor.execute(
            """
            SELECT id FROM feedback_events
            WHERE external_id = ? AND source = ?
            """,
            (external_id, source),
        )
        row = cursor.fetchone()
        conn.close()
        return row[0]

    def link_feedback_to_prediction(
        self,
        *,
        feedback_id: int,
        prediction_event_id: int,
    ) -> None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO prediction_feedback_links (
                created_at,
                feedback_id,
                prediction_event_id
            )
            VALUES (?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                feedback_id,
                prediction_event_id,
            ),
        )

        conn.commit()
        conn.close()
