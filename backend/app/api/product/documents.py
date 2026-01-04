# app/api/product/documents.py

from fastapi import APIRouter, HTTPException
from app.adapters.document_adapter import DocumentAdapter
from app.api.contracts.document_detail_v1 import DocumentDetailV1

router = APIRouter(prefix="/documents", tags=["product-documents"])


@router.get("")
def list_documents():
    adapter = DocumentAdapter()
    return adapter.list_documents()


@router.get("/{document_id}", response_model=DocumentDetailV1)
def get_document_detail(document_id: str):
    adapter = DocumentAdapter()
    doc = adapter.get_document_by_id(document_id)

    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc

@router.get("/{document_id}/replay")
def get_document_replay(document_id: str):
    """
    Document replay endpoint (v1).

    Contract:
    - Endpoint exists
    - Replay is intentionally unavailable in v1
    - Must return controlled 404 with explicit reason
    """
    raise HTTPException(
        status_code=404,
        detail="Replay not available for this document",
    )
