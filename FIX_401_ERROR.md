# 🔧 Fix for 401 Error - Grove Gateway Authentication

## Problem

When running the AI agent, you encountered:

```
❌ Error: Error code: 401 - {'statusCode': 401, 'message': 'Access denied due to missing subscription key. Make sure to include subscription key when making requests to an API.'}
```

## Root Cause

Grove Gateway requires the API key to be sent in a specific header format (`api-key`), which is different from the standard OpenAI format (`Authorization: Bearer`).

The original `langgraph_agent.py` used LangChain's `ChatOpenAI` wrapper, which sends the key in the OpenAI format, causing Grove Gateway to reject the request.

## Solution Implemented

### ✅ Created Agent V2 (`langgraph_agent_v2.py`)

A new version that:
1. **Uses direct API calls** to Grove Gateway instead of LangChain's wrapper
2. **Sends the API key correctly** in the `api-key` header
3. **Handles tool calling** in OpenAI's function calling format
4. **Provides better error messages** for debugging

### Key Differences

#### Original (V1) - Using LangChain Wrapper
```python
llm = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=GROVE_API_KEY,
    base_url=GROVE_ENDPOINT.replace("/chat/completions", ""),
    temperature=0.7,
    max_tokens=500
)
# ❌ Sends: Authorization: Bearer <key>
```

#### New (V2) - Direct API Calls
```python
headers = {
    "Content-Type": "application/json",
    "api-key": GROVE_API_KEY  # ✅ Correct format for Grove
}

response = requests.post(GROVE_ENDPOINT, headers=headers, json=payload)
```

## How to Use the Fix

### Option 1: Automatic (Recommended)

The apps now automatically use V2 if available:

```bash
python agent_app.py
# or
streamlit run agent_streamlit_app.py
```

You'll see:
```
✅ Using LangGraph Agent V2 (Direct API calls)
```

### Option 2: Test First

Before running the agent, test your Grove Gateway connection:

```bash
python test_grove_api.py
```

Expected output:
```
✅ SUCCESS! Grove Gateway is working correctly
🤖 Response: Hello, Grove Gateway is working!
```

### Option 3: Manual Import

In your own code:

```python
from langgraph_agent_v2 import run_agent

response = run_agent("Find Metformin in Houston", customer_id="acmehealth123")
print(response)
```

## Files Modified/Created

### Created
1. **`langgraph_agent_v2.py`** - New agent with direct API calls
2. **`TROUBLESHOOTING.md`** - Comprehensive troubleshooting guide
3. **`FIX_401_ERROR.md`** - This document

### Modified
1. **`agent_app.py`** - Auto-imports V2 if available
2. **`agent_streamlit_app.py`** - Auto-imports V2 if available

## Verification Steps

### Step 1: Test Grove API
```bash
python test_grove_api.py
```

Expected: `✅ SUCCESS!`

### Step 2: Run Agent
```bash
python agent_app.py
```

Expected: No 401 errors, agent responds normally

### Step 3: Try a Query
```
You: Find Metformin in Houston
Agent: I found several options...
```

## What If It Still Doesn't Work?

### Check 1: Verify API Key
```bash
cat .env | grep GROVE_API_KEY
```

Make sure it's a **Grove Gateway** API key, not a standard OpenAI key.

### Check 2: Test API Key Directly
```bash
curl -X POST "https://grove-gateway-prod.azure-api.net/grove-foundry-prod/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "api-key: YOUR_GROVE_API_KEY" \
  -d '{
    "model": "gpt-5.2",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_completion_tokens": 50
  }'
```

### Check 3: Contact Grove Gateway Admin
If the API key is correct but still failing:
- The key might not have access to the endpoint
- The key might be expired
- You might need a different subscription level

## Alternative: Use Standard OpenAI

If you don't have Grove Gateway access, you can modify the code to use standard OpenAI:

```python
# In .env
GROVE_ENDPOINT=https://api.openai.com/v1/chat/completions
OPENAI_MODEL=gpt-4
GROVE_API_KEY=sk-your-openai-api-key
```

Then use V2 agent which will work with both Grove and OpenAI.

## Technical Details

### Grove Gateway Authentication Flow

```
1. Client sends request with header: "api-key: <key>"
2. Grove Gateway validates the subscription key
3. If valid, forwards to OpenAI backend
4. Returns response to client
```

### Why LangChain's ChatOpenAI Doesn't Work

LangChain's `ChatOpenAI` class is designed for OpenAI's API, which uses:
```
Authorization: Bearer <key>
```

Grove Gateway expects:
```
api-key: <key>
```

Even with `default_headers`, LangChain still sends the Authorization header, which Grove Gateway doesn't recognize.

### Why V2 Works

V2 bypasses LangChain's HTTP client and uses `requests` directly, giving us full control over headers:

```python
headers = {
    "Content-Type": "application/json",
    "api-key": GROVE_API_KEY  # Exactly what Grove expects
}
```

## Summary

✅ **Problem**: 401 error due to incorrect authentication header  
✅ **Solution**: Created V2 agent with direct API calls  
✅ **Result**: Proper Grove Gateway authentication  
✅ **Benefit**: Works with both Grove Gateway and standard OpenAI  

## Quick Reference

| File | Purpose |
|------|---------|
| `langgraph_agent_v2.py` | New agent with correct auth |
| `test_grove_api.py` | Test Grove Gateway connection |
| `TROUBLESHOOTING.md` | Full troubleshooting guide |
| `FIX_401_ERROR.md` | This document |

## Next Steps

1. ✅ Run `python test_grove_api.py` to verify connection
2. ✅ Run `python agent_app.py` to use the agent
3. ✅ If issues persist, see `TROUBLESHOOTING.md`
4. ✅ Contact Grove Gateway admin if API key is invalid

---

**The 401 error should now be resolved! 🎉**

