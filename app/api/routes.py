from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.ingestion.schemas import IngestionRequest
from app.db.database import get_connection
from app.core.logger import get_logger
from pathlib import Path
from datetime import datetime
import json
import shutil
import sqlite3

router = APIRouter()
logger = get_logger("ingestion")


@router.post("/ingest")
async def ingest_document(
    metadata: str = Form(...),
    file: UploadFile = File(...)
):
    metadata_obj = IngestionRequest.model_validate(json.loads(metadata))

    conn = get_connection()
    cursor = conn.cursor()

    try:
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
        inserted = True

    except sqlite3.IntegrityError:
        inserted = False
        logger.info(
            "ingestion_duplicate",
            extra={"extra": {"document_id": metadata_obj.document_id}},
        )

    finally:
        conn.close()

    # Raw storage (only if first ingestion)
    ingestion_date = metadata_obj.ingestion_timestamp.date().isoformat()
    source = metadata_obj.source_system or "unknown"

    raw_base = Path("data/raw")
    target_dir = raw_base / ingestion_date / source / metadata_obj.document_id
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / file.filename

    if inserted:
        if target_file.exists():
            logger.warning(
                "raw_file_exists",
                extra={"extra": {"path": str(target_file)}},
            )
        else:
            with target_file.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        status = "received"

    else:
        status = "already_exists"

    logger.info(
        "ingestion_result",
        extra={
            "extra": {
                "document_id": metadata_obj.document_id,
                "status": status,
                "raw_path": str(target_file),
            }
        },
    )

    return {
        "document_id": metadata_obj.document_id,
        "status": status,
        "raw_path": str(target_file),
    }
