#!/usr/bin/env python3
"""
Quick test for the AI Agent - Tests basic functionality
"""

import sys

print("=" * 70)
print("🧪 Quick Agent Test")
print("=" * 70)

# Test imports
print("\n1️⃣ Testing imports...")
try:
    from langgraph_agent_v2 import run_agent
    print("   ✅ Successfully imported langgraph_agent_v2")
except ImportError as e:
    print(f"   ❌ Failed to import langgraph_agent_v2: {e}")
    sys.exit(1)

try:
    from agent_tools import search_drug_prices, get_customer_preferences
    print("   ✅ Successfully imported agent_tools")
except ImportError as e:
    print(f"   ❌ Failed to import agent_tools: {e}")
    sys.exit(1)

# Test environment
print("\n2️⃣ Testing environment variables...")
import os
from dotenv import load_dotenv

load_dotenv()

required_vars = ["MONGODB_URI", "GROVE_API_KEY", "VOYAGE_API_KEY"]
missing_vars = []

for var in required_vars:
    if os.getenv(var):
        print(f"   ✅ {var} is set")
    else:
        print(f"   ❌ {var} is missing")
        missing_vars.append(var)

if missing_vars:
    print(f"\n   ⚠️ Missing environment variables: {', '.join(missing_vars)}")
    print("   Please check your .env file")
    sys.exit(1)

# Test MongoDB connection
print("\n3️⃣ Testing MongoDB connection...")
try:
    from pymongo import MongoClient
    client = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)
    client.server_info()
    print("   ✅ MongoDB connection successful")
except Exception as e:
    print(f"   ❌ MongoDB connection failed: {e}")
    print("   The agent may not work properly without MongoDB")

# Test search tool
print("\n4️⃣ Testing search tool...")
try:
    result = search_drug_prices.invoke({
        "query": "Metformin",
        "top_k": 2
    })
    if result:
        print(f"   ✅ Search tool works - found {len(result)} results")
        print(f"   Sample: {result[0].get('drug')} at {result[0].get('pharmacy')} - ${result[0].get('price')}")
    else:
        print("   ⚠️ Search tool returned no results")
        print("   You may need to run: python setup_database.py")
except Exception as e:
    print(f"   ❌ Search tool failed: {e}")

# Test agent
print("\n5️⃣ Testing agent with simple query...")
try:
    print("   Query: 'Hello, can you help me?'")
    response = run_agent(
        "Hello, can you help me?",
        customer_id="test_user_001"
    )
    print(f"   ✅ Agent responded: {response[:100]}...")
except Exception as e:
    print(f"   ❌ Agent failed: {e}")
    import traceback
    traceback.print_exc()

# Test agent with search query
print("\n6️⃣ Testing agent with search query...")
try:
    print("   Query: 'Find Metformin prices'")
    response = run_agent(
        "Find Metformin prices",
        customer_id="test_user_002"
    )
    print(f"   ✅ Agent responded: {response[:150]}...")
except Exception as e:
    print(f"   ❌ Agent failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✅ Quick test complete!")
print("=" * 70)
print("\n💡 Next steps:")
print("   - If all tests passed, run: python agent_app.py")
print("   - If tests failed, check the error messages above")
print("   - For detailed troubleshooting, see: TROUBLESHOOTING.md")
print("=" * 70)

