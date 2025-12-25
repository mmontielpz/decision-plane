# tests/test_prediction_repository.py

import pytest
from app.db.database import get_connection
from app.serving.repository import PredictionRepository


def test_prediction_run_is_idempotent(clean_state):
    repo = PredictionRepository()

    run_id_1 = repo.get_or_create_run(
        run_key="run-abc",
        model_name="baseline_logreg",
        model_version="v1",
        feature_version="fv1",
        dataset_key="features/2025-12-24",
        dataset_rows=10,
    )

    run_id_2 = repo.get_or_create_run(
        run_key="run-abc",
        model_name="baseline_logreg",
        model_version="v1",
        feature_version="fv1",
        dataset_key="features/2025-12-24",
        dataset_rows=10,
    )

    assert run_id_1 == run_id_2


def test_insert_and_read_predictions(clean_state):
    repo = PredictionRepository()

    run_id = repo.get_or_create_run(
        run_key="run-preds",
        model_name="baseline_logreg",
        model_version="v1",
        feature_version="fv1",
        dataset_key="features/2025-12-24",
        dataset_rows=2,
    )

    inserted = repo.insert_predictions(
        run_id=run_id,
        predictions=[
            {
                "document_id": "doc-1",
                "score": 0.82,
                "threshold": 0.6,
                "decision": "REVIEW",
            },
            {
                "document_id": "doc-2",
                "score": 0.12,
                "threshold": 0.6,
                "decision": "ACCEPT",
            },
        ],
    )

    assert inserted == 2

    rows = repo.list_predictions_for_run(run_id)
    assert len(rows) == 2

    assert rows[0]["document_id"] == "doc-1"
    assert rows[0]["decision"] == "REVIEW"
    assert rows[1]["document_id"] == "doc-2"
    assert rows[1]["decision"] == "ACCEPT"


def test_duplicate_document_in_same_run_fails(clean_state):
    repo = PredictionRepository()

    run_id = repo.get_or_create_run(
        run_key="run-dup",
        model_name="baseline_logreg",
        model_version="v1",
        feature_version="fv1",
        dataset_key="features/2025-12-24",
        dataset_rows=1,
    )

    repo.insert_predictions(
        run_id=run_id,
        predictions=[
            {
                "document_id": "doc-1",
                "score": 0.7,
                "threshold": 0.6,
                "decision": "REVIEW",
            }
        ],
    )

    with pytest.raises(Exception):
        repo.insert_predictions(
            run_id=run_id,
            predictions=[
                {
                    "document_id": "doc-1",
                    "score": 0.9,
                    "threshold": 0.6,
                    "decision": "REVIEW",
                }
            ],
        )
