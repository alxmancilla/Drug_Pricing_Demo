# 🚀 Deployment Checklist

Use this checklist to ensure successful deployment of the Drug Pricing AI Agent.

---

## ✅ Pre-Deployment Checklist

### 1. Prerequisites
- [ ] Docker installed and running
- [ ] Docker Compose installed (v2.0+)
- [ ] MongoDB Atlas account created
- [ ] Grove Gateway API key obtained
- [ ] Voyage AI API key obtained

### 2. Environment Configuration
- [ ] `.env` file created from `.env.example`
- [ ] `MONGODB_URI` configured with valid connection string
- [ ] `GROVE_API_KEY` added
- [ ] `VOYAGE_API_KEY` added
- [ ] All required environment variables set

### 3. Database Setup
- [ ] MongoDB cluster created
- [ ] Database user created with read/write permissions
- [ ] Network access configured (IP whitelist or 0.0.0.0/0)
- [ ] Connection string tested

---

## 🐳 Docker Deployment Steps

### Step 1: Build Image
```bash
docker compose build
```

**Expected result:**
- ✅ Build completes successfully (~60-90 seconds)
- ✅ No error messages
- ✅ Image created: `drug_pricing_demo-agent-ui:latest`

**Verify:**
```bash
docker images | grep drug_pricing_demo
```

### Step 2: Start Container
```bash
docker compose up -d
```

**Expected result:**
- ✅ Network created: `drug_pricing_demo_agent-network`
- ✅ Container created: `drug-pricing-agent`
- ✅ Container status: `Up` and `healthy`

**Verify:**
```bash
docker compose ps
```

### Step 3: Check Logs
```bash
docker compose logs
```

**Expected output:**
```
🚀 Starting Drug Pricing AI Agent...
✅ Environment variables validated
🌐 Starting Streamlit UI on port 8501...
You can now view your Streamlit app in your browser.
```

### Step 4: Test Access
```bash
curl http://localhost:8501/_stcore/health
```

**Expected result:**
- ✅ HTTP 200 response
- ✅ Health check passes

**Or open in browser:**
```
http://localhost:8501
```

---

## 🧪 Post-Deployment Testing

### 1. UI Access Test
- [ ] Web UI loads at http://localhost:8501
- [ ] No error messages displayed
- [ ] Interface renders correctly

### 2. Agent Functionality Test
- [ ] Enter customer ID (e.g., "acmehealth123")
- [ ] Ask a test query: "Find cheapest Metformin in Houston"
- [ ] Agent responds with results
- [ ] No errors in response

### 3. Tool Functionality Test
- [ ] Test search: "What's the price of Ozempic in LA?"
- [ ] Test preferences: "I prefer CVS pharmacy"
- [ ] Test history: "What did I search for before?"
- [ ] All tools execute successfully

### 4. Memory Test
- [ ] Set a preference: "I prefer Walgreens"
- [ ] Ask another question
- [ ] Verify agent remembers preference
- [ ] Check conversation history maintained

---

## 🔍 Troubleshooting Checklist

### Container Won't Start
- [ ] Check logs: `docker compose logs`
- [ ] Verify `.env` file exists
- [ ] Verify all required env vars are set
- [ ] Check port 8501 is not in use: `lsof -i :8501`
- [ ] Try rebuilding: `docker compose build --no-cache`

### Health Check Failing
- [ ] Wait 40 seconds for startup
- [ ] Check logs for errors
- [ ] Verify Streamlit is running
- [ ] Test health endpoint: `curl http://localhost:8501/_stcore/health`

### Can't Access UI
- [ ] Verify container is running: `docker compose ps`
- [ ] Check port mapping: `docker ps | grep 8501`
- [ ] Try accessing: http://localhost:8501
- [ ] Check firewall settings
- [ ] Try different browser

### Agent Not Responding
- [ ] Check Grove API key is valid
- [ ] Check Voyage API key is valid
- [ ] Check MongoDB connection
- [ ] View logs: `docker compose logs -f`
- [ ] Test APIs inside container

---

## 📊 Monitoring Checklist

### Daily Checks
- [ ] Container is running: `docker compose ps`
- [ ] Health check passing
- [ ] No error logs: `docker compose logs --tail=100`
- [ ] Disk space available

### Weekly Checks
- [ ] Review resource usage: `docker stats drug-pricing-agent`
- [ ] Check for updates: `git pull`
- [ ] Backup configuration files
- [ ] Review application logs

---

## 🔄 Maintenance Tasks

### Restart Container
```bash
docker compose restart
```

### Update Application
```bash
git pull
docker compose down
docker compose build
docker compose up -d
```

### View Logs
```bash
# Real-time
docker compose logs -f

# Last 100 lines
docker compose logs --tail=100
```

### Cleanup
```bash
# Remove stopped containers
docker compose down

# Remove everything (including volumes)
docker compose down -v --rmi all
```

---

## ✅ Deployment Complete

Once all items are checked:

- ✅ Container is running and healthy
- ✅ UI is accessible
- ✅ Agent responds to queries
- ✅ All tools working
- ✅ Memory functioning
- ✅ No errors in logs

**Your Drug Pricing AI Agent is successfully deployed! 🎉**

---

## 📚 Additional Resources

- **Quick Reference**: [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)
- **Full Guide**: [DOCKER_GUIDE.md](DOCKER_GUIDE.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Main README**: [README.md](README.md)

