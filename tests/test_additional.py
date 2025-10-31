import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app, preprocess_aggressive

client = TestClient(app)


def test_root_message_content():
    """Test that root endpoint contains expected message."""
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert "DetoxifyAI" in data["message"] or "running" in data["message"].lower()


def test_health_endpoint_model_loaded_bool():
    """Test that model_loaded is always a boolean."""
    for _ in range(3):
        res = client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data["model_loaded"], bool)


def test_predict_very_long_text():
    """Test prediction with very long text."""
    long_text = "This is a test sentence. " * 100  # 500 words
    res = client.post("/predict", json={"text": long_text})
    assert res.status_code == 200
    data = res.json()
    assert "prediction" in data
    assert data["prediction"] in ["toxic", "non-toxic"]


def test_predict_single_word():
    """Test prediction with single word."""
    for word in ["hello", "goodbye", "yes", "no"]:
        res = client.post("/predict", json={"text": word})
        assert res.status_code == 200
        data = res.json()
        assert "prediction" in data


def test_predict_only_symbols():
    """Test prediction with only symbols."""
    res = client.post("/predict", json={"text": "!!!???###$$$"})
    assert res.status_code == 200


def test_predict_mixed_languages():
    """Test with mixed language text."""
    res = client.post("/predict", json={"text": "Hello مرحبا 你好"})
    assert res.status_code == 200


def test_predict_repeated_characters():
    """Test with repeated characters."""
    res = client.post("/predict", json={"text": "hellooooooo woooooorld"})
    assert res.status_code == 200


def test_predict_all_caps():
    """Test with all caps text."""
    res = client.post("/predict", json={"text": "THIS IS ALL CAPS TEXT"})
    assert res.status_code == 200
    data = res.json()
    assert data["input"] == "THIS IS ALL CAPS TEXT"


def test_preprocess_empty_string():
    """Test preprocessing with empty string."""
    result = preprocess_aggressive("")
    assert result == ""


def test_preprocess_only_whitespace():
    """Test preprocessing with only whitespace."""
    result = preprocess_aggressive("   \t\n   ")
    # Should return empty or just whitespace
    assert len(result.strip()) == 0


def test_preprocess_unicode_characters():
    """Test preprocessing with unicode."""
    text = "Hello 世界 🌍"
    result = preprocess_aggressive(text)
    # Should still process it
    assert isinstance(result, str)


def test_preprocess_multiple_urls():
    """Test preprocessing removes multiple URLs."""
    text = "Check https://site1.com and http://site2.org and www.site3.net"
    result = preprocess_aggressive(text)
    assert "https://" not in result
    assert "http://" not in result
    assert "www." not in result


def test_preprocess_hashtags_and_mentions():
    """Test preprocessing removes @ and #."""
    text = "@john @jane #topic #trending @user123 #test"
    result = preprocess_aggressive(text)
    assert "@" not in result
    assert "#" not in result


def test_preprocess_only_numbers():
    """Test preprocessing with only numbers."""
    result = preprocess_aggressive("123 456 789")
    # Numbers should be removed
    assert "123" not in result


def test_preprocess_mixed_case_normalization():
    """Test that preprocessing normalizes case."""
    text = "HeLLo WoRLd"
    result = preprocess_aggressive(text)
    assert result == "hello world"


def test_predict_with_numbers_in_text():
    """Test prediction with numbers embedded in text."""
    res = client.post("/predict", json={"text": "I have 100 apples and 200 oranges"})
    assert res.status_code == 200


def test_predict_with_urls_in_text():
    """Test prediction with URLs in text."""
    res = client.post("/predict", json={"text": "Visit https://example.com for more"})
    assert res.status_code == 200


def test_multiple_sequential_predictions():
    """Test multiple predictions in sequence."""
    texts = ["test1", "test2", "test3", "test4", "test5"]
    for text in texts:
        res = client.post("/predict", json={"text": text})
        assert res.status_code == 200
        assert res.json()["input"] == text


def test_predict_whitespace_variations():
    """Test with various whitespace patterns."""
    res1 = client.post("/predict", json={"text": "hello world"})
    res2 = client.post("/predict", json={"text": "hello  world"})
    res3 = client.post("/predict", json={"text": "hello\tworld"})
    assert all(r.status_code == 200 for r in [res1, res2, res3])


def test_predict_confidence_is_float():
    """Test that confidence is always a float."""
    res = client.post("/predict", json={"text": "test"})
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data["confidence"], (int, float))
    assert 0 <= data["confidence"] <= 1
