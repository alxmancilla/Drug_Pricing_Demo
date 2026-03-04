# 💊 Drug Pricing Assistant

An AI-powered pharmaceutical pricing assistant that helps users find the best drug prices using **MongoDB Atlas Hybrid Search** (text + vector) and **GPT-5.2** recommendations.

## 🌟 Features

### 🔍 **Hybrid Search**
- **MongoDB Atlas Search** - Fast keyword matching using Lucene
- **Vector Search** - Semantic understanding using Voyage AI embeddings
- **Rank Fusion** - Intelligently merges text and vector search results

### 🤖 **AI-Powered Recommendations**
- **GPT-5.2** via Grove Gateway for intelligent price recommendations
- Context-aware responses that understand user intent
- Natural language interaction

### 💬 **Two Interfaces**
1. **CLI** (`app.py`) - Command-line interface for technical users
2. **Streamlit UI** (`streamlit_app.py`) - Modern web interface for everyone

### 📊 **Comprehensive Dataset**
- **53 drug pricing records** across 11 medications
- **20+ cities** across the United States
- **15+ pharmacy chains** (CVS, Walgreens, Walmart, Costco, etc.)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Grove Gateway API key (for OpenAI GPT-5.2)
- Voyage AI API key (for embeddings)

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
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

**Option A: Streamlit Web UI (Recommended)**
```bash
streamlit run streamlit_app.py
# Or use the quick start script:
./run_streamlit.sh  # macOS/Linux
run_streamlit.bat   # Windows
```

**Option B: Command Line Interface**
```bash
python3 app.py
```

## 🎯 Example Queries

Try these queries in either interface:

```
What's the cheapest Metformin in Houston?
Find Ozempic prices in Los Angeles
Where can I get Lisinopril in Miami?
Show me Atorvastatin options in New York
What's the best price for Gabapentin in Phoenix?
```

## 📁 Project Structure

```
BPEpricingDemo/
├── streamlit_app.py          # Streamlit web UI
├── app.py                     # CLI application
├── setup_database.py          # Database setup script
├── generate_datasets.py       # Dataset generator
├── test_grove_api.py          # API connectivity test
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── dataset/                   # Data files (53 records each)
├── run_streamlit.sh          # Quick start (macOS/Linux)
└── run_streamlit.bat         # Quick start (Windows)
```

## 🏗️ Architecture

### Technology Stack

- **Database**: MongoDB Atlas
- **Search**: Atlas Search (Lucene) + Vector Search
- **Embeddings**: Voyage AI (voyage-4-large)
- **LLM**: OpenAI GPT-5.2 via Grove Gateway
- **Backend**: Python 3.8+
- **UI**: Streamlit

### Data Flow

```
User Query → Generate Embedding → Hybrid Search → Rank Fusion → LLM Recommendation → Display
```

## 🐛 Troubleshooting

**MongoDB Connection Error**
```bash
python3 -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGODB_URI')); print('✅ Connected')"
```

**Grove API 401 Error**
```bash
python3 test_grove_api.py
```

**No Search Results**
- Verify Atlas Search indexes are created and active
- Check data exists in `customer_pricing` collection

## 📚 Documentation

- **[STREAMLIT_UI.md](STREAMLIT_UI.md)** - Complete Streamlit documentation
- **[DATASET_EXPANSION.md](DATASET_EXPANSION.md)** - Dataset details
- **[GROVE_API_FIX.md](GROVE_API_FIX.md)** - API troubleshooting

---

**Built with ❤️ using MongoDB Atlas, OpenAI GPT-5.2, Voyage AI, and Streamlit**
