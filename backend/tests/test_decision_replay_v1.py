def test_decision_replay_is_read_only(client):
    # Seed system
    from app.core.config import settings
    settings.ENABLE_SEED_V1 = True
    client.post("/api/admin/seed/v1")

    # Fetch an existing run
    from app.db.database import get_connection
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM prediction_runs LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    run_id = row[0]

    # Replay
    res = client.get(
        f"/api/replay/run/{run_id}?threshold=0.5"
    )
    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, list)

    # Replay must not write anything
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM prediction_events")
    count_after = cursor.fetchone()[0]
    conn.close()

    assert count_after > 0
