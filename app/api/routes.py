from fastapi import APIRouter, UploadFile, File, Form
from app.ingestion.schemas import IngestionRequest
from app.db.database import get_connection
from app.core.logger import get_logger
from pathlib import Path
from datetime import datetime
import json
import shutil

router = APIRouter()
logger = get_logger("ingestion")


@router.post("/ingest")
async def ingest_document(
    metadata: str = Form(...),
    file: UploadFile = File(...)
):
    logger.info(
        "ingestion_started",
        extra={"extra": {"filename": file.filename}},
    )

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

    ingestion_date = metadata_obj.ingestion_timestamp.date().isoformat()
    source = metadata_obj.source_system or "unknown"

    raw_base = Path("data/raw")
    target_dir = raw_base / ingestion_date / source / metadata_obj.document_id
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / file.filename
    with target_file.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.info(
        "ingestion_completed",
        extra={
            "extra": {
                "document_id": metadata_obj.document_id,
                "raw_path": str(target_file),
            }
        },
    )

    return {
        "document_id": metadata_obj.document_id,
        "status": "received",
        "raw_path": str(target_file),
    }
