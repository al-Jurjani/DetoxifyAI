from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_status_field_exists():
    """Check that /health returns a JSON with key 'status'."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
    assert data["status"] in ["ok", "healthy"]


def test_predict_with_empty_text():
    """Check that /predict handles empty text gracefully."""
    res = client.post("/predict", json={"text": ""})
    assert res.status_code == 200
    data = res.json()
    assert "prediction" in data


def test_predict_with_long_text():
    """Check /predict with long input (to ensure path coverage)."""
    text = "This is a long text input for testing purposes." * 20
    res = client.post("/predict", json={"text": text})
    assert res.status_code == 200
    data = res.json()
    assert "confidence" in data
    assert isinstance(data["confidence"], float)


def test_predict_content_type():
    """Check that sending wrong content type returns error 422."""
    res = client.post("/predict", data="not json data")
    assert res.status_code in [400, 422]
