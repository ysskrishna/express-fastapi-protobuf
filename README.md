# Quote Recommender - Node.js + FastAPI + Protobuf

A Quote Recommender app demonstrating microservice communication between Vue.js, Node.js, and FastAPI using Protocol Buffers.

## Architecture

```
┌──────────────┐     JSON/HTTP      ┌──────────────┐     Protobuf      ┌──────────────┐
│              │  ───────────────►  │              │  ───────────────► │              │
│   Vue.js     │  GET /quotes?tag=  │   Node.js    │  Binary payload   │   FastAPI    │
│   Frontend   │  ◄───────────────  │   (BFF)      │  ◄─────────────── │  (Quotes DB) │
│  (Port 5173) │     JSON array     │ (Port 3000)  │  Binary response  │ (Port 8000)  │
└──────────────┘                    └──────────────┘                   └──────────────┘
```

## Quick Start

### Prerequisites
- Python 3.10+ with [uv](https://github.com/astral-sh/uv) installed
- Node.js 18+
- Protocol Buffers compiler (`protoc`)

### Installation

1. **Install dependencies:**
   ```bash
   make setup
   ```

2. **Generate protobuf code:**
   ```bash
   make proto
   ```

3. **Start all services:**
   ```bash
   make start
   ```

4. **Open the app:**
   - Frontend: http://localhost:5173
   - Node.js BFF: http://localhost:3000
   - FastAPI: http://localhost:8000

### Manual Start (Alternative)

If you prefer to start services individually:

1. **Generate protobuf code:**
   ```bash
   protoc --python_out=backend/fastapi backend/common/proto/quote.proto
   ```

2. **Start FastAPI:**
   ```bash
   cd backend/fastapi
   uv sync
   uv run uvicorn main:app --reload --port 8000
   ```

3. **Start Node.js BFF:**
   ```bash
   cd backend/nodejs
   npm install
   npm start
   ```

4. **Start Vue frontend:**
   ```bash
   cd client
   npm install
   npm run dev
   ```

## Features

- **Tag-based quote filtering** - Browse quotes by tags (inspirational, life, love, etc.)
- **Pagination** - Navigate through quotes with page controls
- **Tag statistics** - See count of quotes per tag
- **Protobuf communication** - Efficient binary protocol between Node.js and FastAPI
- **Modern UI** - Clean, responsive Vue.js interface

## Data Source

Quotes are loaded from a local JSON file (`backend/fastapi/quotes.json`) containing 2,508 quotes from the [Hugging Face english_quotes dataset](https://huggingface.co/datasets/Abirate/english_quotes). The dataset file is included in the repository and loaded on FastAPI startup.

## API Endpoints

### Node.js BFF (JSON)
- `GET /api/quotes?tag={tag}&page={page}&page_size={size}` - Get quotes by tag
- `GET /api/tags` - Get all tags with counts
- `GET /health` - Health check

### FastAPI (Protobuf)
- `POST /quotes` - Accepts `QuoteRequest`, returns `QuoteResponse`
- `POST /tags` - Accepts `TagsRequest`, returns `TagsResponse`
- `GET /health` - Health check

## Project Structure

```
nodejs-fastapi-protobuf/
├── backend/
│   ├── common/proto/quote.proto    # Protobuf schema
│   ├── fastapi/                    # FastAPI service
│   └── nodejs/                     # Node.js BFF
├── client/                         # Vue.js frontend
├── Makefile                        # Build commands
└── README.md
```

## Makefile Commands

- `make setup` - Install all dependencies
- `make proto` - Generate protobuf code
- `make start` - Start all services
- `make stop` - Stop all services
- `make clean` - Clean generated files and dependencies

## License

This project uses the english_quotes dataset which is licensed under CC BY 4.0.
