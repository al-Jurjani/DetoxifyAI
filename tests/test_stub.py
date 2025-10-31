# tests/test_stub.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_predict():
    res = client.post("/predict", json={"text": "hello"})
    assert res.status_code == 200
    data = res.json()
    assert "prediction" in data
    assert data["prediction"] in ["toxic", "non-toxic"]
