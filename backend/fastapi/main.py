import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import Response as FastAPIResponse
from typing import List, Dict
import sys
import os
import json

# Add proto directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Import generated protobuf code
try:
    from quote_pb2 import QuoteRequest, QuoteResponse, Quote, TagsRequest, TagsResponse, TagInfo
except ImportError:
    print("Error: quote_pb2.py not found. Run 'make proto' first.")
    sys.exit(1)

app = FastAPI(title="Quote Recommender API")

# Path to local dataset file
DATASET_FILE = os.path.join(os.path.dirname(__file__), "quotes.json")

# Load quotes dataset on startup
quotes_data: List[Dict] = []

@app.on_event("startup")
async def load_quotes():
    """Load quotes from local JSON file"""
    global quotes_data
    try:
        if not os.path.exists(DATASET_FILE):
            print(f"✗ Error: Dataset file not found: {DATASET_FILE}")
            print("  Please ensure quotes.json exists in the fastapi directory")
            quotes_data = []
            return
        
        print(f"Loading quotes from local file: {DATASET_FILE}")
        with open(DATASET_FILE, 'r', encoding='utf-8') as f:
            quotes_data = json.load(f)
        print(f"✓ Loaded {len(quotes_data)} quotes")
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        quotes_data = []

@app.post("/quotes")
async def get_quotes(request: Request) -> Response:
    """Get quotes by tag with pagination (protobuf)"""
    # Read binary protobuf data
    body = await request.body()
    
    # Deserialize QuoteRequest
    quote_request = QuoteRequest()
    quote_request.ParseFromString(body)
    
    tag = quote_request.tag
    page = quote_request.page if quote_request.page > 0 else 1
    page_size = quote_request.page_size if quote_request.page_size > 0 else 10
    
    # Filter quotes by tag
    matching_quotes = []
    for idx, quote_item in enumerate(quotes_data):
        quote_tags = quote_item.get("tags", [])
        if tag.lower() in [t.lower() for t in quote_tags]:
            matching_quotes.append({
                "id": idx + 1,
                "text": quote_item.get("quote", ""),
                "author": quote_item.get("author", ""),
                "tags": quote_tags
            })
    
    # Apply pagination
    total_count = len(matching_quotes)
    total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 1
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_quotes = matching_quotes[start_idx:end_idx]
    
    # Build protobuf response
    response = QuoteResponse()
    response.tag = tag
    response.total_count = total_count
    response.page = page
    response.page_size = page_size
    response.total_pages = total_pages
    
    for q in paginated_quotes:
        quote_msg = Quote()
        quote_msg.id = q["id"]
        quote_msg.text = q["text"]
        quote_msg.author = q["author"]
        quote_msg.tags.extend(q["tags"])
        response.quotes.append(quote_msg)
    
    # Serialize and return binary response
    return FastAPIResponse(
        content=response.SerializeToString(),
        media_type="application/x-protobuf"
    )

@app.post("/tags")
async def get_tags(request: Request) -> Response:
    """Get tags with counts (protobuf) - supports search and limit"""
    # Read binary protobuf data
    body = await request.body()
    
    # Deserialize TagsRequest
    tags_request = TagsRequest()
    tags_request.ParseFromString(body)
    
    search_query = tags_request.search.lower() if tags_request.search else ""
    limit = tags_request.limit if tags_request.limit > 0 else 0
    
    # Calculate tag counts from all quotes
    tag_counts: Dict[str, int] = {}
    
    for quote_item in quotes_data:
        quote_tags = quote_item.get("tags", [])
        for tag in quote_tags:
            tag_lower = tag.lower()
            tag_counts[tag_lower] = tag_counts.get(tag_lower, 0) + 1
    
    # Filter by search query if provided
    if search_query:
        filtered_tags = {
            name: count for name, count in tag_counts.items()
            if search_query in name
        }
        tag_counts = filtered_tags
    
    # Sort by count (descending), then by name
    sorted_tags = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Apply limit if specified
    if limit > 0:
        sorted_tags = sorted_tags[:limit]
    
    # Build protobuf response
    response = TagsResponse()
    response.total_tags = len(tag_counts)  # Total before limit
    
    for tag_name, count in sorted_tags:
        tag_info = TagInfo()
        tag_info.name = tag_name
        tag_info.count = count
        response.tags.append(tag_info)
    
    # Serialize and return binary response
    return FastAPIResponse(
        content=response.SerializeToString(),
        media_type="application/x-protobuf"
    )

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "quotes_loaded": len(quotes_data)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
