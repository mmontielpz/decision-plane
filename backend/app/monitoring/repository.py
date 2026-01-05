# backend/app/monitoring/repository.py

import json
from datetime import datetime
from typing import Optional, Dict, List

from app.db.database import get_connection


class EvaluationWindowRepository:
    """
    Persistence layer for analytical evaluation windows.

    Guarantees:
    * Append-only writes
    * No policy, threshold, or decision semantics
    * Deterministic reads
    * Fully derived, non-authoritative data
    """

    def insert_evaluation_window(
        self,
        *,
        window_start: str,
        window_end: str,
        model_version: str,
        feature_version: str,
        evaluation_config_version: str,
        n_total: int,
        tp: int,
        fp: int,
        tn: int,
        fn: int,
        derived_metrics: Dict,
        reference_notes: Optional[str] = None,
    ) -> None:
        """
        Inserts a new evaluation window.

        Evaluation windows are append-only and may coexist for the same
        time range under different evaluation configurations.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO evaluation_windows (
                created_at,
                window_start,
                window_end,
                model_version,
                feature_version,
                evaluation_config_version,
                n_total,
                tp,
                fp,
                tn,
                fn,
                derived_metrics,
                reference_notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                window_start,
                window_end,
                model_version,
                feature_version,
                evaluation_config_version,
                n_total,
                tp,
                fp,
                tn,
                fn,
                json.dumps(derived_metrics),  # explicit serialization
                reference_notes,
            ),
        )

        conn.commit()
        conn.close()

    def list_windows_by_range(
        self,
        *,
        window_start: str,
        window_end: str,
    ) -> List[Dict]:
        """
        Deterministic read of evaluation windows within a time range.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                model_version,
                feature_version,
                evaluation_config_version,
                n_total,
                tp,
                fp,
                tn,
                fn,
                derived_metrics,
                created_at,
                reference_notes
            FROM evaluation_windows
            WHERE window_start >= ?
              AND window_end <= ?
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
                "evaluation_config_version": r[2],
                "n_total": r[3],
                "tp": r[4],
                "fp": r[5],
                "tn": r[6],
                "fn": r[7],
                "derived_metrics": json.loads(r[8]),  # explicit deserialization
                "created_at": r[9],
                "reference_notes": r[10],
            }
            for r in rows
        ]
