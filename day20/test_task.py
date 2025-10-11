import warnings
import importlib
from unittest.mock import patch, MagicMock
import pytest

# Silence deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import task

# ------------------------------
# 1️⃣ Test ask_question
# ------------------------------
@patch("task.db")
@patch("task.llm")
def test_ask_question_returns_answer(mock_llm, mock_db):
    mock_result = MagicMock()
    mock_result.page_content = "AI helps automate repetitive tasks."
    mock_db.similarity_search.return_value = [mock_result]
    mock_llm.invoke.return_value = "AI improves automation by handling repetitive tasks efficiently."

    query = "How does AI improve automation?"
    answer = task.ask_question(query)

    mock_db.similarity_search.assert_called_once_with(query, k=2)
    mock_llm.invoke.assert_called_once()
    assert "automation" in answer.lower()


@patch("task.db")
@patch("task.llm")
def test_empty_context_handled(mock_llm, mock_db):
    mock_db.similarity_search.return_value = []
    mock_llm.invoke.return_value = "No relevant information found."

    result = task.ask_question("Random unrelated question?")
    assert "information" in result.lower()

# ------------------------------
# 2️⃣ Test interactive loop
# ------------------------------
def test_run_interactive(monkeypatch):
    inputs = iter(["What is AI?", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    printed = []
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(" ".join(map(str, args))))

    # Patch ask_question to avoid heavy LLM call
    with patch("task.ask_question", return_value="AI stands for Artificial Intelligence."):
        task.run_interactive_loop(input_func=input, print_func=print)

    assert any("Answer:" in p for p in printed)
    assert any("AI stands for Artificial Intelligence." in p for p in printed)

# ------------------------------
# 3️⃣ Test similarity_search is called
# ------------------------------
@patch("task.db")
def test_similarity_search_called(mock_db):
    mock_db.similarity_search.return_value = []
    task.db = mock_db
    task.llm = MagicMock()
    task.ask_question("Test query")
    mock_db.similarity_search.assert_called_once()
