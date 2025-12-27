from pathlib import Path
import json
from typing import List, Dict, Any
from datetime import datetime

from app.db.database import get_connection
from app.serving.batch_runner import BatchPredictionRunner


def load_feature_rows(feature_version: str) -> List[Dict[str, Any]]:
    """
    Load feature rows for documents that:
    * are processed
    * have features
    * have no predictions yet
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            dps.document_id,
            dps.feature_path
        FROM document_processing_status dps
        WHERE dps.status = 'processed'
          AND dps.feature_path IS NOT NULL
          AND NOT EXISTS (
              SELECT 1
              FROM prediction_events pe
              WHERE pe.document_id = dps.document_id
          )
        """
    )

    rows = cursor.fetchall()
    conn.close()

    feature_rows: List[Dict[str, Any]] = []

    for document_id, feature_path in rows:
        path = Path(feature_path)
        data = json.loads(path.read_text())

        row = {
            "document_id": document_id,
            **data["features"],
            "features_row_hash": data.get("features_row_hash"),
        }
        feature_rows.append(row)

    return feature_rows


def run_batch_serving():
    features = load_feature_rows(feature_version="v1")

    if not features:
        return 0

    runner = BatchPredictionRunner(
        model_name="baseline_logreg",
        model_version="v1",
        feature_version="v1",
        predictor_fn=lambda row: 0.75,  # placeholder controlado
        threshold=0.6,
    )

    run_id = runner.run(
        run_key=f"batch-{datetime.utcnow().isoformat()}",
        dataset_key="features_v1",
        features=features,
    )

    return run_id
