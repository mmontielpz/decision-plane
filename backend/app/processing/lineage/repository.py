# backend/app/processing/lineage/repository.py

from datetime import datetime
from typing import Iterable, Optional

from app.db.database import get_connection
from app.processing.lineage.models import (
    ProcessingRun,
    ProcessingStep,
    ProcessingArtifactRef,
)


class ProcessingLineageRepository:
    """
    Append-only persistence for processing lineage.

    Guarantees:
    - No updates
    - No deletes
    - Deterministic ordering
    """

    def _ensure_tables(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS processing_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                document_id TEXT NOT NULL,
                pipeline_version TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                status TEXT NOT NULL,
                error_message TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS processing_steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                step_name TEXT NOT NULL,
                step_version TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                status TEXT NOT NULL,
                metadata_json TEXT,
                error_message TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS processing_artifacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                step_name TEXT NOT NULL,
                artifact_type TEXT NOT NULL,
                content_ref TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.commit()
        conn.close()

    # -------------------------
    # Writes (append-only)
    # -------------------------

    def insert_run(self, run: ProcessingRun) -> None:
        self._ensure_tables()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO processing_runs (
                run_id,
                document_id,
                pipeline_version,
                started_at,
                completed_at,
                status,
                error_message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run.run_id,
                run.document_id,
                run.pipeline_version,
                run.started_at.isoformat(),
                run.completed_at.isoformat() if run.completed_at else None,
                run.status,
                run.error_message,
            ),
        )

        conn.commit()
        conn.close()

    def insert_steps(self, steps: Iterable[ProcessingStep]) -> None:
        self._ensure_tables()

        conn = get_connection()
        cursor = conn.cursor()

        rows = []
        for s in steps:
            rows.append(
                (
                    s.run_id,
                    s.step_name,
                    s.step_version,
                    s.started_at.isoformat(),
                    s.completed_at.isoformat() if s.completed_at else None,
                    s.status,
                    None if s.metadata is None else str(s.metadata),
                    s.error_message,
                )
            )

        cursor.executemany(
            """
            INSERT INTO processing_steps (
                run_id,
                step_name,
                step_version,
                started_at,
                completed_at,
                status,
                metadata_json,
                error_message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

        conn.commit()
        conn.close()

    def insert_artifacts(self, artifacts: Iterable[ProcessingArtifactRef]) -> None:
        self._ensure_tables()

        conn = get_connection()
        cursor = conn.cursor()

        rows = []
        for a in artifacts:
            rows.append(
                (
                    a.run_id,
                    a.step_name,
                    a.artifact_type,
                    a.content_ref,
                    a.created_at.isoformat(),
                )
            )

        cursor.executemany(
            """
            INSERT INTO processing_artifacts (
                run_id,
                step_name,
                artifact_type,
                content_ref,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            rows,
        )

        conn.commit()
        conn.close()

    # -------------------------
    # Reads (audit only)
    # -------------------------

    def list_runs_for_document(self, document_id: str) -> list[ProcessingRun]:
        self._ensure_tables()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                run_id,
                document_id,
                pipeline_version,
                started_at,
                completed_at,
                status,
                error_message
            FROM processing_runs
            WHERE document_id = ?
            ORDER BY started_at ASC
            """,
            (document_id,),
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            ProcessingRun(
                run_id=r[0],
                document_id=r[1],
                pipeline_version=r[2],
                started_at=datetime.fromisoformat(r[3]),
                completed_at=datetime.fromisoformat(r[4]) if r[4] else None,
                status=r[5],
                error_message=r[6],
            )
            for r in rows
        ]
