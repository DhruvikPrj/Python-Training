import pytest
from unittest.mock import MagicMock, patch
from task import (
    load_pdf, split_documents, load_model,
    summarize_text, summarize_document
)
from langchain.schema import Document


# ---------- Fixtures ----------

@pytest.fixture
def mock_docs():
    """Simulate 2-page PDF with fake content."""
    return [
        Document(page_content="Python is great for AI."),
        Document(page_content="LangChain helps build LLM workflows.")
    ]


@pytest.fixture
def mock_model_tokenizer():
    """Mock tokenizer & model so we don't download them."""
    mock_tokenizer = MagicMock()
    mock_tokenizer.return_tensors = "pt"
    mock_tokenizer.decode.return_value = "Mock summary"
    mock_tokenizer.side_effect = lambda *args, **kwargs: {"input_ids": [1, 2, 3]}

    mock_model = MagicMock()
    mock_model.generate.return_value = [[0, 1, 2, 3]]

    return mock_model, mock_tokenizer


# ---------- Tests ----------

def test_load_pdf(monkeypatch, mock_docs):
    """Ensure PDF loading works (mocked)."""
    mock_loader = MagicMock()
    mock_loader.load.return_value = mock_docs

    monkeypatch.setattr("task.PyPDFLoader", lambda _: mock_loader)
    docs = load_pdf("fake.pdf")

    assert len(docs) == 2
    assert "Python" in docs[0].page_content


def test_split_documents(mock_docs):
    """Verify splitting into chunks."""
    splits = split_documents(mock_docs, chunk_size=100, chunk_overlap=10)
    assert isinstance(splits, list)
    assert all(hasattr(doc, "page_content") for doc in splits)


@patch("task.AutoTokenizer.from_pretrained")
@patch("task.AutoModelForSeq2SeqLM.from_pretrained")
def test_load_model(mock_model, mock_tokenizer):
    """Test model/tokenizer loading."""
    mock_model.return_value = "fake_model"
    mock_tokenizer.return_value = "fake_tokenizer"

    tokenizer, model = load_model("google/flan-t5-small")
    assert tokenizer == "fake_tokenizer"
    assert model == "fake_model"
    mock_model.assert_called_once()


def test_summarize_text(mock_model_tokenizer):
    """Check summarization function logic."""
    model, tokenizer = mock_model_tokenizer
    result = summarize_text(model, tokenizer, "Test text")
    assert isinstance(result, str)
    assert "Mock summary" in result


@patch("task.load_pdf")
@patch("task.split_documents")
@patch("task.load_model")
@patch("task.summarize_text")
def test_summarize_document(mock_sum, mock_load_model, mock_split, mock_load_pdf, mock_docs):
    """Full pipeline test.sh — ensures chain of calls works."""
    mock_load_pdf.return_value = mock_docs
    mock_split.return_value = mock_docs
    mock_load_model.return_value = ("mock_tokenizer", "mock_model")
    mock_sum.side_effect = ["Summary 1", "Summary 2", "Final Summary"]

    result = summarize_document("sample.pdf")

    assert result == "Final Summary"
    assert mock_sum.call_count == 3
    mock_load_pdf.assert_called_once()
    mock_split.assert_called_once()
    mock_load_model.assert_called_once()
