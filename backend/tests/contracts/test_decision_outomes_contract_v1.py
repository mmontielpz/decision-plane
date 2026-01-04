def test_decision_outcomes_contract_v1_returns_404(client):
    response = client.get("/api/decision-outcomes")

    assert response.status_code == 404
    body = response.json()

    assert "detail" in body
    assert body["detail"] == "Decision outcomes not available"
