from app.db.database import get_connection


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ingestion_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT NOT NULL,
            ingestion_timestamp TEXT NOT NULL,
            source_system TEXT,
            status TEXT NOT NULL
        );
        """
    )

    conn.commit()
    conn.close()
