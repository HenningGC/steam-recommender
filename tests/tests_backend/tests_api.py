# backend/tests/test_api.py

import json

def test_get_recommendations(client):
    # Test valid input
    response = client.post('/recommendations', json={"input": "valid input", "model": "model1"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0

    # Test invalid input
    response = client.post('/recommendations', json={"input": "invalid input", "model": "model1"})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Input not found"

    # Test missing input
    response = client.post('/recommendations', json={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Input not found"
