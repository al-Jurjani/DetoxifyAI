import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
    # Empty text should return 400 error as per main.py line 151
    assert res.status_code == 400
    data = res.json()
    assert "detail" in data


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


def test_root_endpoint():
    """Test the root / endpoint returns correct message."""
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert "message" in data
    assert "model_loaded" in data


def test_metrics_endpoint():
    """Test the /metrics endpoint for Prometheus."""
    res = client.get("/metrics")
    assert res.status_code == 200
    # Prometheus metrics should be plain text
    assert "text/plain" in res.headers.get("content-type", "").lower() or \
           "prometheus" in res.headers.get("content-type", "").lower()


def test_predict_response_structure():
    """Test that /predict returns all expected fields."""
    res = client.post("/predict", json={"text": "test message"})
    assert res.status_code == 200
    data = res.json()
    assert "input" in data
    assert "prediction" in data
    assert "confidence" in data
    assert "model_loaded" in data
    assert data["input"] == "test message"


def test_predict_toxic_text():
    """Test prediction with potentially toxic text."""
    res = client.post("/predict", json={"text": "you are stupid and ugly"})
    assert res.status_code == 200
    data = res.json()
    assert data["prediction"] in ["toxic", "non-toxic"]
    assert 0.0 <= data["confidence"] <= 1.0


def test_predict_non_toxic_text():
    """Test prediction with clearly non-toxic text."""
    res = client.post("/predict", json={"text": "have a wonderful day"})
    assert res.status_code == 200
    data = res.json()
    assert data["prediction"] in ["toxic", "non-toxic"]
    assert 0.0 <= data["confidence"] <= 1.0


def test_health_model_loaded_field():
    """Test that /health includes model_loaded field."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert "model_loaded" in data
    assert isinstance(data["model_loaded"], bool)
