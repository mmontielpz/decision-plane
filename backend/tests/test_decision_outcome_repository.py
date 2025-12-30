# tests/test_decision_outcome_repository.py

from app.monitoring.repository import DecisionOutcomeRepository


def test_insert_and_read_decision_outcome(clean_state):
    repo = DecisionOutcomeRepository()

    repo.upsert_decision_outcome(
        window_start="2025-01-01",
        window_end="2025-01-31",
        model_version="v1",
        feature_version="fv1",
        threshold=0.6,
        cost_version=1,
        n_total=100,
        n_accept=70,
        n_review=20,
        n_labeled=80,
        tp=30,
        fp=10,
        tn=35,
        fn=5,
        total_cost=250.0,
        reference_notes="baseline month",
    )

    rows = repo.list_outcomes_by_window(
        window_start="2025-01-01",
        window_end="2025-01-31",
    )

    assert len(rows) == 1

    row = rows[0]
    assert row["model_version"] == "v1"
    assert row["feature_version"] == "fv1"
    assert row["threshold"] == 0.6
    assert row["cost_version"] == 1
    assert row["n_total"] == 100
    assert row["n_accept"] == 70
    assert row["n_review"] == 20
    assert row["n_labeled"] == 80
    assert row["tp"] == 30
    assert row["fp"] == 10
    assert row["tn"] == 35
    assert row["fn"] == 5
    assert row["total_cost"] == 250.0
    assert row["reference_notes"] == "baseline month"


def test_idempotent_upsert_does_not_duplicate(clean_state):
    repo = DecisionOutcomeRepository()

    for _ in range(2):
        repo.upsert_decision_outcome(
            window_start="2025-02-01",
            window_end="2025-02-28",
            model_version="v1",
            feature_version="fv1",
            threshold=0.5,
            cost_version=1,
            n_total=50,
            n_accept=30,
            n_review=10,
            n_labeled=40,
            tp=15,
            fp=5,
            tn=15,
            fn=5,
            total_cost=180.0,
            reference_notes=None,
        )

    rows = repo.list_outcomes_by_window(
        window_start="2025-02-01",
        window_end="2025-02-28",
    )

    assert len(rows) == 1
