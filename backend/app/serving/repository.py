# app/serving/repository.py

from datetime import datetime
from typing import Iterable, Optional

from app.db.database import get_connection
from app.core.models.document import Prediction


class PredictionRepository:
    """
    Persistence layer for Phase 4 (Serving & Monitoring).

    Guarantees:
    * Idempotent prediction runs via run_key
    * Append-only prediction events
    * Explicit failure on duplicate (run_id, document_id)
    """

    # -------------------------
    # Prediction runs
    # -------------------------
    def get_or_create_run(
        self,
        *,
        run_key: str,
        model_name: str,
        model_version: str,
        feature_version: str,
        dataset_key: str,
        dataset_rows: Optional[int],
        status: str = "SUCCESS",
        error_message: Optional[str] = None,
        context_json: Optional[str] = None,
    ) -> int:
        """
        Returns prediction_runs.id
        Idempotent by run_key.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id FROM prediction_runs
            WHERE run_key = ?
            """,
            (run_key,),
        )
        row = cursor.fetchone()
        if row:
            conn.close()
            return row[0]

        cursor.execute(
            """
            INSERT INTO prediction_runs (
                run_key,
                created_at,
                model_name,
                model_version,
                feature_version,
                dataset_key,
                dataset_rows,
                status,
                error_message,
                context_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_key,
                datetime.utcnow().isoformat(),
                model_name,
                model_version,
                feature_version,
                dataset_key,
                dataset_rows,
                status,
                error_message,
                context_json,
            ),
        )

        run_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return run_id

    # -------------------------
    # Prediction events
    # -------------------------
    def insert_predictions(
        self,
        *,
        run_id: int,
        predictions: Iterable[dict],
    ) -> int:
        """
        Inserts prediction events.

        Each prediction dict must contain:
            document_id
            score
            threshold
            decision

        Optional:
            features_row_hash
            metadata_json

        Fails atomically on duplicate (run_id, document_id).
        """
        conn = get_connection()
        cursor = conn.cursor()

        rows = []
        now = datetime.utcnow().isoformat()

        for p in predictions:
            rows.append(
                (
                    now,
                    run_id,
                    p["document_id"],
                    p["score"],
                    p["threshold"],
                    p["decision"],
                    p.get("features_row_hash"),
                    p.get("metadata_json"),
                )
            )

        try:
            cursor.executemany(
                """
                INSERT INTO prediction_events (
                    created_at,
                    run_id,
                    document_id,
                    score,
                    threshold,
                    decision,
                    features_row_hash,
                    metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )
            conn.commit()
        except Exception:
            conn.rollback()
            conn.close()
            raise

        inserted = cursor.rowcount
        conn.close()
        return inserted

    # -------------------------
    # Reads (auditable, deterministic)
    # -------------------------
    def list_predictions_for_run(self, run_id: int) -> list[dict]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                document_id,
                score,
                threshold,
                decision,
                features_row_hash,
                metadata_json,
                created_at
            FROM prediction_events
            WHERE run_id = ?
            ORDER BY id ASC
            """,
            (run_id,),
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "document_id": r[0],
                "score": r[1],
                "threshold": r[2],
                "decision": r[3],
                "features_row_hash": r[4],
                "metadata_json": r[5],
                "created_at": r[6],
            }
            for r in rows
        ]

    def get_latest_prediction(self, document_id: str) -> Prediction | None:
        """
        Returns the most recent prediction event for a document, mapped to the core Prediction model.
        No triage logic. No thresholds. Pure read+mapping.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                pe.decision,
                pe.score,
                pr.model_version
            FROM prediction_events pe
            JOIN prediction_runs pr
                ON pr.id = pe.run_id
            WHERE pe.document_id = ?
            ORDER BY pe.created_at DESC, pe.id DESC
            LIMIT 1
            """,
            (document_id,),
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        decision, score, model_version = row

        return Prediction(
            label=decision,
            confidence=score,
            model_version=model_version,
        )
