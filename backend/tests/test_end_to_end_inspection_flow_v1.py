import os

os.environ["ENABLE_SEED_V1"] = "true"

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_end_to_end_inspection_flow_v1():
    # 1) Seed system
    res = client.post("/api/admin/seed/v1")
    assert res.status_code == 200

    # 2) Dashboard
    dashboard = client.get("/api/dashboard/summary").json()
    assert dashboard["documents_needing_review"] >= 1

    # 3) Review queue
    queue = client.get("/api/review-queue").json()
    assert len(queue) >= 1

    item = queue[0]
    document_id = item["document_id"]
    reason = item["reason"]

    # 4) Document detail
    detail = client.get(f"/api/documents/{document_id}").json()
    assert detail["latest_prediction"] is not None

    # 5) Invariant
    assert detail["review_reason"] == reason
