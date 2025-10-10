# task.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def load_pdf(path):
    loader = PyPDFLoader(path)
    return loader.load()


def split_documents(documents, chunk_size=800, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(documents)


def load_model(model_name="google/flan-t5-small"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model


def summarize_text(model, tokenizer, text):
    prompt = f"Summarize the following text:\n{text}"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        do_sample=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def summarize_document(path):
    documents = load_pdf(path)
    splits = split_documents(documents)
    tokenizer, model = load_model()

    summaries = [summarize_text(model, tokenizer, doc.page_content) for doc in splits]
    combined = " ".join(summaries)
    final_summary = summarize_text(model, tokenizer, combined)
    return final_summary


if __name__ == "__main__":
    print(summarize_document("sample.pdf"))
