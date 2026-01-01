from fastapi.testclient import TestClient
from app.main import app
from app.db.database import get_connection


client = TestClient(app)


def test_dashboard_summary_counts_visible_documents():
    conn = get_connection()
    cursor = conn.cursor()

    # --- User ---
    cursor.execute(
        """
        INSERT INTO users (email, created_at)
        VALUES (?, datetime('now'))
        """,
        ("operator@demo.local",),
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

    # --- Documents ---
    documents = [
        ("doc-visible-1", "processed"),
        ("doc-visible-2", "indexed"),
        ("doc-hidden-1", "uploaded"),
        ("doc-hidden-2", "failed"),
    ]

    for doc_id, status in documents:
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
                doc_id,
                user_id,
                source_id,
                f"{doc_id}.pdf",
                "contract",
                status,
            ),
        )

        if status in ("processed", "indexed"):
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
                    doc_id,
                    status,
                    f"processed/{doc_id}.json",
                    f"features/{doc_id}.json",
                ),
            )

    conn.commit()
    conn.close()

    # --- Call API ---
    res = client.get("/api/dashboard/summary")
    assert res.status_code == 200

    body = res.json()

    assert body["total_visible_documents"] == 2
    assert body["processed_documents"] == 2
    assert body["documents_needing_review"] == 0
    assert body["latest_activity_at"] is not None
