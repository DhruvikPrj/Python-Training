# test_task.sh.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from task import generate_answer
from task import app  # Make sure your FastAPI app file is named task.py

client = TestClient(app)


def test_qa_success():
    """Test normal Q&A flow"""
    with patch("task.generate_answer") as mock_generate:
        mock_generate.return_value = "AI is Artificial Intelligence"
        response = client.post("/qa", json={"text": "What is AI?"})
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "AI is Artificial Intelligence"
        mock_generate.assert_called_once_with("What is AI?")


def test_qa_empty_input():
    """Test empty input returns 400"""
    response = client.post("/qa", json={"text": "   "})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Text cannot be empty"


def test_qa_missing_text_key():
    """Test missing 'text' key in JSON"""
    response = client.post("/qa", json={})
    # FastAPI/Pydantic returns 422 for missing required fields
    assert response.status_code == 422


def test_qa_model_exception():
    """Test exception inside generate_answer"""
    with patch("task.generate_answer") as mock_generate:
        mock_generate.side_effect = Exception("Model failed")
        response = client.post("/qa", json={"text": "Explain Python."})
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "Model failed"


def test_response_model_structure():
    """Ensure response always has 'answer' key with string type"""
    with patch("task.generate_answer") as mock_generate:
        mock_generate.return_value = "Test answer"
        response = client.post("/qa", json={"text": "Hello"})
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert isinstance(data["answer"], str)


def test_non_json_request():
    """Test sending invalid request content type"""
    response = client.post("/qa", data="Just a string")
    # FastAPI expects JSON, returns 422 Unprocessable Entity
    assert response.status_code == 422


def test_long_text_input():
    """Test handling of long input text"""
    long_text = "AI " * 1000
    expected_text = long_text.strip()
    with patch("task.generate_answer") as mock_generate:
        mock_generate.return_value = "AI is everywhere"
        response = client.post("/qa", json={"text": long_text})
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "AI is everywhere"
        mock_generate.assert_called_once_with(expected_text)



def test_generate_answer_empty_direct():
    """Test ValueError raised when calling generate_answer directly with empty string"""
    with pytest.raises(ValueError, match="Input text is empty."):
        generate_answer("   ")

def test_generate_answer_normal_direct():
    """Test normal generate_answer returns a string"""
    result = generate_answer("What is AI?")
    assert isinstance(result, str)
    assert len(result) > 0
