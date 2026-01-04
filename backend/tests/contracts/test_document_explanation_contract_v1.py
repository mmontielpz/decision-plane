def test_document_explanation_contract_v1_shape(client):
    """
    Contract-only test.

    Behavior expectations:
    - Endpoint exists
    - Returns 404 when explanation is unavailable
    - Response shape is stable once implemented
    """
    response = client.get("/api/documents/fake-document-id/explanation")

    assert response.status_code == 404
    body = response.json()

    assert "detail" in body
    assert body["detail"] == "Explanation not available for this document"
