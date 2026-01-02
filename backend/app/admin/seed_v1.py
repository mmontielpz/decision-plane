from datetime import datetime
import uuid

from app.db.database import get_connection
from app.core.config import settings


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
        ("document_sample_02.pdf", "unknown", "processed"),
        ("document_sample_02.pdf", "unknown", "indexed"),
        ("policy_internal.md", "policy", "processed"),
        ("policy_external.md", "policy", "indexed"),
        ("scan_low_quality.png", "unknown", "failed"),
        ("duplicate_document.pdf", "unknown", "uploaded"),
    ]

    rows = []

    for filename, doc_type, status in documents:
        doc_id = str(uuid.uuid4())
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
        rows.append((doc_id, status))

    return rows


def seed_processing_status(cursor, document_rows):
    for doc_id, status in document_rows:
        if status not in ("processed", "indexed"):
            continue

        cursor.execute(
            """
            INSERT INTO document_processing_status (
                document_id,
                status,
                processed_path,
                feature_path,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                doc_id,
                "processed",
                f"processed/{doc_id}.json",
                f"features/{doc_id}.json",
                NOW,
            ),
        )


def seed_artifacts(cursor, document_rows):
    for doc_id, _ in document_rows:
        cursor.execute(
            """
            INSERT INTO document_artifacts (
                document_id,
                artifact_type,
                content_ref,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (doc_id, "raw", f"/data/raw/{doc_id}", NOW),
        )

        cursor.execute(
            """
            INSERT INTO document_artifacts (
                document_id,
                artifact_type,
                content_ref,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (doc_id, "ocr_text", f"/data/processed/{doc_id}.txt", NOW),
        )


def seed_signals(cursor, document_rows):
    for doc_id, _ in document_rows:
        cursor.execute(
            """
            INSERT INTO document_signals (
                document_id,
                signal_type,
                signal_value,
                confidence,
                created_at
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
    if not settings.ENABLE_SEED_V1:
        raise RuntimeError("Seed V1 is disabled by configuration")

    conn = get_connection()
    cursor = conn.cursor()

    user_id = seed_users(cursor)
    source_id = seed_sources(cursor, user_id)
    document_rows = seed_documents(cursor, user_id, source_id)

    seed_processing_status(cursor, document_rows)
    seed_artifacts(cursor, document_rows)
    seed_signals(cursor, document_rows)

    conn.commit()
    conn.close()

    return {
        "users": 1,
        "sources": 1,
        "documents": len(document_rows),
        "artifacts": len(document_rows) * 2,
        "signals": len(document_rows),
        "visible_documents": len(
            [d for d, s in document_rows if s in ("processed", "indexed")]
        ),
    }


if __name__ == "__main__":
    summary = run_seed_v1()
    print("Seed V1 completed:", summary)
