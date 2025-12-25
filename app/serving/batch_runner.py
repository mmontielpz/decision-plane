# app/serving/batch_runner.py

import json
from typing import Callable, Iterable, Dict, Any, List
from datetime import datetime

from app.serving.repository import PredictionRepository


class BatchPredictionRunner:
    """
    Deterministic batch inference runner.

    This runner:
    * does NOT train models
    * does NOT serve real-time requests
    * does NOT retry silently
    * persists all outcomes (success or failure)
    """

    def __init__(
        self,
        *,
        model_name: str,
        model_version: str,
        feature_version: str,
        predictor_fn: Callable[[Dict[str, Any]], float],
        threshold: float,
    ):
        """
        predictor_fn: function that receives a feature row dict
                      and returns a probability score in [0, 1]
        """
        self.model_name = model_name
        self.model_version = model_version
        self.feature_version = feature_version
        self.predictor_fn = predictor_fn
        self.threshold = threshold
        self.repo = PredictionRepository()

    def run(
        self,
        *,
        run_key: str,
        dataset_key: str,
        features: Iterable[Dict[str, Any]],
    ) -> int:
        """
        Executes batch scoring and persists predictions.

        Returns:
            prediction_run_id
        """
        features = list(features)
        run_id = None

        try:
            run_id = self.repo.get_or_create_run(
                run_key=run_key,
                model_name=self.model_name,
                model_version=self.model_version,
                feature_version=self.feature_version,
                dataset_key=dataset_key,
                dataset_rows=len(features),
                status="RUNNING",
            )

            prediction_rows: List[dict] = []

            for row in features:
                document_id = row["document_id"]
                score = float(self.predictor_fn(row))

                decision = (
                    "REVIEW" if score >= self.threshold else "ACCEPT"
                )

                prediction_rows.append(
                    {
                        "document_id": document_id,
                        "score": score,
                        "threshold": self.threshold,
                        "decision": decision,
                        "features_row_hash": row.get("features_row_hash"),
                        "metadata_json": json.dumps(
                            {
                                "scored_at": datetime.utcnow().isoformat(),
                                "model_version": self.model_version,
                            }
                        ),
                    }
                )

            self.repo.insert_predictions(
                run_id=run_id,
                predictions=prediction_rows,
            )

            self._mark_run_success(run_id)

        except Exception as exc:
            if run_id is not None:
                self._mark_run_failure(run_id, exc)
            raise

        return run_id

    # -------------------------
    # Internal helpers
    # -------------------------
    def _mark_run_success(self, run_id: int) -> None:
        self._update_run_status(run_id, status="SUCCESS")

    def _mark_run_failure(self, run_id: int, exc: Exception) -> None:
        self._update_run_status(
            run_id,
            status="FAILED",
            error_message=str(exc),
        )

    def _update_run_status(
        self,
        run_id: int,
        *,
        status: str,
        error_message: str | None = None,
    ) -> None:
        from app.db.database import get_connection

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE prediction_runs
            SET status = ?, error_message = ?
            WHERE id = ?
            """,
            (status, error_message, run_id),
        )

        conn.commit()
        conn.close()
