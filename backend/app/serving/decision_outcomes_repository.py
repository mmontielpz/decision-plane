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


def compute_decision_outcomes_single_window(
    *, threshold: float
) -> Dict:
    """
    Deterministic aggregation over all prediction_events.

    Produces a single decision window.
    Read-only computation.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            MIN(created_at),
            MAX(created_at)
        FROM prediction_events
        """
    )
    window = cursor.fetchone()

    if not window or window[0] is None:
        conn.close()
        return {}

    window_start, window_end = window

    cursor.execute(
        """
        SELECT
            COUNT(*) AS n_total,
            SUM(CASE WHEN score < ? THEN 1 ELSE 0 END) AS n_accept,
            SUM(CASE WHEN score >= ? THEN 1 ELSE 0 END) AS n_review
        FROM prediction_events
        """,
        (threshold, threshold),
    )

    counts = cursor.fetchone()
    conn.close()

    return {
        "window_start": window_start,
        "window_end": window_end,
        "threshold": threshold,
        "n_total": counts[0],
        "n_accept": counts[1],
        "n_review": counts[2],
    }
