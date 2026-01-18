.PHONY: setup proto start stop clean help

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help:
	@echo "$(GREEN)Quote Recommender - Makefile Commands$(NC)"
	@echo ""
	@echo "  make setup    - Install all dependencies (uv sync, npm install)"
	@echo "  make proto    - Generate protobuf code for Python"
	@echo "  make start    - Start all 3 services (FastAPI, Node.js, Vue)"
	@echo "  make stop     - Stop all services"
	@echo "  make clean    - Clean generated files and node_modules"

setup:
	@echo "$(YELLOW)Setting up FastAPI...$(NC)"
	@cd backend/fastapi && uv sync --no-build
	@echo "$(YELLOW)Setting up Node.js...$(NC)"
	@cd backend/express && npm install
	@echo "$(YELLOW)Setting up Vue frontend...$(NC)"
	@cd client && npm install
	@echo "$(YELLOW)Generating protobuf code...$(NC)"
	@$(MAKE) proto
	@echo "$(GREEN)Setup complete!$(NC)"

proto:
	@echo "$(YELLOW)Generating protobuf code for Python...$(NC)"
	@mkdir -p backend/fastapi/proto
	@protoc \
		--proto_path=backend/common/proto \
		--python_out=backend/fastapi/proto \
		backend/common/proto/*.proto
	@touch backend/fastapi/proto/__init__.py
	@echo "$(GREEN)Protobuf code generated!$(NC)"

start:
	@echo "$(YELLOW)Starting services...$(NC)"
	@echo "$(GREEN)FastAPI: http://localhost:8000$(NC)"
	@echo "$(GREEN)Node.js BFF: http://localhost:3000$(NC)"
	@echo "$(GREEN)Vue Frontend: http://localhost:5173$(NC)"
	@echo ""
	@echo "$(YELLOW)Press Ctrl+C to stop all services$(NC)"
	@trap 'kill 0' INT; \
	cd backend/fastapi && uv run uvicorn main:app --reload --port 8000 & \
	cd backend/express && npm start & \
	cd client && npm run dev & \
	wait

stop:
	@echo "$(YELLOW)Stopping services...$(NC)"
	@pkill -f "uvicorn main:app" || true
	@pkill -f "node src/index.js" || true
	@pkill -f "vite" || true
	@echo "$(GREEN)Services stopped!$(NC)"

clean:
	@echo "$(YELLOW)Cleaning generated files...$(NC)"
	@rm -rf backend/fastapi/proto
	@rm -rf backend/express/node_modules
	@rm -rf client/node_modules
	@rm -rf client/dist
	@echo "$(GREEN)Clean complete!$(NC)"
