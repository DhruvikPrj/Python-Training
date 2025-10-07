# What is BERT?

# BERT (Bidirectional Encoder Representations from Transformers) is a powerful NLP model by Google.
# It understands the context of words in both directions (left & right).
# Pros: Very accurate.
# Cons: Heavy & slow, especially on CPUs.

# What is DistilBERT?

# DistilBERT is a smaller, faster version of BERT created using a process called knowledge distillation.
# It keeps ~97% of BERT’s performance but is ~60% faster and smaller in size.
# Pros: Fast, lightweight.
# Cons: Slightly less accurate than BERT.

# ===> Key Idea: If you care about speed (real-time APIs, lots of data), use DistilBERT. If you need max accuracy, use BERT.

# Caching Models

# Hugging Face models are downloaded the first time from the model hub.
# After that, they are stored locally in a cache folder (~/.cache/huggingface/transformers/).
# When you load the same model next time, it uses cached files, so it’s much faster.
# Tip: Always reuse the model object instead of loading it multiple times for inference.