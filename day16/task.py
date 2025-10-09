from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Choose model (small = faster; base = smarter)
model_name = "google/flan-t5-small"
# model_name = "google/flan-t5-base"  # You can switch later

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def run_text2text(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        temperature=0.7,
        do_sample=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def summarize_and_extract_keywords(text):
    # Step 1: Summarize
    summary_prompt = f"Summarize the following text:\n{text}"
    summary = run_text2text(summary_prompt)

    # Step 2: Extract keywords
    keyword_prompt = f"Extract 5 important keywords from this summary:\n{summary}"
    keywords = run_text2text(keyword_prompt)

    return summary, keywords


text = """
Staying active and eating healthy are crucial steps towards maintaining a healthy weight 
and improving overall well-being. By following a healthy lifestyle, one can enhance 
their physical, mental, and emotional health, leading to a better quality of life. 
In this article, we will explore the benefits of staying active and eating healthy 
and provide tips to incorporate these habits into your daily routine.
"""

summary, keywords = summarize_and_extract_keywords(text)

print("\n📝 Summary:\n", summary)
print("\n🔑 Keywords:\n", keywords)


