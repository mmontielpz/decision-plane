from fastapi import APIRouter, Query
from typing import List

from app.api.contracts.replay_run_v1 import ReplayDecisionV1
from app.serving.replay_repository import get_replay_for_run

router = APIRouter(prefix="/replay", tags=["replay"])


@router.get(
    "/run/{run_id}",
    response_model=List[ReplayDecisionV1],
)
def replay_prediction_run(
    run_id: int,
    threshold: float = Query(..., gt=0.0, lt=1.0),
):
    return get_replay_for_run(
        run_id=run_id,
        new_threshold=threshold,
    )
