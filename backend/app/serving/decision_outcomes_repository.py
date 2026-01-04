from typing import List, Dict
from app.db.database import get_connection


def list_decision_outcomes() -> List[Dict]:
    """
    Read-model for decision outcomes (v1).

    Returns an empty list when no outcomes exist.
    No aggregation logic yet.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            window_start,
            window_end,
            model_version,
            feature_version,
            threshold,
            n_total,
            n_accept,
            n_review
        FROM decision_outcomes
        ORDER BY window_start ASC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "window_start": r[0],
            "window_end": r[1],
            "model_version": r[2],
            "feature_version": r[3],
            "threshold": r[4],
            "n_total": r[5],
            "n_accept": r[6],
            "n_review": r[7],
        }
        for r in rows
    ]
