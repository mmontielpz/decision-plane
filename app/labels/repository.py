from datetime import datetime
import sqlite3
from app.db.database import get_connection


def insert_label(
    *,
    document_id: str,
    label_value: str,
    label_type: str,
    label_source: str,
    label_timestamp: str,
    label_version: int,
    confidence: float | None = None,
) -> bool:
    """
    Inserts a label event in an idempotent way.

    Returns:
        True  -> label inserted
        False -> duplicate label ignored
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO labels (
                document_id,
                label_value,
                label_type,
                label_source,
                label_timestamp,
                label_version,
                confidence,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                document_id,
                label_value,
                label_type,
                label_source,
                label_timestamp,
                label_version,
                confidence,
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # Duplicate label (idempotency)
        return False

    finally:
        conn.close()
