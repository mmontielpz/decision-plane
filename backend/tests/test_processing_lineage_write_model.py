def test_processing_steps_written_during_batch_run(client):
    from app.core.config import settings

    # Enable seed explicitly
    settings.ENABLE_SEED_V1 = True

    # Seed system
    res = client.post("/api/admin/seed/v1")
    assert res.status_code == 200

    # Run batch
    from app.processing.runner import run_batch
    run_batch(limit=1)

    # Assert lineage
    from app.db.database import get_connection
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT step_name, status FROM processing_steps")
    rows = cursor.fetchall()

    conn.close()

    assert len(rows) >= 1
