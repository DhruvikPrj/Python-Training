# test_task.py
import pytest
from unittest.mock import patch, MagicMock
import task

# ------------------------------
# 1️⃣ Test ask_question
# ------------------------------
@patch("task.db")
@patch("task.llm")
def test_ask_question_returns_answer(mock_llm, mock_db):
    mock_result = MagicMock()
    mock_result.page_content = "LangChain is a framework for LLM apps."
    mock_db.similarity_search.return_value = [mock_result]
    mock_llm.invoke.return_value = "LangChain helps build LLM-based applications."

    result = task.ask_question("What is LangChain?")
    mock_db.similarity_search.assert_called_once_with("What is LangChain?", k=2)
    mock_llm.invoke.assert_called_once()
    assert "LangChain" in result

@patch("task.db")
def test_ask_question_no_pdf_uploaded(mock_db):
    # simulate db not set
    task.db = None
    result = task.ask_question("Anything?")
    assert result == "No PDF uploaded yet."

@patch("task.db")
@patch("task.llm")
def test_ask_question_no_results(mock_llm, mock_db):
    mock_db.similarity_search.return_value = []
    result = task.ask_question("Random question?")
    assert result == "No relevant information found."

# ------------------------------
# 2️⃣ Test process_pdf (mock loader/FAISS)
# ------------------------------
@patch("task.PyPDFLoader")
@patch("task.RecursiveCharacterTextSplitter")
@patch("task.HuggingFaceEmbeddings")
@patch("task.FAISS")
def test_process_pdf(mock_faiss, mock_emb, mock_splitter, mock_loader):
    mock_loader.return_value.load.return_value = ["page 1 text", "page 2 text"]
    mock_splitter.return_value.split_documents.return_value = ["chunk1", "chunk2"]
    task.process_pdf("dummy.pdf")
    mock_faiss.from_documents.assert_called_once()

# ------------------------------
# 3️⃣ Test internal ask_question behavior
# ------------------------------
@patch("task.db")
def test_similarity_search_called(mock_db):
    mock_db.similarity_search.return_value = []
    task.db = mock_db
    task.llm = MagicMock()
    task.ask_question("Test query")
    mock_db.similarity_search.assert_called_once()

# ------------------------------
# 4️⃣ Test interactive simulation (simulate upload + ask)
# ------------------------------
@patch("task.process_pdf")
@patch("task.ask_question", return_value="AI stands for Artificial Intelligence")
def test_upload_and_ask(mock_ask, mock_process_pdf):
    # simulate PDF upload
    mock_process_pdf("dummy.pdf")
    res = task.ask_question("What is AI?")
    assert "Artificial Intelligence" in res
