# task.py
import warnings
warnings.filterwarnings("ignore")  # suppress LangChain deprecation warnings

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline
from typing import Optional

# Global DB variable
db: Optional[FAISS] = None

# ------------------------------
# Define LLM
# ------------------------------
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=512,
    temperature=0.2
)
llm = HuggingFacePipeline(pipeline=generator)


# ------------------------------
# Q&A function
# ------------------------------
def ask_question(query: str) -> str:
    global db
    if not db:
        return "No PDF uploaded yet."

    results = db.similarity_search(query, k=2)
    if not results:
        return "No relevant information found."

    context = " ".join([r.page_content for r in results])
    prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
    return llm.invoke(prompt)


# ------------------------------
# PDF processing
# ------------------------------
def process_pdf(file_path: str):
    global db
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    docs = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200).split_documents(pages)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)
