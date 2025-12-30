# tests/test_batch_runner.py

import pytest

from app.serving.batch_runner import BatchPredictionRunner
from app.serving.repository import PredictionRepository


def dummy_predictor(row):
    """
    Deterministic fake model:
    score = normalized length of document_id
    """
    return min(len(row["document_id"]) / 10.0, 1.0)


def test_batch_runner_success(clean_state):
    runner = BatchPredictionRunner(
        model_name="baseline_logreg",
        model_version="v1",
        feature_version="fv1",
        predictor_fn=dummy_predictor,
        threshold=0.5,
    )

    features = [
        {"document_id": "doc-12345"},
        {"document_id": "d1"},
    ]

    run_id = runner.run(
        run_key="batch-success",
        dataset_key="features/test",
        features=features,
    )

    repo = PredictionRepository()
    rows = repo.list_predictions_for_run(run_id)

    assert len(rows) == 2

    assert rows[0]["document_id"] == "doc-12345"
    assert rows[0]["decision"] == "REVIEW"   # score = 0.9

    assert rows[1]["document_id"] == "d1"
    assert rows[1]["decision"] == "ACCEPT"   # score = 0.2


def test_batch_runner_failure_is_recorded(clean_state):
    def exploding_predictor(_):
        raise RuntimeError("model exploded")

    runner = BatchPredictionRunner(
        model_name="baseline_logreg",
        model_version="v1",
        feature_version="fv1",
        predictor_fn=exploding_predictor,
        threshold=0.5,
    )

    with pytest.raises(RuntimeError):
        runner.run(
            run_key="batch-failure",
            dataset_key="features/test",
            features=[{"document_id": "doc-1"}],
        )

    # Validate run is persisted as FAILED
    conn = runner.repo.repo = None  # explicit: no repository shortcut
    from app.db.database import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status, error_message
        FROM prediction_runs
        WHERE run_key = ?
        """,
        ("batch-failure",),
    )

    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "FAILED"
    assert "model exploded" in row[1]
