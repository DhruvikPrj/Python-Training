import requests
from transformers import pipeline

# Hugging Face summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# --- Example: Wikipedia article text ---
article_text = """
Python is an interpreted, high-level and general-purpose programming language. 
Created by Guido van Rossum and first released in 1991, Python’s design philosophy 
emphasizes code readability with its notable use of significant indentation. 
Its language constructs and object-oriented approach aim to help programmers 
write clear, logical code for small and large-scale projects.
"""

summary_local = summarizer(article_text, max_length=60, min_length=30, do_sample=False)
print("🔹 Original Text:\n", article_text)
print("\n🔸 Summary:\n", summary_local[0]['summary_text'])


# --- Custom Input: Wikipedia summary ---
url = "https://en.wikipedia.org/api/rest_v1/page/summary/OpenAI"

# Add User-Agent header to avoid 403
headers = {"User-Agent": "Mozilla/5.0 (compatible; Python script)"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
        article = data.get("extract", "")
        print("\nOriginal length:", len(article))

        if article:
            summary = summarizer(article, max_length=60, min_length=30, do_sample=False)
            print("\n🔸 Summary:", summary[0]['summary_text'])
        else:
            print("No text found in Wikipedia summary.")
    except requests.JSONDecodeError:
        print("Error: Response is not valid JSON:", response.text)
else:
    print(f"Failed to fetch Wikipedia page. Status code: {response.status_code}")
