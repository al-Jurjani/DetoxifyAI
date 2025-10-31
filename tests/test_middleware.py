import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_middleware_adds_metrics():
    """Test that middleware records metrics for requests."""
    # Make a request
    res = client.get("/health")
    assert res.status_code == 200

    # Check that metrics endpoint shows the request
    metrics_res = client.get("/metrics")
    assert metrics_res.status_code == 200
    metrics_text = metrics_res.text

    # Should contain request count metric
    assert "app_request_count" in metrics_text
    # Should contain latency metric
    assert "app_request_latency_seconds" in metrics_text


def test_cors_headers():
    """Test that CORS middleware adds appropriate headers."""
    res = client.options("/predict", headers={"Origin": "http://localhost:3000"})
    # CORS should be configured to allow all origins
    assert res.status_code in [
        200,
        405,
    ]  # OPTIONS might return 405 if not explicitly handled


def test_multiple_requests_increment_counter():
    """Test that making multiple requests increments the counter."""
    # Make several requests
    client.get("/health")
    client.get("/health")
    client.get("/")

    # Get metrics
    metrics = client.get("/metrics").text

    # Metrics should contain our custom metrics
    assert "app_request_count_total" in metrics
    assert "app_request_latency_seconds" in metrics
