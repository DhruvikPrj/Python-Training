# day8/task.py
from transformers import pipeline

def analyze_sentiment(text: str) -> dict:
    sentiment = pipeline("sentiment-analysis")
    return sentiment(text)[0]

def summarize_text(text: str, max_length: int = 50, min_length: int = 25) -> str:
    summarizer = pipeline("summarization")
    return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"]

def generate_text(prompt: str, max_length: int = 50, num_return_sequences: int = 1) -> str:
    generator = pipeline("text-generation")
    return generator(prompt, max_length=max_length, num_return_sequences=num_return_sequences)[0]["generated_text"]

if __name__ == "__main__":
    text = "I love Python and Hugging Face!"
    print("Sentiment:", analyze_sentiment(text))

    long_text = """
    Hugging Face is an amazing library that makes working with AI models super easy. 
    It allows you to do sentiment analysis, text generation, translation, and more, 
    all with just a few lines of code.It makes it much better than we expect.
    """
    print("Summary:", summarize_text(long_text))

    prompt = "Once upon a time, in a magical forest,"
    print("Generated story:", generate_text(prompt))
