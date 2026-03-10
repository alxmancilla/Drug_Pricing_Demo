# 💊 Drug Pricing AI Agent

An **intelligent AI Agent** powered by **LangChain** and **LangGraph** that helps users find the best drug prices using **MongoDB Atlas Hybrid Search**, **GPT-5.2**, and **persistent memory**.

## 🌟 Features

### 🤖 **AI Agent with Tools**
- **LangGraph State Machine** - Intelligent conversation flow with tool calling
- **5 Specialized Tools** - Search, preferences, history management
- **Autonomous Decision Making** - Agent decides when to use tools
- **Multi-turn Conversations** - Maintains context across interactions

### 🧠 **Dual Memory System**
- **Short-term Memory** - Conversation context within sessions (LangGraph state)
- **Long-term Memory** - Customer preferences and search history (MongoDB)
- **Customer-specific** - All memory indexed by `customer_id`
- **Persistent** - Preferences and history survive across sessions

### 🔍 **Hybrid Search**
- **MongoDB Atlas Search** - Fast keyword matching using Lucene
- **Vector Search** - Semantic understanding using Voyage AI embeddings
- **Rank Fusion** - Intelligently merges text and vector search results

### 💬 **Multiple Interfaces**
1. **AI Agent CLI** (`agent_app.py`) - Conversational agent with memory
2. **AI Agent Web UI** (`agent_streamlit_app.py`) - Modern Streamlit interface
3. **Basic CLI** (`app.py`) - Simple search interface
4. **Basic Web UI** (`streamlit_app.py`) - Basic Streamlit interface

### 📊 **Comprehensive Dataset**
- **53 drug pricing records** across 11 medications
- **20+ cities** across the United States
- **15+ pharmacy chains** (CVS, Walgreens, Walmart, Costco, etc.)

## 🚀 Quick Start

### Prerequisites

- **Option A (Docker)**: Docker Desktop or Docker Engine + Docker Compose
- **Option B (Python)**: Python 3.8+
- MongoDB Atlas account
- Grove Gateway API key (for OpenAI GPT-5.2)
- Voyage AI API key (for embeddings)

### 🐳 Option A: Docker Deployment (Recommended)

**Fastest way to get started!**

```bash
# 1. Copy environment template (if not already done)
cp .env.example .env

# 2. Edit .env and add your API keys
# (MONGODB_URI, GROVE_API_KEY, VOYAGE_API_KEY)

# 3. Build and start with Docker Compose
docker compose build
docker compose up -d

# 4. Access the UI
# Open http://localhost:8501
```

**Or use Make commands (easier):**
```bash
make setup    # Initial setup (copies .env.example)
make build    # Build Docker image
make up       # Start containers
make logs     # View logs
make down     # Stop containers
make status   # Check container status
```

**Quick commands:**
```bash
# View real-time logs
docker compose logs -f

# Check container status
docker compose ps

# Restart the application
docker compose restart

# Stop and remove containers
docker compose down
```

See **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** for detailed Docker documentation and **[DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)** for quick reference.

### 🐍 Option B: Python Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (includes LangChain, LangGraph, etc.)
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
# MongoDB
MONGODB_URI=mongodb+srv://your-cluster.mongodb.net/

# Grove Gateway (OpenAI)
GROVE_API_KEY=your-grove-api-key
GROVE_ENDPOINT=https://grove-gateway-prod.azure-api.net/grove-foundry-prod/openai/v1/chat/completions
OPENAI_MODEL=gpt-5.2

# Voyage AI (Embeddings)
VOYAGE_API_KEY=your-voyage-api-key
VOYAGE_ENDPOINT=https://ai.mongodb.com/v1/embeddings
VOYAGE_MODEL=voyage-4-large
```

### 3. Generate and Load Data

```bash
# Generate datasets (53 records each)
python3 generate_datasets.py

# Load data into MongoDB and create indexes
python3 setup_database.py
```

### 4. Create Atlas Search Indexes

Follow the instructions printed by `setup_database.py` to create:
1. **vector_search_index** - For semantic search
2. **text_search_index** - For keyword search

### 5. Run the Application

**🐳 Docker (Recommended)**
```bash
docker-compose up -d
# Access at http://localhost:8501
```

**🤖 Python: AI Agent with Memory**
```bash
# CLI Agent
python agent_app.py

# Or Web UI Agent
streamlit run agent_streamlit_app.py
```

**📊 Python: Basic Search Interface**
```bash
# Basic CLI
python app.py

# Or Basic Streamlit UI
streamlit run streamlit_app.py
# Or use the quick start script:
./run_streamlit.sh  # macOS/Linux
run_streamlit.bat   # Windows
```

## 🎯 Example Queries

### AI Agent Queries (with Memory & Tools)

```
# Search queries
Find Metformin prices in Houston
What's the cheapest Ozempic in Los Angeles?
Show me Lisinopril options in Miami

# Preference management
I prefer CVS pharmacy
I want generic medications only
Save my preference for Houston location

# History and context
What did I search for last time?
Show me my previous searches
What are my saved preferences?

# Multi-turn conversations
Agent: I found Metformin at CVS for $15
You: Is there anything cheaper?
Agent: Yes, Walmart has it for $12
You: Great, I prefer Walmart
Agent: I've saved your preference for Walmart
```

### Basic Search Queries

```
What's the cheapest Metformin in Houston?
Find Ozempic prices in Los Angeles
Where can I get Lisinopril in Miami?
Show me Atorvastatin options in New York
What's the best price for Gabapentin in Phoenix?
```

## 📁 Project Structure

```
Drug_Pricing_Demo/
├── 🤖 AI Agent Files (LangChain + LangGraph)
│   ├── agent_app.py                  # AI Agent CLI
│   ├── agent_streamlit_app.py        # AI Agent Web UI
│   ├── langgraph_agent_v2.py         # Agent logic with LangGraph
│   ├── agent_tools.py                # 5 specialized agent tools
│   └── test_agent_quick.py           # Quick agent test script
│
├── 📊 Basic Search Files (Optional)
│   ├── app.py                        # Basic CLI (non-agent)
│   └── streamlit_app.py              # Basic Streamlit UI (non-agent)
│
├── 🛠️ Setup & Testing
│   ├── setup_database.py             # Database setup & data loading
│   ├── generate_datasets.py          # Dataset generator (53 records)
│   ├── test_grove_api.py             # Grove API connectivity test
│   └── test_agent.py                 # Full agent test suite
│
├── 📚 Documentation
│   ├── README.md                     # This file (main documentation)
│   ├── AGENT_README.md               # Agent architecture details
│   ├── AGENT_COMPARISON.md           # Agent vs Basic comparison
│   ├── GETTING_STARTED_WITH_AGENT.md # Agent getting started guide
│   ├── QUICK_FIX_GUIDE.md            # Quick troubleshooting (3 steps)
│   ├── FIX_401_ERROR.md              # 401 authentication error fix
│   ├── FIX_VALIDATION_ERROR.md       # Validation error fix
│   ├── TROUBLESHOOTING.md            # Full troubleshooting guide
│   └── DATASET_EXPANSION.md          # Dataset details
│
├── 🐳 Docker Files
│   ├── Dockerfile                    # Container image definition
│   ├── docker-compose.yml            # Multi-container orchestration
│   ├── .dockerignore                 # Files to exclude from image
│   ├── docker-entrypoint.sh          # Container startup script
│   ├── Makefile                      # Docker command shortcuts
│   ├── DOCKER_QUICKSTART.md          # Quick reference card
│   ├── DOCKER_GUIDE.md               # Complete Docker guide
│   ├── DEPLOYMENT_CHECKLIST.md       # Deployment checklist
│   └── DOCKER_IMPLEMENTATION_SUMMARY.md  # Implementation summary
│
├── ⚙️ Configuration
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Environment variables (create this)
│   ├── .env.example                  # Environment template
│   ├── run_agent.sh                  # Agent launcher (macOS/Linux)
│   ├── run_agent.bat                 # Agent launcher (Windows)
│   ├── run_streamlit.sh              # Basic UI launcher (macOS/Linux)
│   └── run_streamlit.bat             # Basic UI launcher (Windows)
│
└── 📁 Data
    └── dataset/                      # JSON data files (53 records each)
```

## 🏗️ Architecture

### Technology Stack

- **AI Framework**: LangChain + LangGraph
- **Database**: MongoDB Atlas
- **Search**: Atlas Search (Lucene) + Vector Search
- **Embeddings**: Voyage AI (voyage-4-large)
- **LLM**: OpenAI GPT-5.2 via Grove Gateway
- **Memory**: LangGraph State + MongoDB (long-term)
- **Backend**: Python 3.8+
- **UI**: Streamlit

### AI Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      LangGraph Agent                         │
│  ┌────────────┐      ┌──────────────┐      ┌─────────────┐ │
│  │   Agent    │─────▶│ Should       │─────▶│   Tools     │ │
│  │   (LLM)    │◀─────│ Continue?    │◀─────│  Execution  │ │
│  └────────────┘      └──────────────┘      └─────────────┘ │
│        │                                           │         │
│        │                                           │         │
│        ▼                                           ▼         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Agent State (Messages)                     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │          5 Specialized Tools             │
        ├─────────────────────────────────────────┤
        │ 1. search_drug_prices                   │
        │ 2. save_customer_preference             │
        │ 3. get_customer_preferences             │
        │ 4. get_customer_search_history          │
        │ 5. save_search_to_history               │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         MongoDB Collections              │
        ├─────────────────────────────────────────┤
        │ • customer_pricing (search data)        │
        │ • customer_preferences (long-term)      │
        │ • customer_search_history (long-term)   │
        └─────────────────────────────────────────┘
```

### Data Flow

**Basic Search:**
```
User Query → Generate Embedding → Hybrid Search → Rank Fusion → LLM Recommendation → Display
```

**AI Agent Flow:**
```
User Input → Agent (LLM) → Decide Tools → Execute Tools → Update State →
Agent Response → Save to Memory → Display
```

## 🐛 Troubleshooting

### Quick Health Check
```bash
# Run comprehensive test
python test_agent_quick.py
```

### Common Issues

**❌ 401 Authentication Error**
```bash
# Test Grove API connection
python test_grove_api.py
```
**Fix:** See `QUICK_FIX_GUIDE.md` or `FIX_401_ERROR.md`

**❌ Validation Error (AIMessage content)**
```
2 validation errors for AIMessage - content should be a valid string
```
**Fix:** Make sure you're using Agent V2 (`langgraph_agent_v2.py`). See `FIX_VALIDATION_ERROR.md`

**❌ MongoDB Connection Error**
```bash
python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGODB_URI')); print('✅ Connected')"
```

**❌ No Search Results**
- Verify Atlas Search indexes are created and active
- Check data exists: `python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGODB_URI')); print('Records:', client.pricing_demo.customer_pricing.count_documents({}))"`

### Full Troubleshooting Guide
See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for comprehensive troubleshooting.

## 📚 Documentation

### AI Agent Documentation
- **[AGENT_README.md](AGENT_README.md)** - Complete agent architecture
- **[AGENT_COMPARISON.md](AGENT_COMPARISON.md)** - Agent vs Basic comparison
- **[GETTING_STARTED_WITH_AGENT.md](GETTING_STARTED_WITH_AGENT.md)** - Agent quick start

### Troubleshooting Guides
- **[QUICK_FIX_GUIDE.md](QUICK_FIX_GUIDE.md)** - Quick 3-step fix for common errors
- **[FIX_401_ERROR.md](FIX_401_ERROR.md)** - Detailed 401 error fix
- **[FIX_VALIDATION_ERROR.md](FIX_VALIDATION_ERROR.md)** - Validation error fix
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Full troubleshooting guide

### Deployment & Infrastructure
- **[DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)** - Quick reference (start here!)
- **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Complete Docker deployment guide
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Step-by-step deployment checklist
- **[Makefile](Makefile)** - Docker command shortcuts (`make help`)

### Other Documentation
- **[STREAMLIT_UI.md](STREAMLIT_UI.md)** - Streamlit UI documentation (if exists)
- **[DATASET_EXPANSION.md](DATASET_EXPANSION.md)** - Dataset details

## 🎯 Key Differences: Agent vs Basic

| Feature | AI Agent | Basic Search |
|---------|----------|--------------|
| **Framework** | LangChain + LangGraph | Direct API calls |
| **Tools** | 5 specialized tools | None |
| **Memory** | Short + Long term | None |
| **Conversations** | Multi-turn | Single query |
| **Preferences** | Saved per customer | None |
| **History** | Tracked in MongoDB | None |
| **Intelligence** | Autonomous decisions | Fixed flow |

See **[AGENT_COMPARISON.md](AGENT_COMPARISON.md)** for detailed comparison.

## 🚀 Next Steps

1. **Start with the AI Agent**: `python agent_app.py`
2. **Try multi-turn conversations**: Ask follow-up questions
3. **Set preferences**: "I prefer CVS pharmacy"
4. **Check history**: "What did I search for?"
5. **Explore the tools**: See `agent_tools.py`

---

**Built with ❤️ using LangChain, LangGraph, MongoDB Atlas, OpenAI GPT-5.2, Voyage AI, and Streamlit**
