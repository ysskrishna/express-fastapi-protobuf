.PHONY: setup proto proto-lint proto-breaking start stop clean help

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help:
	@echo "$(GREEN)Quote Recommender - Makefile Commands$(NC)"
	@echo ""
	@echo "  make setup         - Install all dependencies (uv sync, npm install)"
	@echo "  make proto         - Generate protobuf code for Python and JavaScript"
	@echo "  make proto-lint    - Lint proto files with buf"
	@echo "  make proto-breaking - Check for breaking changes against main branch"
	@echo "  make start         - Start all 3 services (FastAPI, Express, Vue)"
	@echo "  make stop          - Stop all services"
	@echo "  make clean         - Clean generated files and node_modules"

setup:
	@echo "$(YELLOW)Setting up FastAPI...$(NC)"
	@cd backend/fastapi && uv sync --no-build
	@echo "$(YELLOW)Setting up Express...$(NC)"
	@cd backend/express && npm install
	@echo "$(YELLOW)Setting up Vue frontend...$(NC)"
	@cd client && npm install
	@echo "$(YELLOW)Generating protobuf code...$(NC)"
	@$(MAKE) proto
	@echo "$(GREEN)Setup complete!$(NC)"

proto:
	@echo "$(YELLOW)Generating protobuf code...$(NC)"
	@cd backend/common && buf generate
	@touch backend/fastapi/src/generated/__init__.py
	@touch backend/fastapi/src/generated/proto/__init__.py
	@echo "$(GREEN)Protobuf code generated for Python and JavaScript!$(NC)"

proto-lint:
	@echo "$(YELLOW)Linting proto files...$(NC)"
	@cd backend/common && buf lint
	@echo "$(GREEN)Lint complete!$(NC)"

proto-breaking:
	@echo "$(YELLOW)Checking for breaking changes...$(NC)"
	@cd backend/common && buf breaking --against '.git#branch=main'
	@echo "$(GREEN)Breaking change check complete!$(NC)"

start:
	@echo "$(YELLOW)Starting services...$(NC)"
	@echo "$(GREEN)FastAPI: see backend/fastapi/src/config.py or .env for port$(NC)"
	@echo "$(GREEN)Express BFF: see backend/express/src/config.js for port$(NC)"
	@echo "$(GREEN)Vue Frontend: see client/src/config.js for port$(NC)"
	@echo ""
	@echo "$(YELLOW)Press Ctrl+C to stop all services$(NC)"
	@trap 'kill 0' INT; \
	cd backend/fastapi && uv run uvicorn main:app --reload & \
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
	@rm -rf backend/fastapi/src/generated
	@rm -rf backend/express/src/generated
	@rm -rf backend/express/node_modules
	@rm -rf client/node_modules
	@rm -rf client/dist
	@echo "$(GREEN)Clean complete!$(NC)"
