# ======> Explanation:

# PyPDFLoader :
# Reads PDF files and extracts text from each page.
# Returns a list of Document objects.
# Each document contains a .page_content (text) and .metadata (like page number).

# RecursiveCharacterTextSplitter :
# Splits large text into smaller chunks (e.g., 800 characters per chunk with 200 overlap).
# Why? LLMs work better with small chunks of text. Too large → memory or token limits.

# HuggingFaceEmbeddings :
# Converts text chunks into vector embeddings (numerical representation of meaning).
# Embeddings let us measure semantic similarity between a question and document content.

# FAISS :
# A fast, in-memory vector database.
# Stores embeddings.
# Supports similarity search: “Which chunks are most relevant to my question?”

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

pdf_path = "/Users/m1macmini3/Desktop/Python/Python-Training/day21/sample111.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load()  # Extract text

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
docs = splitter.split_documents(pages)  # Split into manageable chunks

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)  # Store embeddings in FAISS


# PyPDFLoader → read PDF → pages = list of text per page.
#
# split_documents → break large text into smaller chunks → docs.
#
# HuggingFaceEmbeddings → convert each chunk into a vector (numerical semantic representation).
#
# FAISS.from_documents → store all vectors → allows semantic search later.

# Ask Question → Get Context-Based Answer
# Goal: User asks a question, and we return an answer based on the uploaded PDF content.

from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

# Define LLM
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",  # LLM suitable for Q&A
    max_length=512,
    temperature=0.2
)
llm = HuggingFacePipeline(pipeline=generator)

# Explanation:

# pipeline (Transformers) :
# A wrapper to run pre-trained LLMs easily.
# text2text-generation means the model takes a text prompt and outputs text response.
# max_length → max tokens in output.
# temperature → randomness of output; lower → more deterministic answers.

# HuggingFacePipeline (LangChain) :
# Wraps the HuggingFace pipeline to integrate with LangChain seamlessly.
# Makes it compatible with LangChain prompt handling.

def ask_question(query: str) -> str:
    results = db.similarity_search(query, k=2)  # Retrieve top 2 most relevant chunks
    if not results:
        return "No relevant information found."

    context = " ".join([r.page_content for r in results])  # Combine chunks
    prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"
    return llm.invoke(prompt)  # Generate answer from LLM

# Line by line explanation:

# db.similarity_search(query, k=2) :
# Converts the query into an embedding.
# Finds 2 closest chunks in FAISS based on cosine similarity.

# context = " ".join(...) :
# Combines text from the most relevant chunks into one string.
# This ensures LLM sees contextual info from the PDF.

# prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:" :
# Creates a prompt for the LLM: “Here’s the context, answer the user’s question.”

# llm.invoke(prompt) :
# LLM generates an answer based on the context.
# Returns the answer as a string.

answer = ask_question("Who is Robbert?")
print(answer)
