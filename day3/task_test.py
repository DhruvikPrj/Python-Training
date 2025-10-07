# test_sentiment_api.py

import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(__file__))  # add current folder
from task import app  # now it should work


# Create a TestClient instance
client = TestClient(app)

def test_positive_sentiment():
    response = client.post("/analyze", json={"text": "I love Python and Hugging Face!"})
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "score" in data
    assert data["label"] in ["POSITIVE", "NEGATIVE"]
    assert 0 <= data["score"] <= 1

def test_negative_sentiment():
    response = client.post("/analyze", json={"text": "I hate waiting in long lines."})
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "score" in data
    assert data["label"] in ["POSITIVE", "NEGATIVE"]
    assert 0 <= data["score"] <= 1

def test_empty_text():
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 200  # Hugging Face can still handle empty string
    data = response.json()
    assert "label" in data
    assert "score" in data

def test_missing_text_field():
    response = client.post("/analyze", json={})
    assert response.status_code == 422  # FastAPI validation error for missing field
