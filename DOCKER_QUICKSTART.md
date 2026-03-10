# 🐳 Docker Quick Start

## ⚡ 4-Step Setup

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env and add your API keys

# 2. Build the image
docker compose build

# 3. Start the agent
docker compose up -d

# 4. Access the UI
# Open http://localhost:8501
```

**That's it! 🎉**

---

## 📋 Common Commands

### Using Docker Compose

```bash
# Build
docker compose build

# Start
docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f

# Restart
docker compose restart

# Rebuild
docker compose up -d --build

# Check status
docker compose ps
```

### Using Make (Easier!)

```bash
# Initial setup
make setup

# Build image
make build

# Start
make up

# Stop
make down

# View logs
make logs

# Restart
make restart

# Rebuild
make rebuild

# Run tests
make test

# Access shell
make shell

# Check status
make status

# View all commands
make help
```

---

## 🔧 Troubleshooting

### Check if running
```bash
docker compose ps
```

Expected output:
```
NAME                 STATUS
drug-pricing-agent   Up X seconds (healthy)
```

### View logs
```bash
# Last 50 lines
docker compose logs --tail=50

# Real-time logs
docker compose logs -f

# Logs since 10 minutes ago
docker compose logs --since 10m
```

### Restart container
```bash
docker compose restart
```

### Rebuild from scratch
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Access container shell
```bash
docker compose exec agent-ui bash
```

### Test inside container
```bash
# Test Grove API
docker compose exec agent-ui python test_grove_api.py

# Test agent
docker compose exec agent-ui python test_agent_quick.py
```

### Port already in use
```bash
# Find what's using port 8501
lsof -i :8501

# Or change port in docker-compose.yml
# Then restart
docker compose down
docker compose up -d
```

---

## 📝 Environment Variables

Required in `.env`:
```env
MONGODB_URI=mongodb+srv://...
GROVE_API_KEY=your-key
VOYAGE_API_KEY=your-key
```

---

## 🌐 Access Points

- **Web UI**: http://localhost:8501
- **Health Check**: http://localhost:8501/_stcore/health

---

## 💡 Tips

- Use `make help` to see all available commands
- Use `make logs` to debug issues
- Edit `.env` and restart with `make restart`
- See `DOCKER_GUIDE.md` for detailed documentation

---

**Quick Reference Card - Keep this handy! 📌**

