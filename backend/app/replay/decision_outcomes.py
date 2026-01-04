from typing import Dict, List
from app.db.database import get_connection


def replay_decision_outcomes(
    *,
    run_id: int,
    new_threshold: float,
) -> List[Dict]:
    """
    Deterministic replay of decision outcomes.

    Guarantees:
    - Read-only
    - No DB mutation
    - Recomputes decisions only
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            document_id,
            score,
            threshold,
            decision
        FROM prediction_events
        WHERE run_id = ?
        ORDER BY id ASC
        """,
        (run_id,),
    )

    rows = cursor.fetchall()
    conn.close()

    results = []
    for document_id, score, old_threshold, old_decision in rows:
        new_decision = (
            "REVIEW" if score >= new_threshold else "ACCEPT"
        )

        results.append(
            {
                "document_id": document_id,
                "score": score,
                "old_threshold": old_threshold,
                "old_decision": old_decision,
                "new_threshold": new_threshold,
                "new_decision": new_decision,
                "changed": old_decision != new_decision,
            }
        )

    return results
