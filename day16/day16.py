# =======> Prompt Templates:
# A Prompt Template is a reusable prompt with dynamic placeholders. Instead of hardcoding everything, you can insert variables at runtime.

from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["name", "topic"],
    template="Hello {name}, can you tell me something interesting about {topic}?"
)

# Run with variables
result = prompt.format(name="Dhruvik", topic="AI with Python")
print(result)


# Explanation:

# input_variables: List of placeholders you will replace dynamically.
# template: The actual text with placeholders in {}.
# format(...): Fill in the placeholders at runtime.

# =======> Sequential Chains

# A Sequential Chain is when you combine multiple LLM prompts in sequence.
# Each chain’s output can become the next chain’s input.

# Imagine a workflow:

# Summarize a text.
# Translate the summary to French.
# Rewrite the translation politely.

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def run_text2text(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.7
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

prompt = "Summarize the following text: Staying active and eating healthy are crucial steps towards maintaining a healthy weight and improving overall well-being. By following a healthy lifestyle, one can enhance their physical, mental, and emotional health, leading to a better quality of life. In this article, we will explore the benefits of staying active and eating healthy and provide tips to incorporate these habits into your daily routine."
print(run_text2text(prompt))
