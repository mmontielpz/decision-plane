from fastapi import APIRouter, UploadFile, File, Form
from app.ingestion.schemas import IngestionRequest
from app.db.database import get_connection
import json

router = APIRouter()


@router.post("/ingest")
async def ingest_document(
    metadata: str = Form(...),
    file: UploadFile = File(...)
):
    # Parse metadata JSON string into Pydantic model
    metadata_obj = IngestionRequest.model_validate(json.loads(metadata))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ingestion_events (
            document_id,
            ingestion_timestamp,
            source_system,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            metadata_obj.document_id,
            metadata_obj.ingestion_timestamp.isoformat(),
            metadata_obj.source_system,
            "received",
        ),
    )

    conn.commit()
    conn.close()

    return {
        "document_id": metadata_obj.document_id,
        "status": "received"
    }
