import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_predict_with_whitespace_only():
    """Test prediction with only whitespace."""
    res = client.post("/predict", json={"text": "   "})
    assert res.status_code == 400  # Should reject empty/whitespace


def test_predict_with_special_characters():
    """Test prediction with special characters."""
    res = client.post("/predict", json={"text": "!@#$%^&*()"})
    assert res.status_code == 200
    data = res.json()
    assert "prediction" in data


def test_predict_with_mixed_content():
    """Test prediction with mixed content."""
    res = client.post("/predict", json={"text": "Hello 123 @user #tag http://example.com"})
    assert res.status_code == 200
    data = res.json()
    assert data["prediction"] in ["toxic", "non-toxic"]
    assert "confidence" in data


def test_predict_confidence_range():
    """Test that confidence is always between 0 and 1."""
    texts = [
        "hello world",
        "you are stupid",
        "nice to meet you",
        "I hate this",
        "wonderful day"
    ]
    for text in texts:
        res = client.post("/predict", json={"text": text})
        assert res.status_code == 200
        data = res.json()
        assert 0.0 <= data["confidence"] <= 1.0
        if "toxic_probability" in data:
            assert 0.0 <= data["toxic_probability"] <= 1.0


def test_predict_input_echo():
    """Test that the input is echoed back in the response."""
    test_text = "This is my test input"
    res = client.post("/predict", json={"text": test_text})
    assert res.status_code == 200
    data = res.json()
    assert data["input"] == test_text


def test_health_always_returns_ok():
    """Test that /health consistently returns ok status."""
    for _ in range(5):
        res = client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ok"


def test_root_endpoint_structure():
    """Test that root endpoint has expected structure."""
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "model_loaded" in data
    assert isinstance(data["model_loaded"], bool)


def test_predict_with_unicode():
    """Test prediction with unicode characters."""
    res = client.post("/predict", json={"text": "Hello 你好 مرحبا"})
    assert res.status_code == 200
    data = res.json()
    assert "prediction" in data


def test_predict_with_emojis():
    """Test prediction with emojis."""
    res = client.post("/predict", json={"text": "I love this 😊❤️"})
    assert res.status_code == 200
    data = res.json()
    assert "prediction" in data


def test_predict_with_newlines():
    """Test prediction with newlines."""
    res = client.post("/predict", json={"text": "Line 1\nLine 2\nLine 3"})
    assert res.status_code == 200
    data = res.json()
    assert "prediction" in data
