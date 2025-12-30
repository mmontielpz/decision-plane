# tests/test_replay_runner.py

from app.replay.runner import ReplayRunner
from app.serving.repository import PredictionRepository


def test_replay_runner_changes_decisions(clean_state):
    repo = PredictionRepository()

    run_id = repo.get_or_create_run(
        run_key="replay-test",
        model_name="baseline_logreg",
        model_version="v1",
        feature_version="fv1",
        dataset_key="features/test",
        dataset_rows=2,
    )

    repo.insert_predictions(
        run_id=run_id,
        predictions=[
            {
                "document_id": "doc-1",
                "score": 0.7,
                "threshold": 0.6,
                "decision": "REVIEW",
            },
            {
                "document_id": "doc-2",
                "score": 0.4,
                "threshold": 0.6,
                "decision": "ACCEPT",
            },
        ],
    )

    runner = ReplayRunner(new_threshold=0.5)
    results = runner.replay_run(run_id=run_id)

    assert len(results) == 2

    assert results[0]["old_decision"] == "REVIEW"
    assert results[0]["new_decision"] == "REVIEW"
    assert results[0]["changed"] is False

    assert results[1]["old_decision"] == "ACCEPT"
    assert results[1]["new_decision"] == "ACCEPT"
    assert results[1]["changed"] is False
