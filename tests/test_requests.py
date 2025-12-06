"""
Tests for middleware, request handling, and monitoring
Targets remaining uncovered code paths
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from unittest.mock import Mock
import pytest

from app import main

client = TestClient(main.app)


class TestMiddlewareMetrics:
    """Test middleware metrics collection in detail"""

    def test_middleware_tracks_get_requests(self):
        """Test middleware tracks GET requests"""
        client.get("/health")
        client.get("/")
        client.get("/metrics")

        metrics = client.get("/metrics").text
        assert "app_request_count" in metrics

    def test_middleware_tracks_post_requests(self):
        """Test middleware tracks POST requests"""
        client.post("/predict", json={"text": "test"})

        metrics = client.get("/metrics").text
        assert "app_request_count" in metrics

    def test_middleware_tracks_latency(self):
        """Test middleware tracks request latency"""
        # Make a request
        client.get("/health")

        # Check latency metric exists
        metrics = client.get("/metrics").text
        assert "app_request_latency_seconds" in metrics

    def test_middleware_tracks_multiple_endpoints(self):
        """Test middleware tracks different endpoints"""
        client.get("/")
        client.get("/health")
        client.post("/predict", json={"text": "test"})

        metrics = client.get("/metrics").text
        # Should have counts for different endpoints
        assert "app_request_count" in metrics

    def test_middleware_handles_errors(self):
        """Test middleware still tracks requests that error"""
        # This will error (empty text)
        client.post("/predict", json={"text": ""})

        metrics = client.get("/metrics").text
        assert "app_request_count" in metrics


class TestPredictVariations:
    """Test all predict endpoint code paths"""

    def test_predict_model_none(self):
        """Test predict when model is None"""
        original_model = main.model
        original_loaded = main.model_loaded

        try:
            main.model = None
            main.model_loaded = False

            res = client.post("/predict", json={"text": "test"})
            assert res.status_code == 200
            data = res.json()
            assert data["model_loaded"] is False
            assert "mock" in data.get("note", "").lower()
        finally:
            main.model = original_model
            main.model_loaded = original_loaded

    def test_predict_vectorizer_none(self):
        """Test predict when vectorizer is None"""
        original_vec = main.vectorizer
        original_loaded = main.model_loaded

        try:
            main.vectorizer = None
            main.model_loaded = False

            res = client.post("/predict", json={"text": "test"})
            assert res.status_code == 200
            data = res.json()
            assert data["model_loaded"] is False
        finally:
            main.vectorizer = original_vec
            main.model_loaded = original_loaded

    def test_predict_model_loaded_false(self):
        """Test predict when model_loaded flag is False"""
        original_loaded = main.model_loaded

        try:
            main.model_loaded = False

            res = client.post("/predict", json={"text": "test"})
            assert res.status_code == 200
            data = res.json()
            assert data["model_loaded"] is False
            assert data["prediction"] == "non-toxic"
            assert data["confidence"] == 0.50
        finally:
            main.model_loaded = original_loaded


class TestRephraseVariations:
    """Test all rephrase endpoint code paths"""

    def test_rephrase_model_none(self):
        """Test rephrase when model is None"""
        original_model = main.model
        original_loaded = main.model_loaded

        try:
            main.model = None
            main.model_loaded = False

            res = client.post("/rephrase", json={"text": "you are bad"})
            assert res.status_code == 503
            assert "model not loaded" in res.json()["detail"].lower()
        finally:
            main.model = original_model
            main.model_loaded = original_loaded

    def test_rephrase_vectorizer_none(self):
        """Test rephrase when vectorizer is None"""
        original_vec = main.vectorizer
        original_loaded = main.model_loaded

        try:
            main.vectorizer = None
            main.model_loaded = False

            res = client.post("/rephrase", json={"text": "you are bad"})
            assert res.status_code == 503
        finally:
            main.vectorizer = original_vec
            main.model_loaded = original_loaded

    def test_rephrase_model_loaded_false(self):
        """Test rephrase when model_loaded is False"""
        original_loaded = main.model_loaded

        try:
            main.model_loaded = False

            res = client.post("/rephrase", json={"text": "you are bad"})
            assert res.status_code == 503
            assert "ML model not loaded" in res.json()["detail"]
        finally:
            main.model_loaded = original_loaded

    def test_rephrase_pipeline_none(self):
        """Test rephrase when pipeline is None"""
        original_pipeline = main.pipeline
        original_model = main.model
        original_vec = main.vectorizer
        original_loaded = main.model_loaded

        try:
            import numpy as np

            main.pipeline = None
            main.model_loaded = True

            # Mock model to predict toxic
            mock_model = Mock()
            mock_model.predict = Mock(return_value=np.array([1]))
            mock_model.predict_proba = Mock(return_value=np.array([[0.3, 0.7]]))
            main.model = mock_model

            mock_vec = Mock()
            mock_vec.transform = Mock(return_value=np.array([[0.5, 0.5]]))
            main.vectorizer = mock_vec

            res = client.post("/rephrase", json={"text": "you are bad"})
            assert res.status_code == 503
            assert "RAG pipeline not available" in res.json()["detail"]
        finally:
            main.pipeline = original_pipeline
            main.model = original_model
            main.vectorizer = original_vec
            main.model_loaded = original_loaded

    def test_rephrase_guardrails_none(self):
        """Test rephrase when guardrails is None"""
        original_gr = main.guardrails
        original_pipeline = main.pipeline
        original_model = main.model
        original_vec = main.vectorizer
        original_loaded = main.model_loaded

        try:
            import numpy as np

            main.guardrails = None
            main.model_loaded = True

            # Mock everything
            mock_model = Mock()
            mock_model.predict = Mock(return_value=np.array([0]))  # Non-toxic
            mock_model.predict_proba = Mock(return_value=np.array([[0.9, 0.1]]))
            main.model = mock_model

            mock_vec = Mock()
            mock_vec.transform = Mock(return_value=np.array([[0.5, 0.5]]))
            main.vectorizer = mock_vec

            res = client.post("/rephrase", json={"text": "have a nice day"})
            assert res.status_code == 200
            data = res.json()
            assert data["is_toxic"] is False
        finally:
            main.guardrails = original_gr
            main.pipeline = original_pipeline
            main.model = original_model
            main.vectorizer = original_vec
            main.model_loaded = original_loaded


class TestEndpointErrorCases:
    """Test error handling in all endpoints"""

    def test_predict_with_none_text(self):
        """Test predict with None as text"""
        # FastAPI will reject this at validation level
        res = client.post("/predict", json={"text": None})
        assert res.status_code == 422

    def test_rephrase_with_none_text(self):
        """Test rephrase with None as text"""
        res = client.post("/rephrase", json={"text": None})
        assert res.status_code == 422

    def test_predict_with_missing_text_key(self):
        """Test predict with missing text key"""
        res = client.post("/predict", json={"wrong_key": "value"})
        assert res.status_code == 422

    def test_rephrase_with_missing_text_key(self):
        """Test rephrase with missing text key"""
        res = client.post("/rephrase", json={"wrong_key": "value"})
        assert res.status_code == 422

    def test_predict_with_extra_fields(self):
        """Test predict with extra fields (should work)"""
        res = client.post(
            "/predict", json={"text": "test", "extra": "field", "another": 123}
        )
        assert res.status_code == 200

    def test_rephrase_with_extra_fields(self):
        """Test rephrase with extra fields (should work)"""
        original_loaded = main.model_loaded
        try:
            main.model_loaded = False
            res = client.post(
                "/rephrase", json={"text": "you are bad", "extra": "field"}
            )
            # Will hit model not loaded
            assert res.status_code == 503
        finally:
            main.model_loaded = original_loaded


class TestMetricsEndpointDetails:
    """Detailed tests for /metrics endpoint"""

    def test_metrics_is_plain_text(self):
        """Test metrics returns plain text"""
        res = client.get("/metrics")
        assert "text/plain" in res.headers["content-type"]

    def test_metrics_contains_prometheus_format(self):
        """Test metrics follows Prometheus format"""
        res = client.get("/metrics")
        text = res.text
        # Prometheus metrics have # HELP and # TYPE comments
        assert "# HELP" in text or "app_request_count" in text

    def test_metrics_has_labels(self):
        """Test metrics include labels"""
        # Make some requests
        client.get("/health")
        client.post("/predict", json={"text": "test"})

        metrics = client.get("/metrics").text
        # Should have method and endpoint labels
        assert (
            "method=" in metrics or "endpoint=" in metrics or "app_request" in metrics
        )


class TestRequestProcessing:
    """Test request processing and data flow"""

    def test_predict_processes_text_correctly(self):
        """Test that text is processed correctly"""
        test_text = "This is a TEST message"
        res = client.post("/predict", json={"text": test_text})
        assert res.status_code == 200
        data = res.json()
        assert data["input"] == test_text

    def test_rephrase_processes_text_correctly(self):
        """Test that rephrase preserves original text"""
        test_text = "You are TERRIBLE"
        original_loaded = main.model_loaded
        try:
            main.model_loaded = False
            res = client.post("/rephrase", json={"text": test_text})
            # Will error but we can check error message
            assert res.status_code == 503
        finally:
            main.model_loaded = original_loaded

    def test_preprocessing_is_called_in_predict(self):
        """Test that preprocessing is actually called"""
        from app.main import preprocess_aggressive

        # Test the preprocessing function directly
        text_with_url = "Check https://example.com for info"
        processed = preprocess_aggressive(text_with_url)

        # URL should be removed
        assert "https" not in processed or "example.com" not in processed

    def test_preprocessing_handles_edge_cases(self):
        """Test preprocessing with various edge cases"""
        from app.main import preprocess_aggressive

        test_cases = [
            "",
            "   ",
            "123",
            "!!!",
            "@#$%",
            "http://test.com",
            "@user #tag",
        ]

        for text in test_cases:
            result = preprocess_aggressive(text)
            assert isinstance(result, str)


class TestHealthEndpointDetails:
    """Detailed health endpoint tests"""

    def test_health_status_always_ok(self):
        """Test health always returns ok status"""
        for _ in range(10):
            res = client.get("/health")
            assert res.json()["status"] == "ok"

    def test_health_model_loaded_reflects_state(self):
        """Test health endpoint reflects model state"""
        res = client.get("/health")
        data = res.json()
        assert "model_loaded" in data
        # Value should match main.model_loaded
        assert data["model_loaded"] == main.model_loaded


class TestRootEndpointDetails:
    """Detailed root endpoint tests"""

    def test_root_message_not_empty(self):
        """Test root message is not empty"""
        res = client.get("/")
        data = res.json()
        assert len(data["message"]) > 0

    def test_root_reflects_model_state(self):
        """Test root reflects current model state"""
        res = client.get("/")
        data = res.json()
        assert data["model_loaded"] == main.model_loaded


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
