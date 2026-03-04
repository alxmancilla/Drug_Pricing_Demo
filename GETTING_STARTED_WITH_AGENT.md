# 🚀 Getting Started with the Drug Pricing AI Agent

## 📖 What You Have Now

Your Drug Pricing Demo has been enhanced with a complete **LangGraph AI Agent** implementation that adds:

✅ **Intelligent Conversation** - Multi-turn dialog with context awareness  
✅ **Memory Systems** - Short-term (per session) and long-term (per customer)  
✅ **Personalization** - Learns and remembers customer preferences  
✅ **Tool Orchestration** - Autonomous decision-making with 5 tools  
✅ **Two Interfaces** - CLI and Streamlit web UI  

## 🎯 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `langgraph` - State machine for agent workflow
- `langchain-core` - Core LangChain functionality
- `langchain-mongodb` - MongoDB chat history
- `langchain-openai` - OpenAI integration
- Plus existing dependencies

### Step 2: Verify Environment
Make sure your `.env` file has all required keys:
```env
MONGODB_URI=mongodb+srv://...
GROVE_API_KEY=your_key
VOYAGE_API_KEY=your_key
```

### Step 3: Run the Agent
```bash
# Option A: CLI Interface
python agent_app.py

# Option B: Web Interface
streamlit run agent_streamlit_app.py

# Option C: Use Launcher
./run_agent.sh        # Mac/Linux
run_agent.bat         # Windows
```

## 💬 Try These Examples

### Example 1: Basic Search
```
You: Find the cheapest Metformin in Houston
Agent: I found several options. The cheapest is Walmart at $7.50...
```

### Example 2: Set Preference
```
You: I prefer CVS pharmacy
Agent: I've saved CVS as your preferred pharmacy. I'll prioritize it in future searches.
```

### Example 3: Use Preference
```
You: Show me Lipitor prices
Agent: Based on your preference for CVS, here are the options...
```

### Example 4: Multi-turn Conversation
```
You: Find Metformin in Houston
Agent: Here are 3 options: Walmart $7.50, CVS $8.50, Walgreens $9.00

You: What's the second cheapest?
Agent: The second cheapest option is CVS at $8.50

You: How much would I save vs the most expensive?
Agent: You'd save $1.50 by choosing CVS over Walgreens
```

## 📁 New Files Overview

### Core Implementation
- **`agent_tools.py`** - 5 LangChain tools (search, preferences, history)
- **`langgraph_agent.py`** - LangGraph state machine and workflow
- **`agent_app.py`** - CLI interface with memory
- **`agent_streamlit_app.py`** - Web UI with customer profile

### Testing & Utilities
- **`test_agent.py`** - Comprehensive test suite
- **`run_agent.sh`** / **`run_agent.bat`** - Easy launchers

### Documentation
- **`AGENT_README.md`** - Complete architecture guide
- **`AGENT_QUICKSTART.md`** - Installation & quick start
- **`AGENT_COMPARISON.md`** - Original vs Agent comparison
- **`AGENT_IMPLEMENTATION_SUMMARY.md`** - Implementation overview
- **`GETTING_STARTED_WITH_AGENT.md`** - This file

## 🧪 Test the Agent

Run the test suite to verify everything works:

```bash
# Run all tests
python test_agent.py

# Run specific test
python test_agent.py 1  # Basic search
python test_agent.py 2  # Preference saving
python test_agent.py 3  # Search history
python test_agent.py 4  # Conversation context
python test_agent.py 5  # Personalized recommendations
```

## 🏗️ Architecture at a Glance

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│      LangGraph Agent            │
│  ┌──────────┐   ┌────────────┐ │
│  │   LLM    │◄─►│   Tools    │ │
│  │ GPT-5.2  │   │  (5 tools) │ │
│  └──────────┘   └────────────┘ │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│      Memory Systems             │
│  • Short-term (conversation)    │
│  • Long-term (preferences)      │
│  • Long-term (search history)   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│      MongoDB Atlas              │
│  • customer_pricing             │
│  • customer_preferences         │
│  • customer_search_history      │
│  • conversation_history         │
└─────────────────────────────────┘
```

## 🔧 The 5 Tools

1. **`search_drug_prices`** - Hybrid search (text + vector) for pricing
2. **`save_customer_preference`** - Store customer preferences
3. **`get_customer_preferences`** - Retrieve saved preferences
4. **`get_customer_search_history`** - Access past searches
5. **`save_search_to_history`** - Track search queries

## 🧠 Memory Systems Explained

### Short-term Memory
- **What**: Conversation history within a session
- **Where**: MongoDB `conversation_history` collection
- **Why**: Enables multi-turn conversations with context
- **Example**: "What's the second cheapest?" (remembers previous results)

### Long-term Memory (Preferences)
- **What**: Customer preferences across sessions
- **Where**: MongoDB `customer_preferences` collection
- **Why**: Personalization that persists
- **Example**: "I prefer CVS" → Future searches prioritize CVS

### Long-term Memory (Search History)
- **What**: Record of all searches per customer
- **Where**: MongoDB `customer_search_history` collection
- **Why**: Analytics, learning, quick access to frequent queries
- **Example**: "What did I search for last time?"

## 📊 What Makes This Different?

| Feature | Original Demo | AI Agent |
|---------|---------------|----------|
| Conversation | Single-turn | Multi-turn with context |
| Memory | None | Short + Long term |
| Personalization | None | Learns preferences |
| Tool Use | Hardcoded | Dynamic selection |
| Intelligence | Scripted | Autonomous |

## 🎓 Learning Path

1. **Start Simple**: Run `python agent_app.py` and try basic queries
2. **Explore Memory**: Set preferences and see them persist
3. **Test Multi-turn**: Ask follow-up questions
4. **Read Code**: Start with `agent_tools.py` to see tools
5. **Understand Flow**: Study `langgraph_agent.py` for workflow
6. **Customize**: Add your own tools or modify behavior

## 🔍 Troubleshooting

### "Module not found: langgraph"
```bash
pip install langgraph langgraph-checkpoint
```

### "No search results"
```bash
python setup_database.py  # Ensure data is loaded
```

### "MongoDB connection failed"
- Check `MONGODB_URI` in `.env`
- Verify IP whitelist in MongoDB Atlas
- Test connection with original `app.py`

## 📚 Documentation Guide

- **New to the agent?** → Start with this file
- **Want to install?** → Read `AGENT_QUICKSTART.md`
- **Need architecture details?** → See `AGENT_README.md`
- **Comparing versions?** → Check `AGENT_COMPARISON.md`
- **Implementation overview?** → View `AGENT_IMPLEMENTATION_SUMMARY.md`

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Run the agent (CLI or Web)
3. ✅ Try example conversations
4. ✅ Run tests to verify
5. ✅ Read documentation
6. ✅ Customize for your needs

## 💡 Tips for Success

- **Use descriptive customer IDs**: e.g., "acmehealth123", "bestcare456"
- **Test with different customers**: Each has separate preferences
- **Monitor MongoDB**: Use MongoDB Compass to view collections
- **Check logs**: Agent prints tool usage decisions
- **Experiment**: Try natural language variations

## 🆘 Need Help?

1. Check the documentation files listed above
2. Run `python test_agent.py` to verify setup
3. Review tool implementations in `agent_tools.py`
4. Examine workflow in `langgraph_agent.py`
5. Look at example conversations in test files

## 🎉 You're Ready!

You now have a fully functional AI agent with:
- 🤖 Autonomous decision-making
- 🧠 Memory (short-term & long-term)
- 💬 Natural conversation
- 🎯 Personalization
- 🔧 Extensible architecture

Start with `python agent_app.py` and explore!

---

**Happy coding! 🚀**

