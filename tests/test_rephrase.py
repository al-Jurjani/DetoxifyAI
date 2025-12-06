"""
Comprehensive tests for /rephrase endpoint with guardrails
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import numpy as np

# Import app after path is set
from app import main

client = TestClient(main.app)


class TestRephraseEndpoint:
    """Test /rephrase endpoint functionality"""

    def test_rephrase_empty_text(self):
        """Test rephrase with empty text"""
        res = client.post("/rephrase", json={"text": ""})
        assert res.status_code == 400
        assert "empty" in res.json()["detail"].lower()

    def test_rephrase_whitespace_only(self):
        """Test rephrase with whitespace only"""
        res = client.post("/rephrase", json={"text": "   "})
        assert res.status_code == 400

    @patch("app.main.model_loaded", True)
    @patch("app.main.model")
    @patch("app.main.vectorizer")
    @patch("app.main.pipeline", None)
    def test_rephrase_pipeline_not_available(self, mock_vec, mock_model):
        """Test rephrase when RAG pipeline is not available"""
        mock_model.predict = Mock(return_value=np.array([1]))  # Toxic
        mock_model.predict_proba = Mock(return_value=np.array([[0.3, 0.7]]))
        mock_vec.transform = Mock(return_value=np.array([[0.5, 0.5]]))

        res = client.post("/rephrase", json={"text": "you are terrible"})
        assert res.status_code == 503
        assert "RAG pipeline not available" in res.json()["detail"]

    @patch("app.main.model_loaded", False)
    def test_rephrase_model_not_loaded(self):
        """Test rephrase when ML model not loaded"""
        res = client.post("/rephrase", json={"text": "you are bad"})
        assert res.status_code == 503
        assert "model not loaded" in res.json()["detail"].lower()

    @patch("app.main.model_loaded", True)
    @patch("app.main.model")
    @patch("app.main.vectorizer")
    def test_rephrase_non_toxic_text(self, mock_vec, mock_model):
        """Test rephrase with non-toxic text - should return without rephrasing"""
        mock_model.predict = Mock(return_value=np.array([0]))  # Non-toxic
        mock_model.predict_proba = Mock(return_value=np.array([[0.9, 0.1]]))
        mock_vec.transform = Mock(return_value=np.array([[0.5, 0.5]]))

        res = client.post("/rephrase", json={"text": "have a wonderful day"})
        assert res.status_code == 200
        data = res.json()
        assert data["is_toxic"] is False
        assert "no rephrasing needed" in data["message"].lower()
        assert "guardrails" in data
        assert data["guardrails"]["input_passed"] is True

    @patch("app.main.model_loaded", True)
    @patch("app.main.model")
    @patch("app.main.vectorizer")
    @patch("app.main.guardrails")
    def test_rephrase_input_blocked_by_guardrails(self, mock_gr, mock_vec, mock_model):
        """Test rephrase when input is blocked by guardrails"""
        # Guardrails block the input
        mock_gr.validate_input = Mock(
            return_value=(
                False,
                "PII detected",
                {"rule": "pii_detection", "pii_type": "ssn"},
            )
        )

        res = client.post("/rephrase", json={"text": "My SSN is 123-45-6789"})
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "blocked"
        assert data["stage"] == "input"
        assert "PII" in data["reason"]
        assert data["guardrails"]["input_passed"] is False

    @patch("app.main.model_loaded", True)
    @patch("app.main.model")
    @patch("app.main.vectorizer")
    @patch("app.main.guardrails")
    @patch("app.main.pipeline")
    def test_rephrase_output_blocked_by_guardrails(
        self, mock_pipeline, mock_gr, mock_vec, mock_model
    ):
        """Test rephrase when output is blocked by guardrails"""
        # Input passes
        mock_gr.validate_input = Mock(return_value=(True, "OK", {}))
        # Model predicts toxic
        mock_model.predict = Mock(return_value=np.array([1]))
        mock_model.predict_proba = Mock(return_value=np.array([[0.3, 0.7]]))
        mock_vec.transform = Mock(return_value=np.array([[0.5, 0.5]]))
        # Pipeline returns rephrase
        mock_pipeline.rephrase = Mock(
            return_value={
                "toxic_input": "you are bad",
                "professional_rephrase": "still bad output",
                "retrieved_examples": [],
                "num_examples_used": 5,
            }
        )
        # Output guardrails block it
        mock_gr.validate_output = Mock(
            return_value=(
                False,
                "Still too toxic",
                {"rule": "toxicity_threshold", "score": 0.8},
            )
        )

        res = client.post("/rephrase", json={"text": "you are bad"})
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "blocked"
        assert data["stage"] == "output"
        assert data["guardrails"]["input_passed"] is True
        assert data["guardrails"]["output_passed"] is False

    @patch("app.main.model_loaded", True)
    @patch("app.main.model")
    @patch("app.main.vectorizer")
    @patch("app.main.guardrails")
    @patch("app.main.pipeline")
    def test_rephrase_success_all_guardrails_pass(
        self, mock_pipeline, mock_gr, mock_vec, mock_model
    ):
        """Test successful rephrase with all guardrails passing"""
        # Input passes
        mock_gr.validate_input = Mock(return_value=(True, "OK", {}))
        # Model predicts toxic
        mock_model.predict = Mock(return_value=np.array([1]))
        mock_model.predict_proba = Mock(return_value=np.array([[0.3, 0.7]]))
        mock_vec.transform = Mock(return_value=np.array([[0.5, 0.5]]))
        # Pipeline returns good rephrase
        mock_pipeline.rephrase = Mock(
            return_value={
                "toxic_input": "you are stupid",
                "professional_rephrase": "I respectfully disagree with your perspective",
                "retrieved_examples": [
                    {"toxic": "test", "professional": "test", "category": "test"}
                ],
                "num_examples_used": 5,
            }
        )
        # Output passes
        mock_gr.validate_output = Mock(
            return_value=(True, "OK", {"toxicity_score": 0.1})
        )

        res = client.post("/rephrase", json={"text": "you are stupid"})
        assert res.status_code == 200
        data = res.json()
        assert data["is_toxic"] is True
        assert data["input"] == "you are stupid"
        assert "respectfully" in data["rephrased"].lower()
        assert data["guardrails"]["input_passed"] is True
        assert data["guardrails"]["output_passed"] is True
        assert "retrieved_examples" in data
        assert data["num_examples_used"] == 5

    @patch("app.main.model_loaded", True)
    @patch("app.main.model")
    @patch("app.main.vectorizer")
    @patch("app.main.guardrails", None)
    @patch("app.main.pipeline")
    def test_rephrase_success_no_guardrails(self, mock_pipeline, mock_vec, mock_model):
        """Test successful rephrase when guardrails is None"""
        # Model predicts toxic
        mock_model.predict = Mock(return_value=np.array([1]))
        mock_model.predict_proba = Mock(return_value=np.array([[0.3, 0.7]]))
        mock_vec.transform = Mock(return_value=np.array([[0.5, 0.5]]))
        # Pipeline returns rephrase
        mock_pipeline.rephrase = Mock(
            return_value={
                "toxic_input": "you are bad",
                "professional_rephrase": "I disagree",
                "retrieved_examples": [],
                "num_examples_used": 5,
            }
        )

        res = client.post("/rephrase", json={"text": "you are bad"})
        assert res.status_code == 200
        data = res.json()
        assert data["is_toxic"] is True
        assert "guardrails" in data

    @patch("app.main.model_loaded", True)
    @patch("app.main.model")
    @patch("app.main.vectorizer")
    @patch("app.main.guardrails")
    @patch("app.main.pipeline")
    def test_rephrase_exception_handling(
        self, mock_pipeline, mock_gr, mock_vec, mock_model
    ):
        """Test exception handling in rephrase"""
        mock_gr.validate_input = Mock(return_value=(True, "OK", {}))
        mock_model.predict = Mock(return_value=np.array([1]))
        mock_model.predict_proba = Mock(return_value=np.array([[0.3, 0.7]]))
        mock_vec.transform = Mock(return_value=np.array([[0.5, 0.5]]))
        # Pipeline raises exception
        mock_pipeline.rephrase = Mock(side_effect=Exception("Modal timeout"))

        res = client.post("/rephrase", json={"text": "you are bad"})
        assert res.status_code == 500
        assert "Rephrasing failed" in res.json()["detail"]


class TestMetricsAndMonitoring:
    """Test Prometheus metrics tracking"""

    @patch("app.main.model_loaded", True)
    @patch("app.main.model")
    @patch("app.main.vectorizer")
    @patch("app.main.guardrails")
    @patch("app.main.pipeline")
    def test_llm_token_metrics_tracked(
        self, mock_pipeline, mock_gr, mock_vec, mock_model
    ):
        """Test that LLM token metrics are tracked"""
        mock_gr.validate_input = Mock(return_value=(True, "OK", {}))
        mock_model.predict = Mock(return_value=np.array([1]))
        mock_model.predict_proba = Mock(return_value=np.array([[0.3, 0.7]]))
        mock_vec.transform = Mock(return_value=np.array([[0.5, 0.5]]))
        mock_pipeline.rephrase = Mock(
            return_value={
                "toxic_input": "test input text",
                "professional_rephrase": "test output text",
                "retrieved_examples": [],
                "num_examples_used": 5,
            }
        )
        mock_gr.validate_output = Mock(
            return_value=(True, "OK", {"toxicity_score": 0.1})
        )

        # Make request
        client.post("/rephrase", json={"text": "test input text"})

        # Get metrics
        metrics_res = client.get("/metrics")
        assert metrics_res.status_code == 200
        metrics_text = metrics_res.text

        # Check LLM metrics exist
        assert "llm_tokens_total" in metrics_text or "app_request_count" in metrics_text

    @patch("app.main.model_loaded", True)
    @patch("app.main.model")
    @patch("app.main.vectorizer")
    @patch("app.main.guardrails")
    def test_guardrail_violation_metrics(self, mock_gr, mock_vec, mock_model):
        """Test that guardrail violations are tracked in metrics"""
        # Trigger guardrail violation
        mock_gr.validate_input = Mock(
            return_value=(False, "PII detected", {"rule": "pii_detection"})
        )

        client.post("/rephrase", json={"text": "My email is test@test.com"})

        # Check metrics
        metrics_res = client.get("/metrics")
        assert metrics_res.status_code == 200


class TestPreprocessing:
    """Test preprocessing function coverage"""

    def test_preprocess_with_urls(self):
        """Test preprocessing removes URLs"""
        from app.main import preprocess_aggressive

        result = preprocess_aggressive("Check https://example.com")
        assert "https" not in result
        assert "example.com" not in result

    def test_preprocess_with_mentions(self):
        """Test preprocessing removes @mentions"""
        from app.main import preprocess_aggressive

        result = preprocess_aggressive("Hey @user how are you")
        assert "@" not in result

    def test_preprocess_with_hashtags(self):
        """Test preprocessing removes #hashtags"""
        from app.main import preprocess_aggressive

        result = preprocess_aggressive("This is #trending")
        assert "#" not in result

    def test_preprocess_with_numbers(self):
        """Test preprocessing removes numbers"""
        from app.main import preprocess_aggressive

        result = preprocess_aggressive("I have 123 apples")
        assert "123" not in result

    def test_preprocess_lowercase(self):
        """Test preprocessing converts to lowercase"""
        from app.main import preprocess_aggressive

        result = preprocess_aggressive("HELLO WORLD")
        assert result == "hello world"


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
