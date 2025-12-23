from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.ingestion.schemas import IngestionRequest
from app.db.database import get_connection
from app.core.logger import get_logger
from pathlib import Path
import json
import shutil
import sqlite3

router = APIRouter()
logger = get_logger("ingestion")


@router.post("/ingest", status_code=status.HTTP_200_OK)
async def ingest_document(
    metadata: str = Form(...),
    file: UploadFile = File(...)
):
    # Parse and validate metadata
    try:
        metadata_obj = IngestionRequest.model_validate(json.loads(metadata))
    except Exception as e:
        logger.warning(
            "metadata_validation_failed",
            extra={"extra": {"error": str(e)}},
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid metadata payload",
        )

    # Persist metadata (idempotent)
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

    except Exception as e:
        conn.close()
        logger.error(
            "ingestion_db_error",
            extra={"extra": {"error": str(e)}},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist ingestion metadata",
        )

    finally:
        conn.close()

    # Raw storage (only on first ingestion)
    ingestion_date = metadata_obj.ingestion_timestamp.date().isoformat()
    source = metadata_obj.source_system or "unknown"

    raw_base = Path("data/raw")
    target_dir = raw_base / ingestion_date / source / metadata_obj.document_id
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / file.filename

    if inserted:
        try:
            if not target_file.exists():
                with target_file.open("wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            logger.error(
                "raw_storage_write_failed",
                extra={"extra": {"path": str(target_file), "error": str(e)}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to write raw file",
            )

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

    # Duplicate case
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={
            "document_id": metadata_obj.document_id,
            "status": "already_exists",
        },
    )
