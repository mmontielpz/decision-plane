# tests/test_evaluation_window_repository.py

from app.monitoring.repository import EvaluationWindowRepository


def test_insert_and_read_evaluation_window(clean_state):
    repo = EvaluationWindowRepository()

    repo.insert_evaluation_window(
        window_start="2025-01-01",
        window_end="2025-01-31",
        model_version="v1",
        feature_version="fv1",
        evaluation_config_version="eval_v1",
        n_total=100,
        tp=30,
        fp=10,
        tn=35,
        fn=5,
        derived_metrics={
            "precision": 0.75,
            "recall": 0.86,
        },
        reference_notes="baseline month",
    )

    rows = repo.list_windows_by_range(
        window_start="2025-01-01",
        window_end="2025-01-31",
    )

    assert len(rows) == 1

    row = rows[0]
    assert row["model_version"] == "v1"
    assert row["feature_version"] == "fv1"
    assert row["evaluation_config_version"] == "eval_v1"
    assert row["n_total"] == 100
    assert row["tp"] == 30
    assert row["fp"] == 10
    assert row["tn"] == 35
    assert row["fn"] == 5
    assert "precision" in row["derived_metrics"]
    assert row["reference_notes"] == "baseline month"


def test_evaluation_windows_are_not_upserted(clean_state):
    repo = EvaluationWindowRepository()

    repo.insert_evaluation_window(
        window_start="2025-02-01",
        window_end="2025-02-28",
        model_version="v1",
        feature_version="fv1",
        evaluation_config_version="eval_v1",
        n_total=50,
        tp=15,
        fp=5,
        tn=20,
        fn=10,
        derived_metrics={},
        reference_notes=None,
    )

    repo.insert_evaluation_window(
        window_start="2025-02-01",
        window_end="2025-02-28",
        model_version="v1",
        feature_version="fv1",
        evaluation_config_version="eval_v2",
        n_total=50,
        tp=14,
        fp=6,
        tn=19,
        fn=11,
        derived_metrics={},
        reference_notes=None,
    )

    rows = repo.list_windows_by_range(
        window_start="2025-02-01",
        window_end="2025-02-28",
    )

    assert len(rows) == 2
