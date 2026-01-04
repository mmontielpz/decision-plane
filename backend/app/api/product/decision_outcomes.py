from fastapi import APIRouter, HTTPException
from app.serving.decision_outcomes_repository import list_decision_outcomes

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
