# day8/task_test.py
import pytest
from unittest.mock import patch, MagicMock
from . import task  # relative import works

@patch("day8.task.pipeline")
def test_analyze_sentiment(mock_pipeline):
    # pipeline() returns a callable
    mock_sentiment = MagicMock()
    mock_sentiment.return_value = [{"label": "POSITIVE", "score": 0.99}]
    mock_pipeline.return_value = mock_sentiment

    result = task.analyze_sentiment("I love Python and Hugging Face!")
    assert result["label"] == "POSITIVE"
    assert result["score"] == 0.99

@patch("day8.task.pipeline")
def test_summarize_text(mock_pipeline):
    mock_summarizer = MagicMock()
    mock_summarizer.return_value = [{"summary_text": "Hugging Face is amazing for AI models."}]
    mock_pipeline.return_value = mock_summarizer

    summary = task.summarize_text("Some text")
    assert summary == "Hugging Face is amazing for AI models."

@patch("day8.task.pipeline")
def test_generate_text(mock_pipeline):
    mock_generator = MagicMock()
    mock_generator.return_value = [{"generated_text": "Once upon a time, a unicorn appeared."}]
    mock_pipeline.return_value = mock_generator

    story = task.generate_text("Prompt")
    assert story.startswith("Once upon a time")
