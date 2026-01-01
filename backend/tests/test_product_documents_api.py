from pathlib import Path
import pytest
from app.main import app
from fastapi.testclient import TestClient
from app.db.database import get_connection

client = TestClient(app)


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


def _seed_document(
    *,
    document_id: str,
    ingestion_status: str,
    processing_status: str | None,
):
    conn = get_connection()
    cursor = conn.cursor()

    # user
    cursor.execute(
        "INSERT INTO users (email, created_at) VALUES (?, datetime('now'))",
        (f"{document_id}@example.local",),
    )
    user_id = cursor.lastrowid

    # source
    cursor.execute(
        "INSERT INTO sources (user_id, source_type, created_at) VALUES (?, ?, datetime('now'))",
        (user_id, "upload"),
    )
    source_id = cursor.lastrowid

    # document
    cursor.execute(
        """
        INSERT INTO documents (
            id, user_id, source_id, filename,
            document_type, ingestion_status, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            document_id,
            user_id,
            source_id,
            f"{document_id}.pdf",
            "contract",
            ingestion_status,
        ),
    )

    # processing status (optional)
    if processing_status is not None:
        cursor.execute(
            """
            INSERT INTO document_processing_status (
                document_id, status, updated_at
            )
            VALUES (?, ?, datetime('now'))
            """,
            (document_id, processing_status),
        )

    conn.commit()
    conn.close()


def test_list_documents_returns_only_visible():
    """
    Visible := processing_status ∈ ('processed','indexed')
    """
    _seed_document(
        document_id="doc-visible-1",
        ingestion_status="processed",
        processing_status="processed",
    )
    _seed_document(
        document_id="doc-visible-2",
        ingestion_status="processed",
        processing_status="indexed",
    )
    _seed_document(
        document_id="doc-hidden-1",
        ingestion_status="uploaded",
        processing_status="uploaded",
    )
    _seed_document(
        document_id="doc-hidden-2",
        ingestion_status="failed",
        processing_status="failed",
    )

    res = client.get("/api/documents")
    assert res.status_code == 200

    ids = {d["id"] for d in res.json()}

    assert "doc-visible-1" in ids
    assert "doc-visible-2" in ids
    assert "doc-hidden-1" not in ids
    assert "doc-hidden-2" not in ids


def test_list_documents_empty_when_no_visible():
    _seed_document(
        document_id="doc-uploaded",
        ingestion_status="uploaded",
        processing_status="uploaded",
    )

    res = client.get("/api/documents")
    assert res.status_code == 200
    assert res.json() == []

def test_get_document_detail_returns_404_if_not_visible():
    conn = get_connection()
    cursor = conn.cursor()

    # user
    cursor.execute(
        "INSERT INTO users (email, created_at) VALUES (?, datetime('now'))",
        ("hidden@example.local",),
    )
    user_id = cursor.lastrowid

    # source
    cursor.execute(
        "INSERT INTO sources (user_id, source_type, created_at) VALUES (?, ?, datetime('now'))",
        (user_id, "upload"),
    )
    source_id = cursor.lastrowid

    # document
    cursor.execute(
        """
        INSERT INTO documents (
            id, user_id, source_id, filename,
            document_type, ingestion_status, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            "doc-hidden",
            user_id,
            source_id,
            "hidden.pdf",
            "contract",
            "uploaded",
        ),
    )

    # processing status NOT visible
    cursor.execute(
        """
        INSERT INTO document_processing_status (
            document_id, status, updated_at
        )
        VALUES (?, ?, datetime('now'))
        """,
        ("doc-hidden", "uploaded"),
    )

    conn.commit()
    conn.close()

    res = client.get("/api/documents/doc-hidden")
    assert res.status_code == 404
