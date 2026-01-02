# app/monitoring/decision_quality.py

from typing import Iterable, Dict


def compute_confusion_counts(
    *,
    decisions: Iterable[str],
    labels: Iterable[str],
    positive_label: str = "POSITIVE",
    decision_accept: str = "ACCEPT",
    decision_review: str = "REVIEW",
) -> Dict[str, int]:
    """
    Computes confusion counts given decisions and ground-truth labels.

    Assumptions:
    * labels correspond positionally to decisions
    * REVIEW decisions are treated as abstentions (not positive predictions)
    """
    tp = fp = tn = fn = review = 0

    for decision, label in zip(decisions, labels):
        if decision == decision_review:
            review += 1
            continue

        if decision == decision_accept:
            if label == positive_label:
                fn += 1
            else:
                tn += 1
        else:
            # implicit reject / positive decision
            if label == positive_label:
                tp += 1
            else:
                fp += 1

    return {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "review": review,
    }


def compute_total_cost(
    *,
    tp: int,
    fp: int,
    tn: int,
    fn: int,
    review: int,
    cost_fp: float,
    cost_fn: float,
    cost_review: float,
) -> float:
    """
    Computes total decision cost using asymmetric costs.
    """
    return (
        fp * cost_fp
        + fn * cost_fn
        + review * cost_review
    )


def decision_quality_summary(
    *,
    decisions: Iterable[str],
    labels: Iterable[str],
    costs: Dict[str, float],
) -> Dict[str, float]:
    """
    High-level wrapper that returns confusion counts and total cost.

    costs must contain:
        cost_fp
        cost_fn
        cost_review
    """
    counts = compute_confusion_counts(
        decisions=decisions,
        labels=labels,
    )

    total_cost = compute_total_cost(
        tp=counts["tp"],
        fp=counts["fp"],
        tn=counts["tn"],
        fn=counts["fn"],
        review=counts["review"],
        cost_fp=costs["cost_fp"],
        cost_fn=costs["cost_fn"],
        cost_review=costs["cost_review"],
    )

    return {
        "tp": counts["tp"],
        "fp": counts["fp"],
        "tn": counts["tn"],
        "fn": counts["fn"],
        "review": counts["review"],
        "total_cost": total_cost,
    }
