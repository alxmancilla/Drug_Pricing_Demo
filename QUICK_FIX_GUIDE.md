# ⚡ Quick Fix Guide - Common Errors

## 🎯 Common Problems

### Error 1: 401 Authentication Error
```
❌ Error code: 401 - Access denied due to missing subscription key
```

### Error 2: Validation Error
```
❌ 2 validation errors for AIMessage - content should be a valid string
```

## ✅ The Solution (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Quick Test
```bash
python test_agent_quick.py
```

**Expected Output:**
```
✅ Successfully imported langgraph_agent_v2
✅ MongoDB connection successful
✅ Search tool works
✅ Agent responded
```

**If you get errors:**
- 401 error → Your Grove API key might be invalid
- Validation error → Make sure you're using Agent V2
- MongoDB error → Check your MONGODB_URI in .env

### Step 3: Run the Agent
```bash
# CLI version
python agent_app.py

# OR Web UI version
streamlit run agent_streamlit_app.py
```

## 🔍 What Was Fixed?

**Agent V2** (`langgraph_agent_v2.py`) fixes both errors:

### Fix 1: 401 Authentication Error
- ✅ Uses direct API calls to Grove Gateway
- ✅ Sends API key in correct header format (`api-key` instead of `Authorization`)
- ✅ Works with both Grove Gateway and standard OpenAI

### Fix 2: Validation Error
- ✅ Handles `None` content from LLM responses
- ✅ Ensures AIMessage always has valid content
- ✅ Better error handling and user messages

The apps (`agent_app.py` and `agent_streamlit_app.py`) now automatically use V2.

## 🆘 Still Getting 401 Error?

### Option A: Verify Your API Key

1. Check your `.env` file:
```bash
cat .env | grep GROVE_API_KEY
```

2. Make sure it's a **Grove Gateway** key (not a standard OpenAI key)

3. Test it:
```bash
python test_grove_api.py
```

### Option B: Use Standard OpenAI Instead

If you don't have Grove Gateway access, update your `.env`:

```env
# Change these lines:
GROVE_ENDPOINT=https://api.openai.com/v1/chat/completions
OPENAI_MODEL=gpt-4
GROVE_API_KEY=sk-your-openai-api-key-here
```

Then run the agent normally.

## 📚 More Help

- **Full troubleshooting**: See `TROUBLESHOOTING.md`
- **Detailed fix explanation**: See `FIX_401_ERROR.md`
- **Getting started**: See `GETTING_STARTED_WITH_AGENT.md`

## 🎉 Summary

1. ✅ Install: `pip install -r requirements.txt`
2. ✅ Test: `python test_grove_api.py`
3. ✅ Run: `python agent_app.py`

**That's it! The 401 error should be fixed.** 🚀

