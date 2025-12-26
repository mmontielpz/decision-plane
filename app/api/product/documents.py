# app/api/product/documents.py

from fastapi import APIRouter
from app.adapters.document_adapter import DocumentAdapter

router = APIRouter(prefix="/api/documents", tags=["product-documents"])


@router.get("")
def list_documents():
    adapter = DocumentAdapter()
    return adapter.list_documents()
