# Hugging Face is like a giant library of smart robots that can understand and work with human language.

# The main library is called transformers. It allows you to:

# Use Pretrained Models
# They already learned a lot from huge amounts of text.
# Example: Sentiment analysis, summarization, question answering, translation.
# Tokenization
# Computers don’t understand words directly.
# Tokenizers break text into pieces (tokens) that models understand.
# Example: "I love Python" → ["I", "love", "Python"] → numbers [101, 1023, 564]
# Pipelines (easy mode)
# Think of it as a ready-made robot.
# You give text → it gives result.
# Example tasks:
# sentiment-analysis → Is this text positive or negative?
# summarization → Make long text shorter.
# translation → Convert English to French.
# text-generation → Write stories, code, etc.

from transformers import pipeline

# Create a robot for sentiment
sentiment_analyzer = pipeline("sentiment-analysis")
# "sentiment-analysis" → tells if a text is positive or negative.

# Ask robot to analyze text
result = sentiment_analyzer("worst language i used is Python!")[0]

#It returns the Tone : POSITIVE / NEGATIVE

print(result)
# Output: {'label': 'NEGATIVE', 'score': 0.9997904896736145}
