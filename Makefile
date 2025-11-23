.PHONY: setup proto download-dataset start stop clean help

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help:
	@echo "$(GREEN)Quote Recommender - Makefile Commands$(NC)"
	@echo ""
	@echo "  make setup            - Install all dependencies (uv sync, npm install)"
	@echo "  make proto            - Generate protobuf code for Python"
	@echo "  make download-dataset  - Download quotes dataset from Hugging Face and save locally"
	@echo "  make start             - Start all 3 services (FastAPI, Node.js, Vue)"
	@echo "  make stop              - Stop all services"
	@echo "  make clean             - Clean generated files and node_modules"

setup:
	@echo "$(YELLOW)Setting up FastAPI...$(NC)"
	@cd backend/fastapi && uv sync --no-build
	@echo "$(YELLOW)Setting up Node.js...$(NC)"
	@cd backend/nodejs && npm install
	@echo "$(YELLOW)Setting up Vue frontend...$(NC)"
	@cd client/vue-frontend && npm install
	@echo "$(GREEN)Setup complete!$(NC)"

proto:
	@echo "$(YELLOW)Generating protobuf code for Python...$(NC)"
	@protoc --python_out=backend/fastapi backend/common/proto/quote.proto
	@if [ -f backend/fastapi/backend/common/proto/quote_pb2.py ]; then \
		mv backend/fastapi/backend/common/proto/quote_pb2.py backend/fastapi/ && \
		rm -rf backend/fastapi/backend; \
	fi
	@echo "$(GREEN)Protobuf code generated!$(NC)"

download-dataset:
	@echo "$(YELLOW)Downloading quotes dataset from Hugging Face...$(NC)"
	@cd backend/fastapi && uv run python download_dataset.py
	@echo "$(GREEN)Dataset downloaded!$(NC)"

start:
	@echo "$(YELLOW)Starting services...$(NC)"
	@echo "$(GREEN)FastAPI: http://localhost:8000$(NC)"
	@echo "$(GREEN)Node.js BFF: http://localhost:3000$(NC)"
	@echo "$(GREEN)Vue Frontend: http://localhost:5173$(NC)"
	@echo ""
	@echo "$(YELLOW)Press Ctrl+C to stop all services$(NC)"
	@trap 'kill 0' INT; \
	cd backend/fastapi && uv run uvicorn main:app --reload --port 8000 & \
	cd backend/nodejs && npm start & \
	cd client/vue-frontend && npm run dev & \
	wait

stop:
	@echo "$(YELLOW)Stopping services...$(NC)"
	@pkill -f "uvicorn main:app" || true
	@pkill -f "node index.js" || true
	@pkill -f "vite" || true
	@echo "$(GREEN)Services stopped!$(NC)"

clean:
	@echo "$(YELLOW)Cleaning generated files...$(NC)"
	@rm -f backend/fastapi/quote_pb2.py backend/fastapi/quote_pb2.pyi
	@rm -f backend/fastapi/quotes.json
	@rm -rf backend/nodejs/node_modules
	@rm -rf client/vue-frontend/node_modules
	@rm -rf client/vue-frontend/dist
	@echo "$(GREEN)Clean complete!$(NC)"
