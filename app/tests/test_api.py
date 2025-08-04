# test delle api
# testclient
from fastapi.testclient import TestClient
from app.main import app  # Import di FastAPI

client = TestClient(app)


def test_health_check():
    """Tests the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_endpoint_setosa():
    """Tests a valid prediction request for a 'setosa' iris."""
    payload = {"features": [[5.1, 3.5, 1.4, 0.2]]}
    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "predictions" in data
    assert data["predictions"][0] == "setosa"
