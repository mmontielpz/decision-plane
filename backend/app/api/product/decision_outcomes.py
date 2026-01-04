from fastapi import APIRouter, HTTPException, Query
from app.serving.decision_outcomes_repository import (
        list_decision_outcomes,
        compute_decision_outcomes_single_window,
)


router = APIRouter(prefix="/decision-outcomes", tags=["decision-outcomes"])


@router.get("")
def list_decision_outcomes_v1():
    outcomes = list_decision_outcomes()

    if not outcomes:
        raise HTTPException(
            status_code=404,
            detail="Decision outcomes not available",
        )

    return {"outcomes": outcomes}


@router.get("/aggregate")
def aggregate_decision_outcomes_v1(
    threshold: float = Query(..., gt=0.0, lt=1.0)
):
    outcome = compute_decision_outcomes_single_window(
        threshold=threshold
    )

    if not outcome:
        raise HTTPException(
            status_code=404,
            detail="Decision outcomes not available",
        )

    return outcome
