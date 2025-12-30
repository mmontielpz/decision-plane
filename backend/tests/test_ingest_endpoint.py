import json
from pathlib import Path


def ingest_payload(document_id="doc_001"):
    return {
        "data": {
            "metadata": json.dumps(
                {
                    "document_id": document_id,
                    "ingestion_timestamp": "2025-01-01T10:00:00",
                    "document_type": "invoice",
                    "source_system": "test",
                }
            )
        },
        "files": {
            "file": ("dummy.txt", b"test content")
        },
    }

# HTTP 200
def test_ingest_success(client):
    payload = ingest_payload("doc_001")

    response = client.post(
        "/ingest",
        data=payload["data"],
        files=payload["files"],
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "received"
    assert "raw_path" in body


# HTTP 409
def test_ingest_duplicate(client):
    payload = ingest_payload("doc_001")

    client.post(
        "/ingest",
        data=payload["data"],
        files=payload["files"],
    )

    response = client.post(
        "/ingest",
        data=payload["data"],
        files=payload["files"],
    )

    assert response.status_code == 409
    assert response.json()["detail"]["status"] == "already_exists"

# HTTP 422
def test_ingest_invalid_metadata(client):
    response = client.post(
        "/ingest",
        data={"metadata": "not-a-json"},
        files={"file": ("dummy.txt", b"test")},
    )

    assert response.status_code == 422


# HTTP 500
def test_ingest_raw_storage_failure(client, monkeypatch):
    def fail_mkdir(self, *args, **kwargs):
        if "data/raw" in str(self):
            raise PermissionError("no permission")
        return original_mkdir(self, *args, **kwargs)

    original_mkdir = Path.mkdir
    monkeypatch.setattr(Path, "mkdir", fail_mkdir)

    payload = ingest_payload("doc_002")

    response = client.post(
        "/ingest",
        data=payload["data"],
        files=payload["files"],
    )

    assert response.status_code == 500
