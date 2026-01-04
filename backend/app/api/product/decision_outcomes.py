from fastapi import APIRouter, HTTPException, Query

from app.serving.decision_outcomes_repository import (
    list_decision_outcomes_v1,
    get_decision_outcome_v1,
)

router = APIRouter(
    prefix="/decision-outcomes",
    tags=["decision-outcomes"],
)


@router.get("")
def list_decision_outcomes():
    """
    V1 read-only decision outcomes list.

    Returns persisted, windowed outcomes only.
    """
    outcomes = list_decision_outcomes_v1()

    if not outcomes:
        raise HTTPException(
            status_code=404,
            detail="Decision outcomes not available",
        )

    return {"outcomes": outcomes}


@router.get("/detail")
def get_decision_outcome_detail(
    window_start: str,
    window_end: str,
    model_version: str,
    feature_version: str,
    threshold: float,
):
    """
    V1 read-only decision outcome detail.

    Identifies an exact persisted window.
    """
    outcome = get_decision_outcome_v1(
        window_start=window_start,
        window_end=window_end,
        model_version=model_version,
        feature_version=feature_version,
        threshold=threshold,
    )

    if not outcome:
        raise HTTPException(
            status_code=404,
            detail="Decision outcome not found",
        )

    return outcome
