# Quote Recommender - Node.js + FastAPI + Protobuf

## Overview
A Quote Recommender app demonstrating microservice communication between Vue.js, Node.js, and FastAPI using Protocol Buffers.

## Data Source
**Hugging Face: english_quotes** (CC BY 4.0)
- URL: https://huggingface.co/datasets/Abirate/english_quotes
- **2,508 quotes** from Goodreads
- **Fields**: `quote`, `author`, `tags` (multi-label array)
- **Format**: JSONL
- Example tags: `inspirational`, `life`, `love`, `humor`, `philosophy`

## Use Case
User selects a tag (e.g., "inspirational", "life", "love") in Vue → Node.js forwards request to FastAPI → FastAPI finds matching quotes and returns them via protobuf → Displayed in Vue.

## Architecture

```
┌──────────────┐     JSON/HTTP      ┌──────────────┐     Protobuf      ┌──────────────┐
│              │  ───────────────►  │              │  ───────────────► │              │
│   Vue.js     │  GET /quotes?tag=  │   Node.js    │  Binary payload   │   FastAPI    │
│   Frontend   │  ◄───────────────  │   (BFF)      │  ◄─────────────── │  (Quotes DB) │
│  (Port 5173) │     JSON array     │ (Port 3000)  │  Binary response  │ (Port 8000)  │
└──────────────┘                    └──────────────┘                   └──────────────┘
```

**Flow:**
1. Vue sends `GET /api/quotes?tag=motivation&page=1&page_size=10` to Node.js
2. Node.js serializes request to protobuf, sends to FastAPI
3. FastAPI searches quotes by tag with pagination, returns protobuf response
4. Node.js deserializes, sends JSON to Vue
5. Vue displays the quotes with pagination controls

**Tags Endpoint Flow:**
1. Vue sends `GET /api/tags` to Node.js
2. Node.js serializes empty `TagsRequest` to protobuf, sends to FastAPI
3. FastAPI calculates all tags and their counts, returns protobuf `TagsResponse`
4. Node.js deserializes protobuf response, sends JSON to Vue
5. Vue displays tags with counts

## Project Structure

```
nodejs-fastapi-protobuf/
├── backend/
│   ├── common/
│   │   └── proto/
│   │       └── quote.proto    # Shared protobuf schema
│   ├── fastapi/
│   │   ├── pyproject.toml     # uv project config
│   │   ├── main.py            # FastAPI server (loads HuggingFace dataset)
│   │   └── quote_pb2.py       # Generated protobuf code
│   └── nodejs/
│       ├── index.js           # Express BFF server
│       └── package.json
├── client/
│   └── vue-frontend/
│       ├── src/
│       │   ├── App.vue        # Main component
│       │   └── main.js
│       ├── index.html
│       └── package.json
└── Makefile                   # Build, setup, and run commands
```

## Implementation Steps

### 1. Proto Schema (`backend/common/proto/quote.proto`)

**Note:** All quote-related messages (quotes, tags) are in a single proto file since they're tightly coupled - tags are metadata derived from quotes.
```protobuf
syntax = "proto3";

// Request to get quotes by tag (with pagination)
message QuoteRequest {
  string tag = 1;
  int32 page = 2;          // Page number (1-indexed)
  int32 page_size = 3;     // Items per page
}

// A single quote
message Quote {
  int32 id = 1;
  string text = 2;
  string author = 3;
  repeated string tags = 4;
}

// Response containing quotes (with pagination metadata)
message QuoteResponse {
  repeated Quote quotes = 1;
  string tag = 2;
  int32 total_count = 3;      // Total quotes matching the tag
  int32 page = 4;             // Current page number
  int32 page_size = 5;        // Items per page
  int32 total_pages = 6;      // Total number of pages
}

// Request to get tags and their counts (empty - no params needed)
message TagsRequest {
  // Empty - no parameters needed
}

// A single tag with its count
message TagInfo {
  string name = 1;
  int32 count = 2;           // Number of quotes with this tag
}

// Response containing all tags with counts
message TagsResponse {
  repeated TagInfo tags = 1;
  int32 total_tags = 2;      // Total number of unique tags
}
```

### 2. FastAPI Service (`backend/fastapi/`)
- Load quotes using HuggingFace `datasets` library
- **Endpoints:**
  - `POST /quotes` - accepts protobuf `QuoteRequest`, returns `QuoteResponse` (paginated)
  - `POST /tags` - accepts protobuf `TagsRequest`, returns `TagsResponse` (calculates tags and counts)
- **Logic:**
  - `/quotes`: Filter quotes by tag, apply pagination (page, page_size), return paginated results
  - `/tags`: **Process all quotes**, extract unique tags, count occurrences per tag, return sorted by count

### 3. Node.js Service (`backend/nodejs/`)
- Express server on port 3000
- **Endpoints:**
  - `GET /api/quotes?tag=inspirational&page=1&page_size=10` - get quotes by tag (paginated)
  - `GET /api/tags` - get all tags with counts (serializes `TagsRequest` to protobuf, forwards to FastAPI)
- **Role:** Pure BFF (Backend for Frontend) - serializes/deserializes protobuf, no business logic
- **All FastAPI communication uses protobuf:**
  - Serializes request to protobuf binary, sends to FastAPI
  - Receives protobuf binary response from FastAPI
  - Deserializes protobuf response, converts to JSON for Vue

### 4. Vue Frontend (`client/vue-frontend/`)
- **Tag selector** - dynamically loaded from `/api/tags` endpoint, shows tag name and count
- **Quote cards** - display quote text, author name, tags as badges
- **Pagination controls** - Previous/Next buttons, page numbers, shows "Page X of Y"
- Minimal styling with CSS

## Files to Create

| File | Purpose |
|------|---------|
| `backend/common/proto/quote.proto` | Protobuf schema for quotes and tags |
| `backend/fastapi/pyproject.toml` | uv project config (fastapi, uvicorn, protobuf, datasets) |
| `backend/fastapi/main.py` | FastAPI with protobuf endpoints (quotes, tags) |
| `backend/nodejs/index.js` | Express BFF server with protobuf serialization |
| `backend/nodejs/package.json` | Node deps (express, protobufjs, axios) |
| `client/vue-frontend/src/App.vue` | Vue UI with tag selector, quote cards, and pagination |
| `client/vue-frontend/package.json` | Vue deps |
| `Makefile` | Build commands: setup, proto, start, stop |

## Verification

### Quick Start (using Make)
```bash
make setup    # Install all dependencies (uv sync, npm install)
make proto    # Generate protobuf code
make start    # Start all 3 services
make stop     # Stop all services
```

### Manual Start
1. Generate protobuf code:
   ```bash
   # For Python (FastAPI)
   protoc --python_out=backend/fastapi backend/common/proto/quote.proto

   # For Node.js (optional - can use protobufjs dynamically)
   protoc --js_out=import_style=commonjs:backend/nodejs backend/common/proto/quote.proto
   ```

2. Start FastAPI:
   ```bash
   cd backend/fastapi && uv sync && uv run uvicorn main:app --reload --port 8000
   ```

3. Start Node.js:
   ```bash
   cd backend/nodejs && npm install && node index.js
   ```

4. Start Vue:
   ```bash
   cd client/vue-frontend && npm install && npm run dev
   ```

### Test the App
Open http://localhost:5173:
- Tags load automatically from `/api/tags`
- Click a tag → quotes load with pagination
- Use pagination controls to navigate pages

## Design Decisions

### 1. Tags Endpoint (`/api/tags`)
- **Processing Location:** FastAPI (calculates tags and counts from all quotes)
- **Communication:** All Node.js ↔ FastAPI communication uses protobuf (binary)
  - Node.js serializes `TagsRequest` (empty message) to protobuf
  - FastAPI returns `TagsResponse` as protobuf binary
  - Node.js deserializes and converts to JSON for Vue
- **Node.js Role:** Pure wrapper - protobuf serialization/deserialization only, no business logic
- **Rationale:** Tag calculation requires processing all 2,508 quotes - better done in Python with efficient data structures

### 2. Pagination for Quotes
- **Implementation:** Page-based pagination (page number + page_size)
- **Default:** `page=1`, `page_size=10` (configurable)
- **Response includes:** `total_count`, `total_pages`, `page`, `page_size` for UI pagination controls
- **Rationale:** With 2,508 quotes, pagination is essential for performance and UX

### 3. Project Structure
- **Separation:** `backend/` (services) vs `client/` (frontend)
- **Common Proto:** `backend/common/proto/` - shared schema for both services
- **Rationale:** Clear separation of concerns, shared protobuf definitions, easier to scale

### 4. Proto File Organization
- **Decision:** Keep all messages (quotes, tags) in `quote.proto`
- **Rationale:**
  - Tags are metadata derived from quotes (they're fields in `Quote` messages)
  - Tags endpoint queries quote data to generate statistics
  - All functionality is tightly coupled to the quote domain
  - Simpler to manage for this project scope
- **Alternative:** Separate `tags.proto` if tags become a separate domain with many tag-specific messages, or if strict separation is required for larger projects
