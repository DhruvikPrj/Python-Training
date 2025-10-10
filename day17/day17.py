# What is a Document Loader?

# A Document Loader helps you read files (like .pdf, .txt, .docx, .csv, etc.) and turn them into text documents that LangChain can process.

# Each document is represented as:

# Document(page_content="actual text", metadata={"source": "filename"})
# 🔹 Example Types of Loaders
# File Type	        Loader

# PDF	            PyPDFLoader
# TXT	            TextLoader
# DOCX	            Docx2txtLoader
# HTML	            UnstructuredHTMLLoader
# Website URL	    UnstructuredURLLoader

# ========> Load a TXT file

from langchain_community.document_loaders import TextLoader

loader = TextLoader("/Users/m1macmini3/Desktop/Python/Python-Training/day17/sample.txt")
documents = loader.load()

print(f"Loaded {len(documents)} document(s).")
print("\n📄 Content Preview:\n", documents[0].page_content[:500])


# ========> Load a PDF file
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("/Users/m1macmini3/Desktop/Python/Python-Training/day17/sample.pdf")
documents = loader.load()

print(f"Loaded {len(documents)} pages from PDF.")
print("\n📄 Page 1 Preview:\n", documents[0].page_content[:500])

# ========> Split Long Documents

# Why split?
# → LLMs (like FLAN-T5 or GPT) have a token limit (e.g., 512–2048 tokens).
# So for big PDFs, we divide them into smaller chunks.

from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
splits = splitter.split_documents(documents)

print(f"Total chunks created: {len(splits)}")
print("\n📑 First Chunk:\n", splits[0].page_content)


# Explanation:

# chunk_size: Max characters per piece
# chunk_overlap: Helps preserve context between chunks

# ========> Summarize the Documents

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def run_text2text(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        do_sample=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Create a Summarization Chain
# For each document chunk, we’ll ask the model to summarize.

def summarize_documents(docs):
    summaries = []
    for i, doc in enumerate(docs):
        prompt = f"Summarize the following text:\n{doc.page_content}"
        summary = run_text2text(prompt)
        summaries.append(summary)
        print(f"\n✅ Summary {i+1}:\n{summary}\n{'-'*60}")
    return summaries


summaries = summarize_documents(splits[:3])  # summarize first 3 chunks

# =========> Combine Summaries
# If your document is large, you can combine chunk summaries into one “meta summary”.

combined_text = " ".join(summaries)
final_summary = run_text2text(f"Summarize this overall summary:\n{combined_text}")

print("\n📘 Final Document Summary:\n", final_summary)


