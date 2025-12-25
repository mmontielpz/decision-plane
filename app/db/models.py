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

        # -------------------------
    # Phase 4: Prediction runs
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prediction_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_key TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,

            model_name TEXT NOT NULL,
            model_version TEXT NOT NULL,
            feature_version TEXT NOT NULL,

            dataset_key TEXT NOT NULL,
            dataset_rows INTEGER,

            status TEXT NOT NULL,
            error_message TEXT,
            context_json TEXT
        );
        """
    )

    # -------------------------
    # Phase 4: Prediction events
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prediction_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,

            run_id INTEGER NOT NULL,
            document_id TEXT NOT NULL,

            score REAL NOT NULL,
            threshold REAL NOT NULL,
            decision TEXT NOT NULL,

            features_row_hash TEXT,
            metadata_json TEXT,

            FOREIGN KEY (run_id) REFERENCES prediction_runs(id),
            UNIQUE (run_id, document_id)
        );
        """
    )

    # Helpful indexes for batch reads and audits
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_prediction_events_run_id
        ON prediction_events (run_id);
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_prediction_events_document_id
        ON prediction_events (document_id);
        """
    )

    conn.commit()
    conn.close()
