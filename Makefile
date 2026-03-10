# Drug Pricing AI Agent - Makefile
# Simplifies Docker and development commands

.PHONY: help build up down restart logs shell test clean setup

# Default target
help:
	@echo "🐳 Drug Pricing AI Agent - Docker Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Initial setup (copy .env.example, build, start)"
	@echo "  make build          - Build Docker image"
	@echo ""
	@echo "Container Management:"
	@echo "  make up             - Start containers in background"
	@echo "  make down           - Stop and remove containers"
	@echo "  make restart        - Restart containers"
	@echo "  make logs           - View container logs (follow mode)"
	@echo "  make shell          - Access container shell"
	@echo ""
	@echo "Development:"
	@echo "  make test           - Run tests inside container"
	@echo "  make rebuild        - Rebuild and restart containers"
	@echo "  make clean          - Remove containers, images, and volumes"
	@echo ""
	@echo "Database:"
	@echo "  make db-setup       - Setup database (run inside container)"
	@echo "  make db-generate    - Generate dataset (run inside container)"
	@echo ""
	@echo "Monitoring:"
	@echo "  make status         - Show container status"
	@echo "  make stats          - Show resource usage"
	@echo ""

# Initial setup
setup:
	@echo "🔧 Setting up Drug Pricing AI Agent..."
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env from .env.example..."; \
		cp .env.example .env; \
		echo "⚠️  Please edit .env and add your API keys!"; \
		echo "   Then run: make build && make up"; \
	else \
		echo "✅ .env already exists"; \
		make build; \
		make up; \
	fi

# Build Docker image
build:
	@echo "🏗️  Building Docker image..."
	docker-compose build

# Start containers
up:
	@echo "🚀 Starting containers..."
	docker-compose up -d
	@echo "✅ Containers started!"
	@echo "🌐 Access UI at: http://localhost:8501"

# Stop containers
down:
	@echo "🛑 Stopping containers..."
	docker-compose down

# Restart containers
restart:
	@echo "🔄 Restarting containers..."
	docker-compose restart

# View logs
logs:
	@echo "📋 Viewing logs (Ctrl+C to exit)..."
	docker-compose logs -f

# Access container shell
shell:
	@echo "🐚 Accessing container shell..."
	docker-compose exec agent-ui bash

# Run tests
test:
	@echo "🧪 Running tests..."
	docker-compose exec agent-ui python test_agent_quick.py

# Rebuild and restart
rebuild:
	@echo "🔨 Rebuilding and restarting..."
	docker-compose up -d --build

# Clean everything
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v --rmi all
	@echo "✅ Cleanup complete!"

# Setup database
db-setup:
	@echo "🗄️  Setting up database..."
	docker-compose exec agent-ui python setup_database.py

# Generate dataset
db-generate:
	@echo "📊 Generating dataset..."
	docker-compose exec agent-ui python generate_datasets.py

# Show container status
status:
	@echo "📊 Container status:"
	docker-compose ps

# Show resource usage
stats:
	@echo "📈 Resource usage:"
	docker stats drug-pricing-agent --no-stream

# Quick start (for first-time users)
quickstart: setup
	@echo ""
	@echo "🎉 Quick start complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Edit .env and add your API keys"
	@echo "  2. Run: make build && make up"
	@echo "  3. Access: http://localhost:8501"
	@echo ""

