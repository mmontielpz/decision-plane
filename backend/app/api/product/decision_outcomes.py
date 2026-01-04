from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/decision-outcomes", tags=["decision-outcomes"])


@router.get("")
def list_decision_outcomes():
    """
    Decision outcomes (v1).

    Intentionally unimplemented.
    Contract-only endpoint.
    """
    raise HTTPException(
        status_code=404,
        detail="Decision outcomes not available",
    )
