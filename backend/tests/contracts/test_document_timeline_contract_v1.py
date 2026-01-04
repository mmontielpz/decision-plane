def test_document_timeline_contract_v1_returns_404(client):
    """
    Contract-only test.

    Guarantees:
    - Endpoint exists
    - Returns 404 when timeline is unavailable
    - Does not leak partial data
    """
    response = client.get("/api/documents/fake-document-id/timeline")

    assert response.status_code == 404
    body = response.json()

    assert "detail" in body
    assert body["detail"] == "Timeline not available for this document"
