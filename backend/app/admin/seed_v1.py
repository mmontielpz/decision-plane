from datetime import datetime
import uuid

from app.db.database import get_connection
from app.db.models import init_db


NOW = datetime.utcnow().isoformat()


def seed_users(cursor):
    cursor.execute(
        """
        INSERT OR IGNORE INTO users (email, created_at)
        VALUES (?, ?)
        """,
        ("demo@risk-aware.local", NOW),
    )

    cursor.execute(
        "SELECT id FROM users WHERE email = ?",
        ("demo@risk-aware.local",),
    )
    return cursor.fetchone()[0]


def seed_sources(cursor, user_id):
    cursor.execute(
        """
        INSERT INTO sources (user_id, source_type, created_at)
        VALUES (?, ?, ?)
        """,
        (user_id, "upload", NOW),
    )
    return cursor.lastrowid


def seed_documents(cursor, user_id, source_id):
    documents = [
        ("contract_alpha.pdf", "contract", "uploaded"),
        ("contract_beta.pdf", "contract", "processed"),
        ("invoice_2023_01.pdf", "invoice", "processed"),
        ("invoice_2023_02.pdf", "invoice", "indexed"),
        ("policy_internal.md", "policy", "processed"),
        ("policy_external.md", "policy", "indexed"),
        ("scan_low_quality.png", "unknown", "failed"),
        ("duplicate_invoice.pdf", "invoice", "uploaded"),
    ]

    document_ids = []

    for filename, doc_type, status in documents:
        doc_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO documents (
                id, user_id, source_id,
                filename, document_type, ingestion_status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                doc_id,
                user_id,
                source_id,
                filename,
                doc_type,
                status,
                NOW,
            ),
        )
        document_ids.append(doc_id)

    return document_ids


def seed_artifacts(cursor, document_ids):
    for doc_id in document_ids:
        cursor.execute(
            """
            INSERT INTO document_artifacts (
                document_id, artifact_type, content_ref, created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (doc_id, "raw", f"/data/raw/{doc_id}", NOW),
        )

        cursor.execute(
            """
            INSERT INTO document_artifacts (
                document_id, artifact_type, content_ref, created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (doc_id, "ocr_text", f"/data/processed/{doc_id}.txt", NOW),
        )


def seed_signals(cursor, document_ids):
    for doc_id in document_ids:
        cursor.execute(
            """
            INSERT INTO document_signals (
                document_id, signal_type, signal_value, confidence, created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                doc_id,
                "quality_flag",
                "low_ocr_confidence",
                0.42,
                NOW,
            ),
        )


def run_seed_v1():
    # schema initialization
    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    user_id = seed_users(cursor)
    source_id = seed_sources(cursor, user_id)
    document_ids = seed_documents(cursor, user_id, source_id)
    seed_artifacts(cursor, document_ids)
    seed_signals(cursor, document_ids)

    conn.commit()
    conn.close()

    return {
        "users": 1,
        "sources": 1,
        "documents": len(document_ids),
        "artifacts": len(document_ids) * 2,
        "signals": len(document_ids),
    }


if __name__ == "__main__":
    summary = run_seed_v1()
    print("Seed V1 completed:", summary)
