"""
Development seed script for Risk-Aware ML System.

Creates a minimal, deterministic dataset:
- 1 ingestion event
- 1 processing run
- 1 document processing status
- 1 prediction run
- 1 prediction event

Safe to run multiple times after DB reset.
"""

from datetime import datetime
from app.db.models import init_db
from app.db.database import get_connection


def seed():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()

    # -------------------------
    # Phase 1: Ingestion
    # -------------------------
    cursor.execute(
        """
        INSERT OR IGNORE INTO ingestion_events (
            document_id,
            ingestion_timestamp,
            source_system,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        ("doc-001", now, "dev-seed", "received"),
    )

    # -------------------------
    # Phase 2: Processing run
    # -------------------------
    cursor.execute(
        """
        INSERT OR IGNORE INTO processing_runs (
            run_id,
            started_at,
            completed_at,
            processor_version,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "proc-run-001",
            now,
            now,
            "processor-v1",
            "SUCCESS",
            "Seed processing run",
        ),
    )

    cursor.execute(
        """
        INSERT OR REPLACE INTO document_processing_status (
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
        """,
        (
            "doc-001",
            "proc-run-001",
            "processed",
            "data/processed/dev/doc-001.json",
            "data/features/dev/doc-001.json",
            None,
            None,
            now,
        ),
    )

    # -------------------------
    # Phase 4: Prediction run
    # -------------------------
    cursor.execute(
        """
        INSERT OR IGNORE INTO prediction_runs (
            run_key,
            created_at,
            model_name,
            model_version,
            feature_version,
            dataset_key,
            dataset_rows,
            status,
            error_message,
            context_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "pred-run-001",
            now,
            "baseline-logreg",
            "v1",
            "v1",
            "dev-dataset",
            1,
            "SUCCESS",
            None,
            '{"seed": true}',
        ),
    )

    cursor.execute(
        "SELECT id FROM prediction_runs WHERE run_key = ?",
        ("pred-run-001",),
    )
    prediction_run_id = cursor.fetchone()["id"]

    # -------------------------
    # Phase 4: Prediction event
    # -------------------------
    cursor.execute(
        """
        INSERT OR IGNORE INTO prediction_events (
            created_at,
            run_id,
            document_id,
            score,
            threshold,
            decision,
            features_row_hash,
            metadata_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            now,
            prediction_run_id,
            "doc-001",
            0.75,
            0.5,
            "REVIEW",
            "hash-dev-001",
            '{"seed": true}',
        ),
    )

    conn.commit()
    conn.close()

    print("Seed data inserted successfully.")


if __name__ == "__main__":
    seed()
