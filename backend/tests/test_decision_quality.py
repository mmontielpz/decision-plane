# tests/test_decision_quality.py

from app.monitoring.decision_quality import (
    compute_confusion_counts,
    compute_total_cost,
    decision_quality_summary,
)


def test_confusion_counts_with_review():
    decisions = [
        "ACCEPT",   # negative
        "REJECT",   # positive
        "REVIEW",   # abstain
        "ACCEPT",   # negative
        "REJECT",   # negative -> FP
    ]

    labels = [
        "NEGATIVE",
        "POSITIVE",
        "POSITIVE",
        "NEGATIVE",
        "NEGATIVE",
    ]

    counts = compute_confusion_counts(
        decisions=decisions,
        labels=labels,
        positive_label="POSITIVE",
        decision_accept="ACCEPT",
        decision_review="REVIEW",
    )

    assert counts["tp"] == 1
    assert counts["fp"] == 1
    assert counts["tn"] == 2
    assert counts["fn"] == 0
    assert counts["review"] == 1


def test_total_cost_computation():
    cost = compute_total_cost(
        tp=1,
        fp=2,
        tn=5,
        fn=3,
        review=4,
        cost_fp=10.0,
        cost_fn=50.0,
        cost_review=5.0,
    )

    # 2*10 + 3*50 + 4*5 = 20 + 150 + 20 = 190
    assert cost == 190.0


def test_decision_quality_summary_end_to_end():
    decisions = [
        "ACCEPT",
        "REJECT",
        "REVIEW",
        "REJECT",
    ]

    labels = [
        "NEGATIVE",
        "POSITIVE",
        "POSITIVE",
        "NEGATIVE",
    ]

    costs = {
        "cost_fp": 10.0,
        "cost_fn": 100.0,
        "cost_review": 5.0,
    }

    summary = decision_quality_summary(
        decisions=decisions,
        labels=labels,
        costs=costs,
    )

    assert summary["tp"] == 1
    assert summary["fp"] == 1
    assert summary["tn"] == 1
    assert summary["fn"] == 0
    assert summary["review"] == 1

    # cost = 1*10 + 0*100 + 1*5 = 15
    assert summary["total_cost"] == 15.0
