from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings


client = TestClient(app)


def test_document_detail_includes_processing_lineage():
    # Explicitly enable seed (settings already loaded)
    settings.ENABLE_SEED_V1 = True

    # Seed system
    res = client.post("/api/admin/seed/v1")
    assert res.status_code == 200

    # Fetch documents
    docs = client.get("/api/documents").json()
    assert len(docs) >= 1

    document_id = docs[0]["id"]

    # Document detail
    detail = client.get(f"/api/documents/{document_id}").json()

    assert "processing_lineage" in detail
    assert isinstance(detail["processing_lineage"], list)

    if detail["processing_lineage"]:
        step = detail["processing_lineage"][0]
        assert "step" in step
        assert "status" in step
        assert "created_at" in step
