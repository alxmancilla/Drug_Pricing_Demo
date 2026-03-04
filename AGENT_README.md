# 🤖 Drug Pricing AI Agent with LangGraph

This implementation converts the Drug Pricing Demo into an intelligent AI Agent using **LangChain** and **LangGraph** with comprehensive memory management.

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph AI Agent                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │   Agent      │─────▶│    Tools     │─────▶│   LLM     │ │
│  │   (State)    │◀─────│   (Actions)  │◀─────│ (GPT-5.2) │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│         │                      │                             │
│         ▼                      ▼                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Memory Management                        │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Short-term: Conversation History (per session)      │  │
│  │  Long-term:  Customer Preferences (per customer_id)  │  │
│  │  Long-term:  Search History (per customer_id)        │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              MongoDB Collections                      │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  • customer_pricing (hybrid search)                   │  │
│  │  • customer_preferences (long-term memory)            │  │
│  │  • customer_search_history (long-term memory)         │  │
│  │  • conversation_history (short-term memory)           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Components

### 1. **agent_tools.py** - LangChain Tools
Defines tools that the agent can use:

- **`search_drug_prices`**: Hybrid search (text + vector) for drug pricing
- **`save_customer_preference`**: Save customer preferences to long-term memory
- **`get_customer_preferences`**: Retrieve customer preferences
- **`get_customer_search_history`**: Get past searches
- **`save_search_to_history`**: Track search queries

### 2. **langgraph_agent.py** - LangGraph State Machine
Implements the agent workflow:

- **State Management**: Tracks messages, customer_id, preferences, search results
- **Agent Node**: Calls LLM with tools
- **Tool Node**: Executes tool calls
- **Conditional Routing**: Decides when to use tools vs. respond

### 3. **agent_app.py** - CLI Interface
Interactive command-line interface with:
- Customer ID selection
- Preference display
- Search history
- Real-time agent interaction

### 4. **agent_streamlit_app.py** - Web UI
Modern web interface with:
- Customer profile sidebar
- Live preference updates
- Search history tracking
- Chat interface

## 📦 Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Ensure your `.env` file has**:
```env
MONGODB_URI=your_mongodb_connection_string
GROVE_API_KEY=your_grove_api_key
GROVE_ENDPOINT=https://grove-gateway-prod.azure-api.net/grove-foundry-prod/openai/v1/chat/completions
OPENAI_MODEL=gpt-5.2
VOYAGE_API_KEY=your_voyage_api_key
VOYAGE_ENDPOINT=https://ai.mongodb.com/v1/embeddings
VOYAGE_MODEL=voyage-4-large
```

3. **Setup database** (if not already done):
```bash
python setup_database.py
```

## 🚀 Usage

### CLI Interface
```bash
python agent_app.py
```

Example interaction:
```
👤 Enter Customer ID: acmehealth123

🧑‍⚕️ You: What's the cheapest Metformin in Houston?
🤖 Agent: I found several options. The cheapest is at Walmart for $7.50...

🧑‍⚕️ You: I prefer CVS pharmacy
🤖 Agent: I've saved your preference for CVS pharmacy...

🧑‍⚕️ You: Show me options at my preferred pharmacy
🤖 Agent: Based on your preference for CVS, here are the options...
```

### Streamlit Web UI
```bash
streamlit run agent_streamlit_app.py
```

## 🧠 Memory System

### Short-term Memory (Conversation History)
- **Scope**: Per session
- **Storage**: MongoDB `conversation_history` collection
- **Purpose**: Maintain context within a conversation
- **Implementation**: `MongoDBChatMessageHistory` from LangChain

### Long-term Memory (Customer Preferences)
- **Scope**: Per customer_id
- **Storage**: MongoDB `customer_preferences` collection
- **Purpose**: Remember customer preferences across sessions
- **Examples**:
  - Preferred pharmacy (CVS, Walgreens, etc.)
  - Preferred location (Houston, New York, etc.)
  - Regular medications

### Long-term Memory (Search History)
- **Scope**: Per customer_id
- **Storage**: MongoDB `customer_search_history` collection
- **Purpose**: Track and learn from past searches
- **Use cases**:
  - Personalized recommendations
  - Trend analysis
  - Quick access to frequent queries

## 🔧 How It Works

1. **User sends a query** → Agent receives message
2. **Agent analyzes query** → LLM decides which tools to use
3. **Tools execute** → Search prices, retrieve preferences, etc.
4. **Results processed** → Agent formulates response
5. **Memory updated** → Preferences and history saved
6. **Response delivered** → User receives intelligent answer

## 💡 Example Use Cases

### Use Case 1: Price Search with Memory
```
User: "Find Metformin in Houston"
Agent: [Uses search_drug_prices tool]
      [Saves to search_history]
      "I found 3 options. Walmart has the best price at $7.50..."
```

### Use Case 2: Preference Learning
```
User: "I always go to CVS"
Agent: [Uses save_customer_preference tool]
      "I've saved CVS as your preferred pharmacy. I'll prioritize it in future searches."
```

### Use Case 3: Personalized Recommendations
```
User: "Show me Lipitor prices"
Agent: [Uses get_customer_preferences tool]
      [Uses search_drug_prices with customer filter]
      "Based on your preference for CVS in Houston, here are your options..."
```

## 🎨 Customization

### Add New Tools
Edit `agent_tools.py`:
```python
@tool
def your_custom_tool(param: str) -> str:
    """Tool description for the LLM"""
    # Your logic here
    return result
```

### Modify Agent Behavior
Edit `langgraph_agent.py` system message to change agent personality or instructions.

### Add New Memory Types
Create new MongoDB collections and tools to store/retrieve additional data.

## 📊 MongoDB Collections

| Collection | Purpose | Key Fields |
|------------|---------|------------|
| `customer_pricing` | Drug pricing data with embeddings | drug, pharmacy, location, price, embedding |
| `customer_preferences` | Customer preferences | customer_id, preference_type, preference_value |
| `customer_search_history` | Search tracking | customer_id, query, timestamp |
| `conversation_history` | Chat messages | session_id, messages |

## 🔍 Key Differences from Original

| Feature | Original | Agent Version |
|---------|----------|---------------|
| Architecture | Simple function calls | LangGraph state machine |
| Memory | None | Short-term + Long-term |
| Personalization | None | Customer preferences |
| Tool Use | Hardcoded | Dynamic tool selection |
| Conversation | Stateless | Stateful with context |
| Learning | None | Learns preferences over time |

## 🚦 Next Steps

1. **Test the agent**: Run both CLI and Streamlit versions
2. **Add preferences**: Tell the agent your pharmacy/location preferences
3. **Explore memory**: Check how it remembers your preferences
4. **Customize tools**: Add domain-specific tools for your use case
5. **Scale**: Deploy with proper authentication and multi-user support

