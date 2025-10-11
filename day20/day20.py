# What is RAG (Retrieval-Augmented Generation)?

# RAG = Retrieval-Augmented Generation
# It’s a technique to make Large Language Models (LLMs) smarter by connecting them to your external knowledge (like PDFs, documents, websites, databases, etc.).

# ==============================================
# ✅ RAG Example using Hugging Face LLM (No OpenAI)
# ==============================================

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

# Step 1️⃣: Documents
docs = [
    "AI helps automate repetitive tasks.",
    "Python is used for AI and data science.",
]

# Step 2️⃣: Create embeddings (text → vectors)
embeddings = HuggingFaceEmbeddings(model_name="google/flan-t5-small")


# Step 3️⃣: Create FAISS vector store
db = FAISS.from_texts(docs, embeddings)

# Step 4️⃣: Query for retrieval
query = "How current USA market now?"
results = db.similarity_search(query, k=1)

# Step 5️⃣: Prepare context for LLM
context = results[0].page_content
prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"

# Step 6️⃣: Load Hugging Face model as an LLM
# Using a small model for demo — replace with any other HF model
generator = pipeline(
    "text-generation",
    model="distilgpt2",  # ⚡ lightweight open model
    # model="mistralai/Mistral-7B-Instruct-v0.2",
    max_length=800,
    temperature=0.7,
    do_sample=True
)

# Wrap it with LangChain for uniform interface
hf_llm = HuggingFacePipeline(pipeline=generator)

# Step 7️⃣: Generate answer
response = hf_llm.invoke(prompt)

# Step 8️⃣: Display
print("Prompt:\n", prompt)
print("\nGenerated Answer:\n", response)
