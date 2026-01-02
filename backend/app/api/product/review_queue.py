from fastapi import APIRouter
from app.adapters.review_queue_adapter import ReviewQueueAdapter

router = APIRouter(
    prefix="/review-queue",
    tags=["review-queue"],
)


@router.get("")
def list_review_queue():
    """
    Read-only endpoint exposing the review queue (v1).

    Scope:
    - Finance / Accounts Payable
    - PDFs digitales
    - invoice | unknown
    - confidence threshold >= 0.80
    """
    adapter = ReviewQueueAdapter()
    return adapter.list_review_queue()
