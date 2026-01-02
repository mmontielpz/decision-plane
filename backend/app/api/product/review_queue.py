from fastapi import APIRouter
from app.adapters.review_queue_adapter import ReviewQueueAdapter

router = APIRouter(
    prefix="/review-queue",
    tags=["review-queue"],
)


@router.get("")
def list_review_queue():
    """
    Read-only endpoint exposing the review queue.

    This endpoint delegates all decision logic to the core triage system
    and returns a UI-ready read model.
    """
    adapter = ReviewQueueAdapter()
    return adapter.list_review_queue()
