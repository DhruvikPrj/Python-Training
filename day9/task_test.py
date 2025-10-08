# day9/task_test.py
import pytest
from unittest.mock import patch, MagicMock
import requests
import day9.task as task
from requests.exceptions import RequestException

# -----------------------------
# 1️⃣ Test fetch_article success
# -----------------------------
@patch("day9.task.requests.get")
def test_fetch_article_success(mock_get):
    # Mock a successful Wikipedia response
    mock_response = MagicMock()
    mock_response.json.return_value = {"extract": "This is a test article about AI."}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    article = task.fetch_article("Artificial intelligence")
    assert article == "This is a test article about AI."
    mock_get.assert_called_once()  # Ensure HTTP GET was called

# -----------------------------
# 2️⃣ Test fetch_article failure
# -----------------------------
@patch("day9.task.requests.get")
def test_fetch_article_failure(mock_get):
    # Mock raising RequestException
    mock_get.side_effect = RequestException("Network error")

    article = task.fetch_article("Nonexistent topic")
    assert article is None
    mock_get.assert_called_once()

# -----------------------------
# 3️⃣ Test summarize_text
# -----------------------------
@patch("day9.task.pipeline")
def test_summarize_text(mock_pipeline):
    # Mock the Hugging Face summarizer
    mock_summarizer = MagicMock()
    mock_summarizer.return_value = [{"summary_text": "AI is the future."}]
    mock_pipeline.return_value = mock_summarizer

    text = "Some long text about AI that needs summarization."
    summary = task.summarize_text(text)
    assert summary == "AI is the future."
    mock_pipeline.assert_called_once_with("summarization", model="facebook/bart-large-cnn")

# -----------------------------
# 4️⃣ Test main function (success path)
# -----------------------------
@patch("day9.task.fetch_article")
@patch("day9.task.summarize_text")
def test_main_success(mock_summarize, mock_fetch):
    mock_fetch.return_value = "Article text about AI."
    mock_summarize.return_value = "Summary text about AI."

    # We can patch 'print' to avoid printing during tests
    with patch("builtins.print") as mock_print:
        task.main()
        # Check if prints were called for article and summary
        assert mock_print.call_count >= 2
        mock_fetch.assert_called_once()
        mock_summarize.assert_called_once_with("Article text about AI.")

# -----------------------------
# 5️⃣ Test main function (no article found)
# -----------------------------
@patch("day9.task.fetch_article")
def test_main_no_article(mock_fetch):
    mock_fetch.return_value = None
    with patch("builtins.print") as mock_print:
        task.main()
        mock_print.assert_any_call("No article found. Exiting.")
        mock_fetch.assert_called_once()
