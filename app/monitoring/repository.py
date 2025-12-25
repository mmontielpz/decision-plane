# app/monitoring/repository.py

from datetime import datetime
from typing import Optional, Dict

from app.db.database import get_connection


class DecisionOutcomeRepository:
    """
    Persistence layer for decision quality outcomes.

    Guarantees:
    * Idempotent writes per (window, model, feature, threshold, cost_version)
    * Append-only semantics
    * Deterministic reads
    """

    def upsert_decision_outcome(
        self,
        *,
        window_start: str,
        window_end: str,
        model_version: str,
        feature_version: str,
        threshold: float,
        cost_version: int,
        n_total: int,
        n_accept: int,
        n_review: int,
        n_labeled: int,
        tp: int,
        fp: int,
        tn: int,
        fn: int,
        total_cost: float,
        reference_notes: Optional[str] = None,
    ) -> None:
        """
        Inserts a decision outcome row.

        If the unique key already exists, the write is ignored.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO decision_outcomes (
                created_at,
                window_start,
                window_end,
                model_version,
                feature_version,
                threshold,
                cost_version,
                n_total,
                n_accept,
                n_review,
                n_labeled,
                tp,
                fp,
                tn,
                fn,
                total_cost,
                reference_notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                window_start,
                window_end,
                model_version,
                feature_version,
                threshold,
                cost_version,
                n_total,
                n_accept,
                n_review,
                n_labeled,
                tp,
                fp,
                tn,
                fn,
                total_cost,
                reference_notes,
            ),
        )

        conn.commit()
        conn.close()

    def list_outcomes_by_window(
        self,
        *,
        window_start: str,
        window_end: str,
    ) -> list[Dict]:
        """
        Deterministic read of decision outcomes for a window.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                model_version,
                feature_version,
                threshold,
                cost_version,
                n_total,
                n_accept,
                n_review,
                n_labeled,
                tp,
                fp,
                tn,
                fn,
                total_cost,
                created_at,
                reference_notes
            FROM decision_outcomes
            WHERE window_start = ?
              AND window_end = ?
            ORDER BY created_at ASC
            """,
            (window_start, window_end),
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "model_version": r[0],
                "feature_version": r[1],
                "threshold": r[2],
                "cost_version": r[3],
                "n_total": r[4],
                "n_accept": r[5],
                "n_review": r[6],
                "n_labeled": r[7],
                "tp": r[8],
                "fp": r[9],
                "tn": r[10],
                "fn": r[11],
                "total_cost": r[12],
                "created_at": r[13],
                "reference_notes": r[14],
            }
            for r in rows
        ]
