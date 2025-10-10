# sentence-transformers: Used to generate embeddings from text.
# faiss-cpu (or faiss-gpu if you have CUDA): For fast vector search.
# langchain: Provides nice wrappers for embeddings and FAISS integration.

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

# 1️⃣ Read text files
folder_path = "texts"
file_names = os.listdir(folder_path)

texts = []
file_mapping = []

for file_name in file_names:
    if file_name.endswith(".txt"):
        path = os.path.join(folder_path, file_name)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            texts.append(content)
            file_mapping.append(file_name)

# 2️⃣ Load embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 3️⃣ Create FAISS vector store
vector_store = FAISS.from_texts(texts, embeddings, metadatas=[{"file": f} for f in file_mapping])

# 4️⃣ Query
query = "Which file talks about AI?"
results = vector_store.similarity_search(query, k=1)

# 5️⃣ Show results
for result in results:
    print("Matching File:", result.metadata["file"])
    print("Content Preview:", result.page_content[:200], "...")


# ========> Explanation of Concepts

# Embeddings

# Transform text into numbers (vectors).
# Capture semantic meaning, not just keywords.

# FAISS

# A library optimized for fast similarity search on vectors.
# Great for semantic search over many documents.

# Querying

# Your question is also converted to a vector.
# FAISS finds the nearest document vectors.
# Returns the most relevant file(s) for your question.

# Metadatas

# Stores extra info with each vector.
# Useful to know which file or document the vector belongs to.