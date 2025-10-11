# ==============================================
# 🧠 Mini Q&A Bot using RAG + Hugging Face
# Refactored for testable interactive loop
# ==============================================

import warnings
warnings.filterwarnings("ignore")  # suppress all warnings

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

# Load PDF, create embeddings, FAISS DB, LLM (same as before)
pdf_path = "sample.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
docs = splitter.split_documents(pages)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=512,
    temperature=0.2
)
llm = HuggingFacePipeline(pipeline=generator)

# Q&A function
def ask_question(query: str) -> str:
    results = db.similarity_search(query, k=2)
    if not results:
        return "No relevant information found."
    context = " ".join([r.page_content for r in results])
    prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
    return llm.invoke(prompt)

# Interactive function (testable)
def run_interactive_loop(input_func=input, print_func=print):
    while True:
        query = input_func("\nAsk a question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        print_func("\nAnswer:", ask_question(query))

# Only run interactively if executed directly
if __name__ == "__main__":
    run_interactive_loop()
