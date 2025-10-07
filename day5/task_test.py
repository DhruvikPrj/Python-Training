# test_task.py
import pytest
from transformers import pipeline

@pytest.fixture(scope="module")
def sentiment_analyzer():
    # Create the sentiment pipeline once for all tests
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        truncation=True
    )

def test_positive_sentiment(sentiment_analyzer):
    text = "I love Python and Hugging Face!"
    result = sentiment_analyzer(text)[0]
    assert "label" in result
    assert "score" in result
    assert result["label"] in ["POSITIVE", "NEGATIVE"]
    assert 0.0 <= result["score"] <= 1.0

def test_negative_sentiment(sentiment_analyzer):
    text = "I hate rainy days and long queues."
    result = sentiment_analyzer(text)[0]
    assert "label" in result
    assert "score" in result
    assert result["label"] in ["POSITIVE", "NEGATIVE"]
    assert 0.0 <= result["score"] <= 1.0

def test_truncation_long_text(sentiment_analyzer):
    long_text = "Python is amazing. " * 1000  # very long text
    result = sentiment_analyzer(long_text)[0]
    assert "label" in result
    assert "score" in result
    assert result["label"] in ["POSITIVE", "NEGATIVE"]
    assert 0.0 <= result["score"] <= 1.0

def test_empty_text(sentiment_analyzer):
    text = ""
    result = sentiment_analyzer(text)[0]
    # Should still return something (DistilBERT handles empty string)
    assert "label" in result
    assert "score" in result
