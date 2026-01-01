import os
from fastapi.testclient import TestClient
from app.main import app


def test_seed_v1_disabled_by_default():
    """
    Seed endpoint must be disabled unless explicitly enabled.
    """
    os.environ.pop("ENABLE_SEED_V1", None)

    client = TestClient(app)
    response = client.post("/api/admin/seed/v1")

    assert response.status_code == 403
    assert response.json()["detail"] == "Seed V1 is disabled"

def test_seed_v1_enabled(monkeypatch):
    """
    When ENABLE_SEED_V1 is true, the seed endpoint should run successfully.
    """
    monkeypatch.setenv("ENABLE_SEED_V1", "true")

    from app.core.config import settings
    settings.ENABLE_SEED_V1 = True

    client = TestClient(app)
    response = client.post("/api/admin/seed/v1")

    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["seed"] == "v1"

    summary = payload["summary"]
    assert summary["users"] == 1
    assert summary["sources"] == 1
    assert summary["documents"] > 0
    assert summary["artifacts"] > 0
    assert summary["signals"] > 0
