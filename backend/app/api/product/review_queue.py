from fastapi import APIRouter
from typing import List

from app.adapters.review_queue_adapter import ReviewQueueAdapter
from app.api.contracts.review_queue_v1 import ReviewQueueItemV1

router = APIRouter(
    prefix="/review-queue",
    tags=["review-queue"],
)


@router.get("", response_model=List[ReviewQueueItemV1])
def list_review_queue():
    """
    Read-only endpoint exposing the review queue.

    This endpoint delegates all decision logic to the core triage system
    and returns a UI-ready read model.
    """
    adapter = ReviewQueueAdapter()
    return adapter.list_review_queue()
