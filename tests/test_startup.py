"""
Tests for app startup, middleware, and Azure blob integration
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import pytest

from app import main

client = TestClient(main.app)


class TestAppStartup:
    """Test application startup logic"""

    @patch('app.main.AZURE_CONNECTION_STRING', '')
    def test_startup_no_azure_connection(self):
        """Test startup when Azure connection string is empty"""
        # App should still start without Azure
        res = client.get("/health")
        assert res.status_code == 200

    @patch('app.main.AZURE_CONNECTION_STRING', 'test_connection_string')
    @patch('app.main.BlobServiceClient')
    def test_startup_with_azure_connection(self, mock_blob_service):
        """Test startup with Azure connection string"""
        # Mock blob service
        mock_blob_service.from_connection_string = Mock(return_value=MagicMock())

        # App should initialize blob client
        res = client.get("/health")
        assert res.status_code == 200


class TestMiddleware:
    """Test middleware functionality"""

    def test_cors_middleware_active(self):
        """Test CORS middleware is active"""
        res = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert res.status_code == 200

    def test_prometheus_middleware_tracks_requests(self):
        """Test Prometheus middleware tracks requests"""
        # Make multiple requests
        for _ in range(5):
            client.get("/health")

        # Check metrics endpoint
        metrics = client.get("/metrics")
        assert metrics.status_code == 200
        assert "app_request_count" in metrics.text

    def test_request_latency_tracked(self):
        """Test request latency is tracked"""
        client.post("/predict", json={"text": "test"})

        metrics = client.get("/metrics")
        assert "app_request_latency_seconds" in metrics.text


class TestModelLoading:
    """Test model loading from Azure"""

    @patch('app.main.AZURE_CONNECTION_STRING', '')
    def test_model_loading_no_azure(self):
        """Test model loading when no Azure connection"""
        # Should work with mock responses
        res = client.post("/predict", json={"text": "hello"})
        assert res.status_code == 200
        data = res.json()
        assert data["model_loaded"] is False

    @patch('app.main.blob_service_client')
    def test_model_loading_blob_error(self, mock_blob):
        """Test model loading handles blob errors gracefully"""
        mock_blob.get_blob_client = Mock(side_effect=Exception("Blob error"))

        # App should still work with mock
        res = client.post("/predict", json={"text": "test"})
        assert res.status_code in [200, 503]  # Either mock or service unavailable


class TestErrorHandling:
    """Test error handling across endpoints"""

    def test_predict_invalid_json(self):
        """Test /predict with invalid JSON"""
        res = client.post("/predict", data="not json")
        assert res.status_code in [400, 422]

    def test_rephrase_invalid_json(self):
        """Test /rephrase with invalid JSON"""
        res = client.post("/rephrase", data="not json")
        assert res.status_code in [400, 422]

    def test_predict_missing_text_field(self):
        """Test /predict with missing text field"""
        res = client.post("/predict", json={})
        assert res.status_code == 422

    def test_rephrase_missing_text_field(self):
        """Test /rephrase with missing text field"""
        res = client.post("/rephrase", json={})
        assert res.status_code == 422


class TestEndpointVariations:
    """Test various input scenarios for better coverage"""

    def test_predict_long_text(self):
        """Test /predict with very long text"""
        long_text = "test " * 500
        res = client.post("/predict", json={"text": long_text})
        assert res.status_code == 200

    def test_predict_special_characters(self):
        """Test /predict with special characters"""
        res = client.post("/predict", json={"text": "!@#$%^&*()"})
        assert res.status_code == 200

    def test_predict_unicode(self):
        """Test /predict with unicode characters"""
        res = client.post("/predict", json={"text": "Hello 你好 مرحبا"})
        assert res.status_code == 200

    def test_predict_with_newlines(self):
        """Test /predict with newlines"""
        res = client.post("/predict", json={"text": "Line 1\nLine 2\nLine 3"})
        assert res.status_code == 200

    def test_predict_with_tabs(self):
        """Test /predict with tabs"""
        res = client.post("/predict", json={"text": "Word1\tWord2\tWord3"})
        assert res.status_code == 200


class TestMetricsEndpoint:
    """Test Prometheus metrics endpoint"""

    def test_metrics_endpoint_format(self):
        """Test metrics endpoint returns correct format"""
        res = client.get("/metrics")
        assert res.status_code == 200
        # Just check it's text/plain, version can vary
        assert "text/plain" in res.headers["content-type"]
        assert "charset=utf-8" in res.headers["content-type"]

    def test_metrics_contains_custom_metrics(self):
        """Test metrics endpoint contains custom metrics"""
        res = client.get("/metrics")
        text = res.text

        # Should have our custom metrics
        assert "app_request_count" in text
        assert "app_request_latency_seconds" in text

    def test_metrics_after_multiple_requests(self):
        """Test metrics accumulate after multiple requests"""
        # Make several requests
        for i in range(10):
            client.get("/health")
            client.post("/predict", json={"text": f"test {i}"})

        res = client.get("/metrics")
        assert res.status_code == 200
        # Metrics should show activity
        assert "app_request_count" in res.text


class TestRootEndpoint:
    """Test root endpoint variations"""

    def test_root_returns_correct_structure(self):
        """Test root endpoint returns correct structure"""
        res = client.get("/")
        assert res.status_code == 200
        data = res.json()
        assert "message" in data
        assert "model_loaded" in data
        assert isinstance(data["model_loaded"], bool)

    def test_root_message_content(self):
        """Test root endpoint message content"""
        res = client.get("/")
        data = res.json()
        assert "DetoxifyAI" in data["message"]

    def test_root_with_query_params(self):
        """Test root endpoint ignores query params"""
        res = client.get("/?test=123")
        assert res.status_code == 200


class TestHealthEndpoint:
    """Test health endpoint variations"""

    def test_health_always_returns_ok(self):
        """Test health endpoint always returns ok"""
        for _ in range(5):
            res = client.get("/health")
            assert res.status_code == 200
            data = res.json()
            assert data["status"] == "ok"

    def test_health_includes_model_status(self):
        """Test health endpoint includes model loaded status"""
        res = client.get("/health")
        data = res.json()
        assert "model_loaded" in data
        assert isinstance(data["model_loaded"], bool)

    def test_health_with_query_params(self):
        """Test health endpoint ignores query params"""
        res = client.get("/health?check=full")
        assert res.status_code == 200


class TestPreprocessFunction:
    """Test preprocess_aggressive function comprehensively"""

    def test_preprocess_empty_string(self):
        """Test preprocessing empty string"""
        from app.main import preprocess_aggressive
        result = preprocess_aggressive("")
        assert result == ""

    def test_preprocess_only_whitespace(self):
        """Test preprocessing only whitespace"""
        from app.main import preprocess_aggressive
        result = preprocess_aggressive("   \t\n  ")
        assert len(result.strip()) == 0

    def test_preprocess_removes_multiple_urls(self):
        """Test preprocessing removes multiple URLs"""
        from app.main import preprocess_aggressive
        text = "Check https://site1.com and http://site2.org"
        result = preprocess_aggressive(text)
        assert "https" not in result
        assert "http" not in result

    def test_preprocess_removes_punctuation(self):
        """Test preprocessing removes punctuation"""
        from app.main import preprocess_aggressive
        result = preprocess_aggressive("Hello! How are you?")
        assert "!" not in result
        assert "?" not in result

    def test_preprocess_normalizes_whitespace(self):
        """Test preprocessing normalizes whitespace"""
        from app.main import preprocess_aggressive
        result = preprocess_aggressive("Hello    world   test")
        assert "  " not in result  # No double spaces

    def test_preprocess_complex_text(self):
        """Test preprocessing complex text"""
        from app.main import preprocess_aggressive
        text = "Hey @user123! Check https://test.com #cool 999 times!!!"
        result = preprocess_aggressive(text)
        # Should be cleaned
        assert "@" not in result
        assert "#" not in result
        assert "https" not in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
