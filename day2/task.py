# day2/task.py
from transformers import pipeline
import requests

def fetch_article(topic: str) -> str:
    """Fetch Wikipedia summary for the given topic."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.strip().replace(' ', '_')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        return None
    return data.get("extract")

def summarize_text(text: str) -> str:
    """Summarize text using Hugging Face pipeline."""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=60, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

def main():
    # Hardcoded topic instead of asking user input
    topic = "Artificial intelligence"
    article = fetch_article(topic)
    if not article:
        print("No article found. Exiting.")
        return
    summary = summarize_text(article)
    print("\n🔹 Original Article:\n", article)
    print("\n🔸 Summary (2 sentences):\n", summary)

if __name__ == "__main__":
    main()
