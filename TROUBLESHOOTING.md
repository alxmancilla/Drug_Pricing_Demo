# 🔧 Troubleshooting Guide - Drug Pricing AI Agent

## Common Errors and Solutions

### ❌ Error 401: Access Denied - Missing Subscription Key

**Error Message:**
```
Error code: 401 - {'statusCode': 401, 'message': 'Access denied due to missing subscription key. Make sure to include subscription key when making requests to an API.'}
```

**Cause:** Grove Gateway API key is missing or not being sent correctly.

**Solutions:**

#### Solution 1: Use Agent V2 (Recommended)
The V2 agent uses direct API calls with proper authentication:

```bash
# The app automatically uses V2 if available
python agent_app.py
```

#### Solution 2: Verify Your .env File
Check that your `.env` file has the correct Grove API key:

```bash
cat .env | grep GROVE_API_KEY
```

Should show:
```
GROVE_API_KEY=your_actual_api_key_here
```

#### Solution 3: Test Grove API Directly
```bash
python test_grove_api.py
```

This will verify your Grove Gateway credentials.

#### Solution 4: Check API Key Format
Grove Gateway expects the API key in the `api-key` header (not `Authorization`).

The V2 agent handles this correctly:
```python
headers = {
    "Content-Type": "application/json",
    "api-key": GROVE_API_KEY  # Correct format for Grove
}
```

---

### ❌ Validation Error: AIMessage content

**Error Message:**
```
2 validation errors for AIMessage
content.str Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]
```

**Cause:** The LLM returned a response with `content=None` (usually when making tool calls without text).

**Solution:**

This is fixed in **Agent V2** (`langgraph_agent_v2.py`). Make sure you're using it:

```bash
# Check which version you're using
python -c "from langgraph_agent_v2 import run_agent; print('✅ Using V2')"
```

If you get an import error, the apps will fall back to V1. Ensure V2 is available:
```bash
ls -la langgraph_agent_v2.py
```

**Manual Fix (if needed):**

If you're using V1, update to V2 or modify the code to handle `None` content:
```python
content = message.get("content") or ""  # Ensure never None
```

---

### ❌ Module Not Found: langgraph

**Error Message:**
```
ModuleNotFoundError: No module named 'langgraph'
```

**Solution:**
```bash
pip install langgraph langgraph-checkpoint langchain-core langchain-mongodb langchain-openai
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

---

### ❌ MongoDB Connection Failed

**Error Message:**
```
pymongo.errors.ServerSelectionTimeoutError: connection timeout
```

**Solutions:**

1. **Check MongoDB URI:**
   ```bash
   cat .env | grep MONGODB_URI
   ```

2. **Verify IP Whitelist:**
   - Go to MongoDB Atlas
   - Network Access → Add your IP address
   - Or allow access from anywhere: `0.0.0.0/0`

3. **Test Connection:**
   ```bash
   python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGODB_URI')); print('✅ Connected:', client.server_info()['version'])"
   ```

---

### ❌ No Search Results Found

**Error Message:**
```
No relevant pricing information found
```

**Solutions:**

1. **Populate Database:**
   ```bash
   python setup_database.py
   ```

2. **Verify Data:**
   ```bash
   python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGODB_URI')); db = client.pricing_demo; print('Records:', db.customer_pricing.count_documents({}))"
   ```

3. **Check Search Indexes:**
   - Go to MongoDB Atlas
   - Browse Collections → pricing_demo → customer_pricing
   - Search Indexes tab
   - Verify `text_search_index` and `vector_search_index` exist

---

### ❌ Voyage AI Embedding Error

**Error Message:**
```
Embedding generation error: 401 Unauthorized
```

**Solutions:**

1. **Check Voyage API Key:**
   ```bash
   cat .env | grep VOYAGE_API_KEY
   ```

2. **Verify Endpoint:**
   ```bash
   cat .env | grep VOYAGE_ENDPOINT
   ```
   
   Should be:
   ```
   VOYAGE_ENDPOINT=https://ai.mongodb.com/v1/embeddings
   ```

3. **Test Embedding Generation:**
   ```python
   import os
   import requests
   from dotenv import load_dotenv
   
   load_dotenv()
   
   headers = {
       "Authorization": f"Bearer {os.getenv('VOYAGE_API_KEY')}",
       "Content-Type": "application/json"
   }
   
   payload = {
       "input": ["test"],
       "model": "voyage-4-large"
   }
   
   response = requests.post(
       "https://ai.mongodb.com/v1/embeddings",
       headers=headers,
       json=payload
   )
   
   print(response.status_code, response.json())
   ```

---

### ❌ Tool Execution Error

**Error Message:**
```
Error executing search_drug_prices: ...
```

**Solutions:**

1. **Check Tool Implementation:**
   ```bash
   python -c "from agent_tools import search_drug_prices; print(search_drug_prices.invoke({'query': 'Metformin', 'top_k': 5}))"
   ```

2. **Verify MongoDB Collections:**
   ```bash
   python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGODB_URI')); db = client.pricing_demo; print('Collections:', db.list_collection_names())"
   ```

---

### ❌ Streamlit Import Error

**Error Message:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
pip install streamlit
```

---

### ❌ Agent Doesn't Use Tools

**Symptoms:**
- Agent responds without searching
- No tool calls in output
- Generic responses

**Solutions:**

1. **Check LLM Response:**
   - The LLM decides when to use tools
   - Try more specific queries: "Search for Metformin prices in Houston"

2. **Verify Tool Definitions:**
   ```bash
   python -c "from agent_tools import ALL_TOOLS; print([t.name for t in ALL_TOOLS])"
   ```

3. **Check Agent V2:**
   Make sure you're using `langgraph_agent_v2.py` which has better tool support.

---

### ❌ Memory Not Persisting

**Symptoms:**
- Preferences not saved
- Conversation context lost

**Solutions:**

1. **Check MongoDB Collections:**
   ```bash
   python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGODB_URI')); db = client.pricing_demo; print('Preferences:', db.customer_preferences.count_documents({})); print('History:', db.customer_search_history.count_documents({}))"
   ```

2. **Verify Customer ID:**
   - Make sure you're using the same customer_id across sessions
   - Check: `python agent_app.py` and enter the same ID

3. **Test Preference Saving:**
   ```bash
   python -c "from agent_tools import save_customer_preference; print(save_customer_preference.invoke({'customer_id': 'test123', 'preference_type': 'test', 'preference_value': 'value'}))"
   ```

---

## 🧪 Diagnostic Commands

### Test All Components
```bash
# Test Grove API
python test_grove_api.py

# Test Agent Tools
python -c "from agent_tools import ALL_TOOLS; [print(f'✅ {t.name}') for t in ALL_TOOLS]"

# Test MongoDB Connection
python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGODB_URI')); print('✅ MongoDB Connected')"

# Run Agent Tests
python test_agent.py 1  # Basic search test
```

---

## 📞 Getting Help

If you're still experiencing issues:

1. **Check Environment Variables:**
   ```bash
   cat .env
   ```

2. **Verify All Dependencies:**
   ```bash
   pip list | grep -E "langchain|langgraph|pymongo|streamlit"
   ```

3. **Run Full Test Suite:**
   ```bash
   python test_agent.py
   ```

4. **Enable Debug Logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

---

## ✅ Quick Health Check

Run this to verify everything is working:

```bash
python -c "
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

print('🔍 Checking configuration...')
print(f'✅ MONGODB_URI: {\"Set\" if os.getenv(\"MONGODB_URI\") else \"❌ Missing\"}')
print(f'✅ GROVE_API_KEY: {\"Set\" if os.getenv(\"GROVE_API_KEY\") else \"❌ Missing\"}')
print(f'✅ VOYAGE_API_KEY: {\"Set\" if os.getenv(\"VOYAGE_API_KEY\") else \"❌ Missing\"}')

try:
    client = MongoClient(os.getenv('MONGODB_URI'), serverSelectionTimeoutMS=5000)
    client.server_info()
    print('✅ MongoDB: Connected')
except:
    print('❌ MongoDB: Connection failed')

print('✅ All checks complete!')
"
```

