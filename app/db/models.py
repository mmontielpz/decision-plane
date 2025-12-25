from app.db.database import get_connection
from datetime import datetime


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # Phase 1: Ingestion events
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ingestion_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT NOT NULL UNIQUE,
            ingestion_timestamp TEXT NOT NULL,
            source_system TEXT,
            status TEXT NOT NULL
        );
        """
    )

    # -------------------------
    # Phase 2: Processing runs
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS processing_runs (
            run_id TEXT PRIMARY KEY,
            started_at TEXT NOT NULL,
            completed_at TEXT,
            processor_version TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS document_processing_status (
            document_id TEXT PRIMARY KEY,
            last_run_id TEXT,
            status TEXT NOT NULL,
            processed_path TEXT,
            feature_path TEXT,
            error_code TEXT,
            error_message TEXT,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (last_run_id) REFERENCES processing_runs(run_id)
        );
        """
    )

    # -------------------------
    # Phase 3: Label signals
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS labels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT NOT NULL,
            label_value TEXT NOT NULL,
            label_type TEXT NOT NULL,
            label_source TEXT NOT NULL,
            label_timestamp TEXT NOT NULL,
            label_version INTEGER NOT NULL,
            confidence REAL,
            created_at TEXT NOT NULL,
            UNIQUE (
                document_id,
                label_type,
                label_source,
                label_version
            )
        );
        """
    )

    conn.commit()
    conn.close()
