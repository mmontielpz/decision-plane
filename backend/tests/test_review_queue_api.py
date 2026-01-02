from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_connection

client = TestClient(app)


def test_review_queue_basic_behavior():
    """
    Review Queue v1 (Finance / AP)

    Inclusion rules:
    - document_type = unknown
    - OR confidence < 0.80
    - OR missing prediction

    Exclusion rule:
    - invoice with confidence >= 0.80
    """

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # User
    # -------------------------
    cursor.execute(
        """
        INSERT INTO users (email, created_at)
        VALUES ('ap@company.local', datetime('now'))
        """
    )
    user_id = cursor.lastrowid

    # -------------------------
    # Source
    # -------------------------
    cursor.execute(
        """
        INSERT INTO sources (user_id, source_type, created_at)
        VALUES (?, 'upload', datetime('now'))
        """,
        (user_id,),
    )
    source_id = cursor.lastrowid

    # -------------------------
    # Documents
    # -------------------------
    documents = [
        # invoice, high confidence -> should NOT appear
        ("doc-ok", "invoice"),
        # invoice, low confidence -> should appear
        ("doc-low", "invoice"),
        # unknown, no prediction -> should appear
        ("doc-unknown", "unknown"),
    ]

    for doc_id, doc_type in documents:
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
            VALUES (?, ?, ?, ?, ?, 'processed', datetime('now'))
            """,
            (
                doc_id,
                user_id,
                source_id,
                f"{doc_id}.pdf",
                doc_type,
            ),
        )

        cursor.execute(
            """
            INSERT INTO document_processing_status (
                document_id,
                status,
                updated_at
            )
            VALUES (?, 'processed', datetime('now'))
            """,
            (doc_id,),
        )

    # -------------------------
    # Prediction runs
    # -------------------------
    cursor.execute(
        """
        INSERT INTO prediction_runs (
            run_key,
            created_at,
            model_name,
            model_version,
            feature_version,
            dataset_key,
            status
        )
        VALUES (
            'run-1',
            datetime('now'),
            'doc-classifier',
            'v1',
            'v1',
            'test',
            'completed'
        )
        """
    )
    run_id = cursor.lastrowid

    # -------------------------
    # Predictions
    # -------------------------
    predictions = [
        # High confidence invoice (excluded)
        ("doc-ok", 0.92),
        # Low confidence invoice (included)
        ("doc-low", 0.65),
    ]

    for doc_id, score in predictions:
        cursor.execute(
            """
            INSERT INTO prediction_events (
                created_at,
                run_id,
                document_id,
                score,
                threshold,
                decision
            )
            VALUES (datetime('now'), ?, ?, ?, 0.80, 'accept')
            """,
            (run_id, doc_id, score),
        )

    conn.commit()
    conn.close()

    # -------------------------
    # Call API
    # -------------------------
    res = client.get("/api/review-queue")

    assert res.status_code == 200

    body = res.json()
    ids = {item["document_id"] for item in body}

    # -------------------------
    # Assertions
    # -------------------------
    assert "doc-low" in ids          # low confidence
    assert "doc-unknown" in ids      # unknown, no prediction
    assert "doc-ok" not in ids       # high confidence invoice excluded

    # Reasons are deterministic
    reasons = {item["document_id"]: item["reason"] for item in body}

    assert reasons["doc-low"] == "low_confidence"
    assert reasons["doc-unknown"] == "missing_prediction"
