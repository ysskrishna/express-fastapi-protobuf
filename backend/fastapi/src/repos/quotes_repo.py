import os
import json
from typing import List, Dict

# Path helpers: quotes.json lives in backend/fastapi/quotes.json (two levels above src)
# quotes_repo.py is at backend/fastapi/src/repos/quotes_repo.py, so go up three dirs to reach backend/fastapi
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATASET_FILE = os.path.join(BASE_DIR, "quotes.json")

quotes_data: List[Dict] = []

async def load_quotes() -> None:
    """Load quotes from local JSON file into memory."""
    global quotes_data
    try:
        if not os.path.exists(DATASET_FILE):
            print(f"✗ Error: Dataset file not found: {DATASET_FILE}")
            quotes_data = []
            return
        with open(DATASET_FILE, "r", encoding="utf-8") as f:
            quotes_data = json.load(f)
        print(f"✓ Loaded {len(quotes_data)} quotes from {DATASET_FILE}")
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        quotes_data = []

def get_all_quotes() -> List[Dict]:
    return quotes_data

