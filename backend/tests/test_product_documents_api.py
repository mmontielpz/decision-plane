from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.db.database import get_connection


def _make_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> TestClient:
    db_path = tmp_path / "db" / "metadata.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))

    # Import AFTER env is set
    from app.db.models import init_db
    from app.main import app

    # Explicit schema initialization for tests
    init_db()

    return TestClient(app)


def test_get_document_detail(monkeypatch, tmp_path):
    client = _make_client(monkeypatch, tmp_path)

    conn = get_connection()
    cursor = conn.cursor()

    # --- User ---
    cursor.execute(
        """
        INSERT INTO users (email, created_at)
        VALUES (?, datetime('now'))
        """,
        ("demo@risk-aware.local",),
    )
    user_id = cursor.lastrowid

    # --- Source ---
    cursor.execute(
        """
        INSERT INTO sources (user_id, source_type, created_at)
        VALUES (?, ?, datetime('now'))
        """,
        (user_id, "upload"),
    )
    source_id = cursor.lastrowid

    # --- Document ---
    cursor.execute(
        """
        INSERT INTO documents (
            id,
            user_id,
            source_id,
            filename,
            document_type,
            ingestion_status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            "doc-001",
            user_id,
            source_id,
            "example.pdf",
            "contract",
            "processed",
        ),
    )

    # --- Processing status ---
    cursor.execute(
        """
        INSERT INTO document_processing_status (
            document_id,
            status,
            processed_path,
            feature_path,
            updated_at
        )
        VALUES (?, ?, ?, ?, datetime('now'))
        """,
        (
            "doc-001",
            "processed",
            "processed/doc-001.json",
            "features/doc-001.json",
        ),
    )

    conn.commit()
    conn.close()

    # --- Call API ---
    res = client.get("/api/documents/doc-001")

    assert res.status_code == 200

    body = res.json()
    assert body["id"] == "doc-001"
    assert body["filename"] == "example.pdf"
    assert body["processing"]["status"] == "processed"
