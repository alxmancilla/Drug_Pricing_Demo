# 🐳 Docker Deployment Guide

This guide explains how to deploy the Drug Pricing AI Agent using Docker for easy deployment and testing.

## 📋 Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- MongoDB Atlas account with connection string
- Grove Gateway API key
- Voyage AI API key

## 🚀 Quick Start (4 Steps)

### Step 1: Configure Environment

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your actual API keys:

```env
MONGODB_URI=mongodb+srv://your-username:your-password@cluster.mongodb.net/
GROVE_API_KEY=your-grove-api-key
VOYAGE_API_KEY=your-voyage-api-key
```

### Step 2: Build the Docker Image

```bash
# Build the container image
docker compose build
```

This will take about 1-2 minutes on first build.

### Step 3: Start the Container

```bash
# Start the container in detached mode
docker compose up -d

# View logs to confirm it's running
docker compose logs -f
```

You should see:
```
✅ Environment variables validated
🌐 Starting Streamlit UI on port 8501...
You can now view your Streamlit app in your browser.
```

### Step 4: Access the UI

Open your browser to:
```
http://localhost:8501
```

**That's it! The AI Agent is now running! 🎉**

---

## 📦 What's Included

The Docker setup includes:

- ✅ **Streamlit Web UI** - Running on port 8501
- ✅ **AI Agent** - LangGraph agent with all tools
- ✅ **Auto-restart** - Container restarts if it crashes
- ✅ **Health checks** - Monitors container health
- ✅ **Volume mounting** - Dataset persists across restarts

---

## 🛠️ Docker Commands

### Start the Agent
```bash
docker compose up -d
```

### Stop the Agent
```bash
docker compose down
```

### View Logs
```bash
# Follow logs in real-time
docker compose logs -f

# View last 100 lines
docker compose logs --tail=100

# View logs since last 10 minutes
docker compose logs --since 10m
```

### Restart the Agent
```bash
docker compose restart
```

### Rebuild After Code Changes
```bash
# Rebuild and restart
docker compose up -d --build

# Or rebuild only
docker compose build
```

### Check Container Status
```bash
# List containers
docker compose ps

# Detailed status
docker compose ps -a
```

### Access Container Shell
```bash
docker compose exec agent-ui bash
```

### Run Commands Inside Container
```bash
# Run tests
docker compose exec agent-ui python test_agent_quick.py

# Setup database
docker compose exec agent-ui python setup_database.py

# Generate dataset
docker compose exec agent-ui python generate_datasets.py
```

---

## 🔧 Advanced Configuration

### Custom Port

To run on a different port, edit `docker-compose.yml`:

```yaml
ports:
  - "8080:8501"  # Change 8080 to your desired port
```

Then restart:
```bash
docker compose down
docker compose up -d
```

### Run CLI Instead of Web UI

Edit `docker-compose.yml` and change the command:

```yaml
command: ["python", "agent_app.py"]
```

Then run interactively:
```bash
docker compose run --rm agent-ui python agent_app.py
```

Or run without changing docker-compose.yml:
```bash
docker compose run --rm agent-ui python agent_app.py
```

### Add More Environment Variables

Edit `docker-compose.yml` and add to the `environment` section:

```yaml
environment:
  - MONGODB_URI=${MONGODB_URI}
  - CUSTOM_VAR=${CUSTOM_VAR}
```

---

## 🐛 Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker compose logs
```

**Common issues:**
- Missing environment variables in `.env`
- Invalid MongoDB URI
- Invalid API keys
- Port 8501 already in use

**Solution for port conflict:**
```bash
# Find what's using port 8501
lsof -i :8501

# Kill the process or change port in docker-compose.yml
```

### Can't Access UI

**Check if container is running:**
```bash
docker compose ps
```

**Expected output:**
```
NAME                 STATUS
drug-pricing-agent   Up X seconds (healthy)
```

**Check port binding:**
```bash
docker ps | grep drug-pricing
```

**Try accessing:**
```bash
curl http://localhost:8501/_stcore/health
```

**If health check fails:**
```bash
# View detailed logs
docker compose logs --tail=100

# Restart container
docker compose restart
```

### Environment Variables Not Loading

**Verify .env file exists:**
```bash
ls -la .env
```

**Check .env format:**
- No spaces around `=`
- No quotes around values (unless needed)
- One variable per line
- No comments on same line as values

**Test environment variables:**
```bash
docker compose exec agent-ui env | grep -E "MONGODB|GROVE|VOYAGE"
```

### Database Connection Issues

**Test MongoDB connection from container:**
```bash
docker compose exec agent-ui python -c "
from pymongo import MongoClient
import os
client = MongoClient(os.getenv('MONGODB_URI'))
print('✅ Connected:', client.server_info()['version'])
"
```

**Common MongoDB errors:**
- Authentication failed → Check username/password in URI
- Network timeout → Check network connectivity
- SSL/TLS errors → Ensure URI includes `ssl=true` if required

### Container Keeps Restarting

**Check logs for errors:**
```bash
docker compose logs --tail=200
```

**Common causes:**
- Missing required environment variables
- Invalid API keys
- Application crash on startup
- Health check failing

**Disable health check temporarily:**
Edit `docker-compose.yml` and comment out the `healthcheck` section, then:
```bash
docker compose down
docker compose up -d
docker compose logs -f
```

---

## 📊 Container Management

### View Resource Usage
```bash
docker stats drug-pricing-agent
```

### Clean Up Everything
```bash
# Stop and remove containers
docker compose down

# Remove images
docker compose down --rmi all

# Remove volumes (⚠️ deletes data)
docker compose down -v

# Complete cleanup (containers, networks, images, volumes)
docker compose down -v --rmi all --remove-orphans
```

### Update to Latest Code
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker compose up -d --build
```

### View Resource Usage
```bash
# Real-time stats
docker stats drug-pricing-agent

# Or use docker compose
docker compose stats
```

### Export/Backup Container
```bash
# Save image to tar file
docker save drug_pricing_demo-agent-ui:latest -o agent-backup.tar

# Load image from tar file
docker load -i agent-backup.tar
```

---

## 🔒 Production Deployment

### Security Best Practices

1. **Never commit `.env` file**
   ```bash
   # Already in .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use secrets management**
   - Docker Swarm secrets
   - Kubernetes secrets
   - AWS Secrets Manager
   - Azure Key Vault

3. **Run as non-root user**
   Add to Dockerfile:
   ```dockerfile
   RUN useradd -m -u 1000 appuser
   USER appuser
   ```

4. **Enable HTTPS**
   Use a reverse proxy (nginx, Traefik, Caddy)

### Scaling

For multiple instances, use Docker Swarm or Kubernetes:

```bash
# Docker Swarm
docker swarm init
docker stack deploy -c docker-compose.yml agent-stack

# Scale to 3 replicas
docker service scale agent-stack_agent-ui=3
```

---

## 📝 Files Created

| File | Purpose |
|------|---------|
| `Dockerfile` | Container image definition |
| `docker-compose.yml` | Multi-container orchestration |
| `.dockerignore` | Files to exclude from image |
| `docker-entrypoint.sh` | Container startup script |
| `.env.example` | Environment template |
| `DOCKER_GUIDE.md` | This documentation |

---

## 🎯 Next Steps

1. ✅ Start the container: `docker-compose up -d`
2. ✅ Access UI: http://localhost:8501
3. ✅ Test the agent with queries
4. ✅ Check logs: `docker-compose logs -f`
5. ✅ Customize as needed

---

## 💡 Tips

- **Development**: Use volume mounts to edit code without rebuilding
- **Production**: Build optimized images with multi-stage builds
- **Monitoring**: Add Prometheus/Grafana for metrics
- **Logging**: Use centralized logging (ELK, Splunk)
- **CI/CD**: Automate builds with GitHub Actions or GitLab CI

---

**Your AI Agent is now containerized and ready to deploy anywhere! 🚀**

