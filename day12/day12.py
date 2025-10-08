# What is Hugging Face Datasets?

# The datasets library is like a giant toy box of ready-to-use datasets. You can:
# Load datasets instantly (IMDB, SST-2, MNIST, etc.)

# Sample or split data easily (train/test)
# Process data in batches for fast training or analysis
# Basically, it saves you from downloading CSVs and cleaning data manually.

# Load the IMDB dataset
# IMDB is a movie review dataset with:
# text → the review itself
# label → 0 (negative) or 1 (positive)

from datasets import load_dataset

# Load the IMDB train dataset
dataset = load_dataset("imdb", split="train")

# Check total number of reviews
print(f"Total reviews in train set: {len(dataset)}")

# Look at the first review
print(dataset[0])


# ✅ Output example:
{'text': "I loved this movie...", 'label': 1}


# Summary :

# datasets library → easy access to ready datasets
# Load IMDB → get reviews & labels easily
# Batch sentiment analysis → use pretrained models to analyze multiple reviews quickly
# Random sampling → see a subset of data without reading everything