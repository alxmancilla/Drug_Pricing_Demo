# BPE Structured Pricing Assistant - Version 5.0 (Hybrid Search with $rankFusion)
# Uses MongoDB Atlas Search ($search) + Vector Search with $rankFusion
# No $regex queries - all searches use Atlas Search indexes

# --- 📚 1. Install Requirements (if needed) ---
#!pip install pymongo requests

# --- 🛠️ 2. Import Libraries ---
import pymongo
import requests
import logging

# --- 🏗️ 3. Setup Logging ---
logging.basicConfig(level=logging.INFO)

# --- 🔐 4. Set Up API Keys and MongoDB URI ---
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in environment variables. Please check your .env file.")

# Grove Gateway (OpenAI) Configuration
GROVE_API_KEY = os.getenv("GROVE_API_KEY")
if not GROVE_API_KEY:
    raise ValueError("GROVE_API_KEY not found in environment variables. Please check your .env file.")
GROVE_ENDPOINT = os.getenv("GROVE_ENDPOINT", "https://grove-gateway-prod.azure-api.net/grove-foundry-prod/openai/v1/chat/completions")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")

# MongoDB AI (Voyage) Configuration
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
if not VOYAGE_API_KEY:
    raise ValueError("VOYAGE_API_KEY not found in environment variables. Please check your .env file.")
VOYAGE_ENDPOINT = os.getenv("VOYAGE_ENDPOINT", "https://ai.mongodb.com/v1/embeddings")
VOYAGE_MODEL = os.getenv("VOYAGE_MODEL", "voyage-4-large")

# --- 📦 5. Initialize Clients ---
client = pymongo.MongoClient(MONGODB_URI)
db = client.pricing_demo
drug_pricing = db.drug_pricing

# --- 🧱 6. Example Document Structure ---
example_doc = {
    "drug": "Lipitor",
    "generic": "Atorvastatin",
    "location": "New York City",
    "pharmacy": "Walmart",
    "price": 12,
    "supply_days": 30,
    "customer_id": "acmehealth123",
    "last_updated": {"$date": "2024-04-26T00:00:00Z"}
}

# --- 🔍 7. Hybrid Search Function (Text + Vector with $rankFusion) ---
def hybrid_search(query, customer=None, top_k=5):
    """
    Performs hybrid search combining:
    - Atlas Search ($search) for keyword matching on drug, generic, location
    - Vector Search ($vectorSearch) for semantic similarity
    - $rankFusion to combine and rank results
    """
    try:
        # Generate embedding for the query
        headers = {
            "Authorization": f"Bearer {VOYAGE_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "input": [query],
            "model": VOYAGE_MODEL
        }

        response = requests.post(VOYAGE_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()

        # Extract embedding from response
        embedding_data = response.json()
        query_vector = embedding_data["data"][0]["embedding"]

        # Build hybrid search pipeline with $rankFusion
        pipeline = [
            {
                "$rankFusion": {
                    "input": {
                        "pipelines": {
                            # Pipeline 1: Text search using Atlas Search
                            "textSearch": [
                                {
                                    "$search": {
                                        "index": "text_search_index",
                                        "text": {
                                            "query": query,
                                            "path": ["drug", "generic", "location", "pharmacy"]
                                        }
                                    }
                                },
                                {"$limit": 20}
                            ],
                            # Pipeline 2: Vector search for semantic similarity
                            "vectorSearch": [
                                {
                                    "$vectorSearch": {
                                        "queryVector": query_vector,
                                        "path": "embedding",
                                        "numCandidates": 50,
                                        "limit": 20,
                                        "index": "vector_search_index"
                                    }
                                }
                            ]
                        }
                    }
                }
            },
            {"$limit": top_k},
            {
                "$project": {
                    "drug": 1,
                    "generic": 1,
                    "location": 1,
                    "pharmacy": 1,
                    "price": 1,
                    "supply_days": 1,
                    "customer_id": 1,
                    "score": {"$meta": "searchScore"}
                }
            }
        ]

        # Add customer filter if provided
        if customer:
            pipeline.insert(1, {"$match": {"customer_id": customer}})

        results = list(db.customer_pricing.aggregate(pipeline))

        if results:
            logging.info(f"Hybrid search found {len(results)} results for query: {query}")
        else:
            logging.warning(f"No results found for query: {query}")

        return results

    except Exception as e:
        logging.error(f"Hybrid search error: {e}")
        import traceback
        traceback.print_exc()
        return []

# --- ✨ 8. GPT-4 Recommendation Generation ---
def generate_recommendation(user_query, customer=None):
    """
    Generate pricing recommendation using hybrid search + LLM
    """
    results = hybrid_search(user_query, customer, top_k=5)

    if not results:
        return "No relevant pricing information found. Please try rephrasing your query or check if the data exists in the database."

    # Format results for context
    context = "\n".join(
        f"- {doc.get('drug', 'Unknown Drug')} ({doc.get('generic', 'N/A')}) at {doc.get('pharmacy', 'Unknown Pharmacy')} in {doc.get('location', 'Unknown Location')} for ${doc.get('price', 'N/A')} ({doc.get('supply_days', 'N/A')} day supply)"
        for doc in results
    )

    prompt = f"""
    You are a helpful assistant in a pharmaceutical pricing recommendation system.
    The user asked: \"{user_query}\"

    Here are the most relevant pricing options from our database:
    {context}

    Please provide a concise and helpful pricing recommendation. Focus on:
    1. The best price option
    2. Alternative options if available
    3. Any relevant details about the medication

    Keep your response brief and actionable.
    """

    try:
        # Call Grove Gateway endpoint for OpenAI
        headers = {
            "Content-Type": "application/json",
            "api-key": GROVE_API_KEY
        }

        payload = {
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful pharmaceutical pricing assistant. Provide clear, concise recommendations based on the pricing data provided."},
                {"role": "user", "content": prompt}
            ],
            "max_completion_tokens": 300
        }

        response = requests.post(GROVE_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()

        # Extract response from Grove Gateway
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.error(f"LLM generation error: {e}")
        import traceback
        traceback.print_exc()
        return "An error occurred while generating a recommendation."

# --- 🖥️ 9. Interactive CLI Simulation ---
def run_cli():
    print("\n💊 Drug Pricing Assistant (Hybrid Search Edition)")
    print("=" * 60)
    print("Using MongoDB Atlas Search + Vector Search with $rankFusion")
    print("Type 'exit' to quit.\n")
    while True:
        user_input = input("🧑\u200d⚕️ You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        if not user_input:
            print("⚠️ Please enter a valid query.")
            continue

        # Always use hybrid search - no hardcoded matching
        print("\n🔍 Searching using hybrid approach (text + vector)...")
        answer = generate_recommendation(user_input)
        print(f"\n🤖 Drug Pricing Assistant:\n{answer}\n")

# --- 🚀 10. Run the Assistant ---
run_cli()
