from fastapi import APIRouter, HTTPException

from app.api.contracts.document_replay_v1 import DocumentReplayV1

router = APIRouter(
    prefix="/documents",
    tags=["product-replay"],
)


@router.get(
    "/{document_id}/replay",
    response_model=DocumentReplayV1,
)
def replay_document(document_id: str):
    """
    V1 replay endpoint (stub).

    Contract exists.
    Behavior intentionally not implemented.
    """
    raise HTTPException(
        status_code=404,
        detail="Replay not available for this document",
    )
