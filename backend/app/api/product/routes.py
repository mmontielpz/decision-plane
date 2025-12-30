from fastapi import APIRouter, HTTPException
from app.adapters.document_adapter import DocumentAdapter

router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.get("/{document_id}")
def get_document_detail(document_id: str):
    adapter = DocumentAdapter()
    doc = adapter.get_document_by_id(document_id)

    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc
