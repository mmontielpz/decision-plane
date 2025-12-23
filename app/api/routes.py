from fastapi import APIRouter, UploadFile, File
from app.ingestion.schemas import IngestionRequest

router = APIRouter()


@router.post("/ingest")
async def ingest_document(
    metadata: IngestionRequest,
    file: UploadFile = File(...)
):
    """
    Stub endpoint for document ingestion.
    Business logic intentionally deferred.
    """
    return {
        "document_id": metadata.document_id,
        "status": "received"
    }
