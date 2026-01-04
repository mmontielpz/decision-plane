from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_document_replay_v1_returns_404():
    """
    Replay endpoint exists but is intentionally unimplemented.

    Contract:
    - Endpoint must exist
    - Must return 404
    - Must NOT leak partial data
    """
    response = client.get("/api/documents/fake-document-id/replay")

    assert response.status_code == 404
    body = response.json()

    assert "detail" in body
    assert body["detail"] == "Replay not available for this document"
