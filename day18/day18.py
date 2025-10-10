# What are Embeddings?
#
# Embeddings are numerical representations of text.
# They capture the meaning of a sentence, paragraph, or document in a vector (list of numbers).
# Similar texts → vectors close in space.
# Useful for: search, clustering, recommendations, question-answering over documents.

# ======> Sentence Embeddings in Python
# LangChain supports multiple embedding models. For example, using HuggingFace:

from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Load a sentence embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 2. Convert text to vector
text = "I love Python programming."
vector = embeddings.embed_query(text)

print("Vector length:", len(vector))
print("First 5 values:", vector[:5])


# ========> Vector Stores
#
# Once you have embeddings, you need a fast way to search for similar vectors.
# FAISS is a popular library for this:
# Stores vectors efficiently.
# Can search for nearest neighbors quickly.
# Perfect for semantic search in documents.

# ==========> FAISS with LangChain
# from langchain.vectorstores import FAISS

# 1️⃣ Example documents
texts = [
    "Python is a programming language.",
    "LangChain is a framework for LLM apps.",
    "Embeddings help capture semantic meaning."
]

# 2️⃣ Convert to embeddings
doc_vectors = embeddings.embed_documents(texts)

# 3️⃣ Create FAISS index
vector_store = FAISS.from_texts(texts, embeddings)

# 4️⃣ Query by similarity
query = "Tell me about Python programming"
results = vector_store.similarity_search(query, k=2)  # top 2 similar docs

for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.page_content}")


# ========> Real Use Case Example

# Imagine a 2-page PDF:
# Load PDF → split into chunks.
# Create embeddings for each chunk.
# Store them in FAISS.
# Ask a question → find top chunks related to it.

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load PDF
loader = PyPDFLoader("/Users/m1macmini3/Desktop/Python/Python-Training/day18/sample.pdf")
docs = loader.load()

# Split into smaller chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Build FAISS vector store
vector_store = FAISS.from_documents(chunks, embeddings)

# Query
query = "What are the health benefits of exercise?"
results = vector_store.similarity_search(query, k=3)

for i, doc in enumerate(results, 1):
    print(f"Chunk {i}:\n{doc.page_content}\n{'-'*40}")
