import pytest
from unittest.mock import patch, MagicMock
import os
import task  # your actual module

# -----------------------------
# Mock file reading
# -----------------------------
@patch("task.os.listdir")
@patch("builtins.open")
def test_file_reading(mock_open, mock_listdir):
    # Setup
    mock_listdir.return_value = ["file1.txt", "file2.txt", "ignore.me"]
    mock_file = MagicMock()
    mock_file.read.side_effect = ["Content of file1", "Content of file2"]
    mock_open.return_value.__enter__.return_value = mock_file

    # Execute file reading logic
    texts = []
    file_mapping = []
    for file_name in os.listdir("texts"):
        if file_name.endswith(".txt"):
            path = os.path.join("texts", file_name)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                texts.append(content)
                file_mapping.append(file_name)

    # Assertions
    assert texts == ["Content of file1", "Content of file2"]
    assert file_mapping == ["file1.txt", "file2.txt"]
    mock_open.assert_any_call(os.path.join("texts", "file1.txt"), "r", encoding="utf-8")
    mock_open.assert_any_call(os.path.join("texts", "file2.txt"), "r", encoding="utf-8")


# -----------------------------
# Mock embeddings & FAISS
# -----------------------------
@patch("task.HuggingFaceEmbeddings")
@patch("task.FAISS.from_texts")
def test_faiss_index_and_query(mock_faiss, mock_embeddings):
    # Mock embeddings object
    mock_embeddings_instance = MagicMock()
    mock_embeddings.return_value = mock_embeddings_instance

    # Mock FAISS vector store
    mock_vector_store = MagicMock()
    mock_faiss.return_value = mock_vector_store

    texts = ["Text A", "Text B"]
    file_mapping = ["fileA.txt", "fileB.txt"]

    vector_store = task.FAISS.from_texts(
        texts, mock_embeddings_instance, metadatas=[{"file": f} for f in file_mapping]
    )

    # Assertions
    mock_faiss.assert_called_once()
    assert vector_store == mock_vector_store

    # Mock similarity_search result
    mock_result = MagicMock()
    mock_result.metadata = {"file": "fileA.txt"}
    mock_result.page_content = "Text A content here"
    mock_vector_store.similarity_search.return_value = [mock_result]

    # Execute query
    query = "Which file talks about AI?"
    results = vector_store.similarity_search(query, k=1)

    # Assertions
    mock_vector_store.similarity_search.assert_called_once_with(query, k=1)
    assert results[0].metadata["file"] == "fileA.txt"
    assert "Text A content" in results[0].page_content


# -----------------------------
# Edge case: empty folder
# -----------------------------
def test_empty_file_list(monkeypatch):
    # Simulate empty folder
    monkeypatch.setattr(task.os, "listdir", lambda _: [])
    texts = []
    file_mapping = []

    for file_name in task.os.listdir("texts"):
        if file_name.endswith(".txt"):
            path = os.path.join("texts", file_name)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                texts.append(content)
                file_mapping.append(file_name)

    assert texts == []
    assert file_mapping == []
