import uuid
from pathlib import Path
from datetime import datetime

from app.db.database import get_connection
from app.processing.schemas import ProcessedRecord, FeatureRecord

PROCESSOR_VERSION = "0.2.0"
FEATURE_VERSION = "v1"

def _emit_processing_step(
    *,
    run_id: str,
    document_id: str,
    step_name: str,
    status: str,
    metadata: dict | None = None,
    error_message: str | None = None,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO processing_steps (
            run_id,
            document_id,
            step_name,
            status,
            metadata_json,
            error_message,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            document_id,
            step_name,
            status,
            json.dumps(metadata) if metadata else None,
            error_message,
            datetime.utcnow().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


def _create_processing_run() -> str:
    run_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO processing_runs (
            run_id,
            started_at,
            processor_version,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        (run_id, now, PROCESSOR_VERSION, "running"),
    )

    conn.commit()
    conn.close()

    return run_id


def _complete_processing_run(run_id: str, status: str):
    now = datetime.utcnow().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE processing_runs
        SET completed_at = ?, status = ?
        WHERE run_id = ?
        """,
        (now, status, run_id),
    )

    conn.commit()
    conn.close()


def _fetch_unprocessed_documents(limit: int = 1):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT document_id, ingestion_timestamp, source_system
        FROM ingestion_events
        WHERE document_id NOT IN (
            SELECT document_id FROM document_processing_status
        )
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def _update_document_status(
    document_id: str,
    run_id: str,
    status: str,
    processed_path: str = None,
    feature_path: str = None,
    error_code: str = None,
    error_message: str = None,
):
    now = datetime.utcnow().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO document_processing_status (
            document_id,
            last_run_id,
            status,
            processed_path,
            feature_path,
            error_code,
            error_message,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(document_id) DO UPDATE SET
            last_run_id = excluded.last_run_id,
            status = excluded.status,
            processed_path = excluded.processed_path,
            feature_path = excluded.feature_path,
            error_code = excluded.error_code,
            error_message = excluded.error_message,
            updated_at = excluded.updated_at
        """,
        (
            document_id,
            run_id,
            status,
            processed_path,
            feature_path,
            error_code,
            error_message,
            now,
        ),
    )

    conn.commit()
    conn.close()


def _read_raw_text(raw_path: Path) -> str:
    return raw_path.read_text(encoding="utf-8")


def _build_features(text: str) -> dict:
    return {
        "char_count": float(len(text)),
        "token_count": float(len(text.split())),
        "line_count": float(len(text.splitlines())),
    }


def run_batch(limit: int = 1):
    run_id = _create_processing_run()
    run_status = "completed"

    try:
        documents = _fetch_unprocessed_documents(limit=limit)

        for document_id, ingestion_ts, source_system in documents:
            try:
                raw_path = (
                    Path("data/raw")
                    / ingestion_ts.split("T")[0]
                    / source_system
                    / document_id
                )

                raw_files = list(raw_path.glob("*"))
                if not raw_files:
                    raise FileNotFoundError("Raw file not found")

                raw_file = raw_files[0]
                text = _read_raw_text(raw_file)

                _emit_processing_step(
                    run_id=run_id,
                    document_id=document_id,
                    step_name="read_raw_text",
                    status="success",
                    metadata={"path": str(raw_file)},
                )

                processed_record = ProcessedRecord(
                    document_id=document_id,
                    ingestion_timestamp=datetime.fromisoformat(ingestion_ts),
                    source_system=source_system,
                    processing_timestamp=datetime.utcnow(),
                    processor_version=PROCESSOR_VERSION,
                    extraction_method="plain_text",
                    normalized_text=text,
                    raw_path=str(raw_file),
                )

                _emit_processing_step(
                    run_id=run_id,
                    document_id=document_id,
                    step_name="write_processed_record",
                    status="success",
                    metadata={"processed_path": str(processed_path)},
                )

                processed_dir = (
                    Path("data/processed")
                    / ingestion_ts.split("T")[0]
                    / source_system
                    / document_id
                )
                processed_dir.mkdir(parents=True, exist_ok=True)

                processed_path = processed_dir / "processed.json"
                processed_path.write_text(processed_record.model_dump_json())

                features = _build_features(text)

                feature_record = FeatureRecord(
                    document_id=document_id,
                    feature_timestamp=datetime.utcnow(),
                    feature_version=FEATURE_VERSION,
                    features=features,
                    processed_path=str(processed_path),
                )

                feature_dir = (
                    Path("data/features")
                    / FEATURE_VERSION
                    / ingestion_ts.split("T")[0]
                    / source_system
                )
                feature_dir.mkdir(parents=True, exist_ok=True)

                feature_path = feature_dir / f"{document_id}.json"
                feature_path.write_text(feature_record.model_dump_json())

                _update_document_status(
                    document_id=document_id,
                    run_id=run_id,
                    status="processed",
                    processed_path=str(processed_path),
                    feature_path=str(feature_path),
                )

            except Exception as e:
                run_status = "partial"
                _update_document_status(
                    document_id=document_id,
                    run_id=run_id,
                    status="failed",
                    error_code="PROCESSING_ERROR",
                    error_message=str(e),
                )

    except Exception:
        run_status = "failed"
        raise

    finally:
        _complete_processing_run(run_id, run_status)
