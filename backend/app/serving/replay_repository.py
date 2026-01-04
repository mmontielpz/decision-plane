from typing import Optional, Dict, Any, List
from app.db.database import get_connection
from app.replay.runner import ReplayRunner


def get_replay_for_run(
    *, run_id: int, new_threshold: float
) -> List[Dict]:
    """
    Read-only decision replay for an existing prediction run.

    Guarantees:
    - No database writes
    - Deterministic output
    - Pure analytical view
    """
    runner = ReplayRunner(new_threshold=new_threshold)
    return runner.replay_run(run_id=run_id)


def get_document_replay(document_id: str) -> Optional[Dict[str, Any]]:
    """
    Replay read-model (v1).

    Builds a deterministic replay input bundle for a document.
    This is READ-ONLY infrastructure.

    Returns None when replay is not available.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # 1. Resolve last successful processing status
    cursor.execute(
        """
        SELECT
            dps.last_run_id,
            dps.processed_path,
            dps.feature_path
        FROM document_processing_status dps
        WHERE dps.document_id = ?
          AND dps.status = 'processed'
        """,
        (document_id,),
    )

    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    last_run_id, processed_path, feature_path = row

    # 2. Resolve processor version for the run
    cursor.execute(
        """
        SELECT processor_version
        FROM processing_runs
        WHERE run_id = ?
        """,
        (last_run_id,),
    )

    run_row = cursor.fetchone()
    if not run_row:
        conn.close()
        return None

    processor_version = run_row[0]

    # 3. Resolve raw artifact (immutable input)
    cursor.execute(
        """
        SELECT content_ref
        FROM document_artifacts
        WHERE document_id = ?
          AND artifact_type = 'raw'
        ORDER BY created_at ASC
        LIMIT 1
        """,
        (document_id,),
    )

    artifact_row = cursor.fetchone()
    if not artifact_row:
        conn.close()
        return None

    raw_path = artifact_row[0]

    conn.close()

    return {
        "document_id": document_id,
        "source_run_id": last_run_id,
        "processor_version": processor_version,
        "raw_path": raw_path,
        "processed_path": processed_path,
        "feature_path": feature_path,
    }
