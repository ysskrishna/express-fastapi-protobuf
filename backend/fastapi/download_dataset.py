#!/usr/bin/env python3
"""
Download the english_quotes dataset from Hugging Face and save it locally as JSON.
"""
import json
from datasets import load_dataset
import os

DATASET_FILE = os.path.join(os.path.dirname(__file__), "quotes.json")

def download_dataset():
    """Download dataset from Hugging Face and save to local JSON file"""
    print("Downloading quotes dataset from Hugging Face...")
    try:
        dataset = load_dataset("Abirate/english_quotes", split="train")
        quotes = [item for item in dataset]
        
        print(f"Downloaded {len(quotes)} quotes")
        print(f"Saving to {DATASET_FILE}...")
        
        with open(DATASET_FILE, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Dataset saved successfully to {DATASET_FILE}")
        print(f"  Total quotes: {len(quotes)}")
        return True
    except Exception as e:
        print(f"✗ Error downloading dataset: {e}")
        return False

if __name__ == "__main__":
    success = download_dataset()
    exit(0 if success else 1)
