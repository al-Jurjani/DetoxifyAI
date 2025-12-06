"""
Simple tests to cover the real prediction code path (lines 188-203 in main.py).
Uses direct module patching without complex Azure mocking.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import Mock
from fastapi.testclient import TestClient
import numpy as np


def test_predict_real_path_toxic():
    """Test the real prediction code path with toxic result."""
    # Import after sys.path is set
    from app import main

    # Create simple mocks
    mock_model = Mock()
    mock_model.predict = Mock(return_value=np.array([1]))  # Toxic
    mock_model.predict_proba = Mock(return_value=np.array([[0.25, 0.75]]))  # 75% toxic

    mock_vectorizer = Mock()
    mock_vectorizer.transform = Mock(return_value=np.array([[0.5, 0.5]]))

    # Save originals
    original_model = main.model
    original_vectorizer = main.vectorizer
    original_loaded = main.model_loaded

    try:
        # Patch the module globals
        main.model = mock_model
        main.vectorizer = mock_vectorizer
        main.model_loaded = True

        # Create client and make request
        client = TestClient(main.app)
        response = client.post("/predict", json={"text": "you are terrible"})

        # Verify response
        assert response.status_code == 200
        data = response.json()

        # Check all fields in the response (covers lines 195-201)
        assert data["input"] == "you are terrible"
        assert data["prediction"] == "toxic"
        assert data["confidence"] == 0.75
        assert data["toxic_probability"] == 0.75
        assert data["model_loaded"]

        # Verify the functions were called (covers lines 190-193)
        assert mock_vectorizer.transform.called
        assert mock_model.predict.called
        assert mock_model.predict_proba.called

    finally:
        # Restore
        main.model = original_model
        main.vectorizer = original_vectorizer
        main.model_loaded = original_loaded


def test_predict_real_path_non_toxic():
    """Test the real prediction code path with non-toxic result."""
    from app import main

    mock_model = Mock()
    mock_model.predict = Mock(return_value=np.array([0]))  # Non-toxic
    mock_model.predict_proba = Mock(return_value=np.array([[0.9, 0.1]]))  # 10% toxic

    mock_vectorizer = Mock()
    mock_vectorizer.transform = Mock(return_value=np.array([[0.3, 0.7]]))

    original_model = main.model
    original_vectorizer = main.vectorizer
    original_loaded = main.model_loaded

    try:
        main.model = mock_model
        main.vectorizer = mock_vectorizer
        main.model_loaded = True

        client = TestClient(main.app)
        response = client.post("/predict", json={"text": "have a wonderful day"})

        assert response.status_code == 200
        data = response.json()

        # Covers the "non-toxic" branch in line 197
        assert data["prediction"] == "non-toxic"
        assert data["confidence"] == 0.9  # 1 - 0.1
        assert data["toxic_probability"] == 0.1

    finally:
        main.model = original_model
        main.vectorizer = original_vectorizer
        main.model_loaded = original_loaded


def test_predict_exception_handling():
    """Test exception handling in prediction (lines 202-203)."""
    from app import main

    mock_model = Mock()
    # Make model.predict raise an exception
    mock_model.predict = Mock(side_effect=Exception("Model failed"))

    mock_vectorizer = Mock()
    mock_vectorizer.transform = Mock(return_value=[[0.5, 0.5]])

    original_model = main.model
    original_vectorizer = main.vectorizer
    original_loaded = main.model_loaded

    try:
        main.model = mock_model
        main.vectorizer = mock_vectorizer
        main.model_loaded = True

        client = TestClient(main.app)
        response = client.post("/predict", json={"text": "test"})

        # Should catch exception and return 500 (line 203)
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Prediction failed" in data["detail"]

    finally:
        main.model = original_model
        main.vectorizer = original_vectorizer
        main.model_loaded = original_loaded


def test_predict_preprocessing_called():
    """Test that preprocessing is called (line 190)."""
    from app import main

    mock_model = Mock()
    mock_model.predict = Mock(return_value=np.array([0]))
    mock_model.predict_proba = Mock(return_value=np.array([[0.8, 0.2]]))

    mock_vectorizer = Mock()
    mock_vectorizer.transform = Mock(return_value=np.array([[0.5, 0.5]]))

    original_model = main.model
    original_vectorizer = main.vectorizer
    original_loaded = main.model_loaded

    try:
        main.model = mock_model
        main.vectorizer = mock_vectorizer
        main.model_loaded = True

        client = TestClient(main.app)

        # Send text that needs preprocessing
        response = client.post(
            "/predict",
            json={"text": "Visit https://test.com @user #tag 123"},
        )

        assert response.status_code == 200

        # Verify vectorizer.transform was called (preprocessing happened)
        assert mock_vectorizer.transform.called
        call_args = mock_vectorizer.transform.call_args[0][0]

        # Should be a list with one preprocessed string
        assert isinstance(call_args, list)
        assert len(call_args) == 1

    finally:
        main.model = original_model
        main.vectorizer = original_vectorizer
        main.model_loaded = original_loaded


def test_predict_various_probabilities():
    """Test with various probability values to cover both branches."""
    from app import main

    test_cases = [
        # (prediction, toxic_prob, expected_prediction, expected_confidence)
        ([1], 0.8, "toxic", 0.8),
        ([0], 0.2, "non-toxic", 0.8),
        ([1], 1.0, "toxic", 1.0),
        ([0], 0.0, "non-toxic", 1.0),
        ([1], 0.55, "toxic", 0.55),
        ([0], 0.45, "non-toxic", 0.55),
    ]

    for pred, toxic_prob, expected_pred, expected_conf in test_cases:
        mock_model = Mock()
        mock_model.predict = Mock(return_value=np.array(pred))
        mock_model.predict_proba = Mock(return_value=np.array([[1 - toxic_prob, toxic_prob]]))

        mock_vectorizer = Mock()
        mock_vectorizer.transform = Mock(return_value=np.array([[0.5, 0.5]]))

        original_model = main.model
        original_vectorizer = main.vectorizer
        original_loaded = main.model_loaded

        try:
            main.model = mock_model
            main.vectorizer = mock_vectorizer
            main.model_loaded = True

            client = TestClient(main.app)
            response = client.post("/predict", json={"text": "test"})

            assert response.status_code == 200
            data = response.json()

            # Test both branches of line 197: "toxic" if prediction == 1 else "non-toxic"
            assert data["prediction"] == expected_pred

            # Test both branches of line 198: confidence calculation
            assert data["confidence"] == expected_conf
            assert data["toxic_probability"] == toxic_prob

        finally:
            main.model = original_model
            main.vectorizer = original_vectorizer
            main.model_loaded = original_loaded
