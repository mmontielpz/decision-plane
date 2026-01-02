# app/replay/runner.py

from typing import Dict, List
from app.db.database import get_connection


class ReplayRunner:
    """
    Replays historical predictions with a new decision rule.

    Guarantees:
    * Does NOT modify existing predictions
    * Deterministic output
    * Purely analytical (no side effects)
    """

    def __init__(self, *, new_threshold: float):
        self.new_threshold = new_threshold

    def replay_run(self, *, run_id: int) -> List[Dict]:
        """
        Recompute decisions for a given prediction run using a new threshold.
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
        for r in rows:
            document_id, score, old_threshold, old_decision = r
            new_decision = (
                "REVIEW" if score >= self.new_threshold else "ACCEPT"
            )

            results.append(
                {
                    "document_id": document_id,
                    "score": score,
                    "old_threshold": old_threshold,
                    "old_decision": old_decision,
                    "new_threshold": self.new_threshold,
                    "new_decision": new_decision,
                    "changed": old_decision != new_decision,
                }
            )

        return results
