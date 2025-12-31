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

    # -------------------------
    # Phase 5: Drift events
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS drift_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,

            window_start TEXT NOT NULL,
            window_end TEXT NOT NULL,

            drift_type TEXT NOT NULL,          -- INPUT|PREDICTION|DECISION
            metric_name TEXT NOT NULL,         -- e.g. psi, ks, js, rate_shift
            metric_value REAL NOT NULL,
            threshold REAL NOT NULL,
            is_alert INTEGER NOT NULL,         -- 0/1

            reference_window_key TEXT NOT NULL,
            current_window_key TEXT NOT NULL,

            notes TEXT,
            UNIQUE (
                window_start,
                window_end,
                drift_type,
                metric_name,
                reference_window_key,
                current_window_key
            )
        );
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_drift_events_window
        ON drift_events (window_start, window_end);
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_drift_events_type_metric
        ON drift_events (drift_type, metric_name);
        """
    )

    # -------------------------
    # Phase 5: Decision cost config (versioned)
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS decision_costs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,

            cost_version INTEGER NOT NULL,

            cost_fp REAL NOT NULL,
            cost_fn REAL NOT NULL,
            cost_review REAL NOT NULL,

            notes TEXT,
            UNIQUE (cost_version)
        );
        """
    )

    # -------------------------
    # Phase 5: Decision outcomes by window (post-label, delayed)
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS decision_outcomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,

            window_start TEXT NOT NULL,
            window_end TEXT NOT NULL,

            model_version TEXT NOT NULL,
            feature_version TEXT NOT NULL,
            threshold REAL NOT NULL,

            cost_version INTEGER NOT NULL,

            n_total INTEGER NOT NULL,
            n_accept INTEGER NOT NULL,
            n_review INTEGER NOT NULL,

            n_labeled INTEGER NOT NULL,
            tp INTEGER NOT NULL,
            fp INTEGER NOT NULL,
            tn INTEGER NOT NULL,
            fn INTEGER NOT NULL,

            total_cost REAL NOT NULL,

            reference_notes TEXT,
            FOREIGN KEY (cost_version) REFERENCES decision_costs(cost_version),
            UNIQUE (
                window_start,
                window_end,
                model_version,
                feature_version,
                threshold,
                cost_version
            )
        );
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_decision_outcomes_window
        ON decision_outcomes (window_start, window_end);
        """
    )

        # -------------------------
    # Phase 5: Feedback events
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,

            external_id TEXT NOT NULL,
            source TEXT NOT NULL,

            feedback_value TEXT NOT NULL,
            confidence REAL,
            notes TEXT,

            UNIQUE (external_id, source)
        );
        """
    )

    # -------------------------
    # Phase 5: Prediction ↔ Feedback linkage
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prediction_feedback_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,

            feedback_id INTEGER NOT NULL,
            prediction_event_id INTEGER NOT NULL,

            FOREIGN KEY (feedback_id) REFERENCES feedback_events(id),
            FOREIGN KEY (prediction_event_id) REFERENCES prediction_events(id),

            UNIQUE (feedback_id, prediction_event_id)
        );
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_feedback_links_prediction
        ON prediction_feedback_links (prediction_event_id);
        """
    )

        # -------------------------
    # Product: Users (mock / logical)
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        );
        """
    )

    # -------------------------
    # Product: Sources
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            source_type TEXT NOT NULL,     -- e.g. upload
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )

    # -------------------------
    # Product: Documents
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,           -- UUID / deterministic id
            user_id INTEGER NOT NULL,
            source_id INTEGER NOT NULL,

            filename TEXT NOT NULL,
            document_type TEXT,            -- contract | invoice | policy | unknown
            ingestion_status TEXT NOT NULL,

            created_at TEXT NOT NULL,

            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (source_id) REFERENCES sources(id)
        );
        """
    )

    # -------------------------
    # Product: Document artifacts
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS document_artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT NOT NULL,

            artifact_type TEXT NOT NULL,   -- raw | ocr_text | parsed
            content_ref TEXT NOT NULL,

            created_at TEXT NOT NULL,

            FOREIGN KEY (document_id) REFERENCES documents(id)
        );
        """
    )

    # -------------------------
    # Product: Document signals
    # -------------------------
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS document_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT NOT NULL,

            signal_type TEXT NOT NULL,     -- quality_flag | risk_flag
            signal_value TEXT NOT NULL,    -- e.g. low_ocr_confidence
            confidence REAL,

            created_at TEXT NOT NULL,

            FOREIGN KEY (document_id) REFERENCES documents(id)
        );
        """
    )

    conn.commit()
    conn.close()
