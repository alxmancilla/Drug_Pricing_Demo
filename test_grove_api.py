#!/usr/bin/env python3
"""
Test script to verify Grove Gateway API connectivity
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("Grove Gateway API Test")
print("=" * 70)

# Get configuration
GROVE_API_KEY = os.getenv("GROVE_API_KEY")
GROVE_ENDPOINT = os.getenv("GROVE_ENDPOINT", "https://grove-gateway-prod.azure-api.net/grove-foundry-prod/openai/v1/chat/completions")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")

print(f"\n📋 Configuration:")
print(f"  Endpoint: {GROVE_ENDPOINT}")
print(f"  Model: {OPENAI_MODEL}")
print(f"  API Key: {GROVE_API_KEY[:20]}...{GROVE_API_KEY[-10:] if GROVE_API_KEY and len(GROVE_API_KEY) > 30 else 'NOT SET'}")

if not GROVE_API_KEY:
    print("\n❌ ERROR: GROVE_API_KEY not found in environment variables")
    print("   Please check your .env file")
    exit(1)

print(f"\n🔍 Testing Grove Gateway API...")

# Test request
headers = {
    "Content-Type": "application/json",
    "api-key": GROVE_API_KEY
}

payload = {
    "model": OPENAI_MODEL,
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say 'Hello, Grove Gateway is working!' if you can read this."}
    ],
    "max_completion_tokens": 50
}

try:
    print(f"  📤 Sending request to {GROVE_ENDPOINT}...")
    response = requests.post(GROVE_ENDPOINT, headers=headers, json=payload, timeout=30)
    
    print(f"  📥 Response status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"  ✅ SUCCESS! Grove Gateway is working correctly")
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0]["message"]["content"]
            print(f"\n  🤖 Response: {message}")
    elif response.status_code == 401:
        print(f"  ❌ ERROR: 401 Access Denied")
        print(f"\n  This means your API key is invalid or not authorized for Grove Gateway.")
        print(f"\n  Possible issues:")
        print(f"    1. The API key is not a valid Grove Gateway key")
        print(f"    2. The API key is an OpenAI key, not a Grove key")
        print(f"    3. The API key has expired or been revoked")
        print(f"    4. The API key doesn't have access to this endpoint")
        print(f"\n  Response body:")
        print(f"    {response.text}")
    elif response.status_code == 404:
        print(f"  ❌ ERROR: 404 Not Found")
        print(f"  The endpoint URL might be incorrect")
        print(f"  Response: {response.text}")
    else:
        print(f"  ❌ ERROR: Unexpected status code {response.status_code}")
        print(f"  Response: {response.text}")
        
except requests.exceptions.Timeout:
    print(f"  ❌ ERROR: Request timed out after 30 seconds")
except requests.exceptions.ConnectionError as e:
    print(f"  ❌ ERROR: Connection error: {e}")
except Exception as e:
    print(f"  ❌ ERROR: {type(e).__name__}: {e}")

print("\n" + "=" * 70)
print("\n💡 Next Steps:")
print("  1. Verify you have a valid Grove Gateway API key")
print("  2. Contact your Grove Gateway administrator for the correct API key")
print("  3. Update GROVE_API_KEY in your .env file with the correct key")
print("  4. If you don't have Grove Gateway access, you may need to:")
print("     - Use the standard OpenAI endpoint instead")
print("     - Request access to Grove Gateway")
print("=" * 70)

