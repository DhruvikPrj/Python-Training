# test_text_analysis_api.py
from fastapi.testclient import TestClient
from day7.task import app

client = TestClient(app)

# --------------------------
# 1️⃣ Test Sentiment Endpoint
# --------------------------
def test_sentiment_positive():
    response = client.post(
        "/sentiment",
        json={"text": "I absolutely love this app! It's fast and fun to use."}
    )
    data = response.json()

    assert response.status_code == 200
    assert "label" in data
    assert data["label"] in ["POSITIVE", "NEGATIVE"]
    assert 0 <= data["score"] <= 1


def test_sentiment_negative():
    response = client.post(
        "/sentiment",
        json={"text": "This was the worst movie I have ever seen."}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["label"] in ["NEGATIVE", "POSITIVE"]
    assert 0 <= data["score"] <= 1


# --------------------------
# 2️⃣ Test Summary Endpoint
# --------------------------
def test_summary_basic():
    long_text = (
        "FastAPI is a modern Python web framework for building APIs quickly. "
        "It’s built on Starlette and Pydantic, offering high performance and great developer experience. "
        "It is used by developers worldwide to deploy machine learning and data applications."
    )

    response = client.post("/summary", json={"text": long_text})
    data = response.json()

    assert response.status_code == 200
    assert "summary" in data
    assert isinstance(data["summary"], str)
    assert len(data["summary"]) > 10


# --------------------------
# 3️⃣ Test Invalid Request Handling
# --------------------------
def test_invalid_request():
    response = client.post("/sentiment", json={})
    assert response.status_code == 422
