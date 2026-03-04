#!/usr/bin/env python3
"""
Drug Pricing Assistant - Streamlit UI
A simple web interface for the pharmaceutical pricing chatbot
"""

import streamlit as st
import os
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

# Load environment variables
load_dotenv()

# --- Configuration ---
MONGODB_URI = os.getenv("MONGODB_URI")
GROVE_API_KEY = os.getenv("GROVE_API_KEY")
GROVE_ENDPOINT = os.getenv("GROVE_ENDPOINT", "https://grove-gateway-prod.azure-api.net/grove-foundry-prod/openai/v1/chat/completions")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
VOYAGE_ENDPOINT = os.getenv("VOYAGE_ENDPOINT", "https://ai.mongodb.com/v1/embeddings")
VOYAGE_MODEL = os.getenv("VOYAGE_MODEL", "voyage-4-large")

# --- Page Configuration ---
st.set_page_config(
    page_title="Drug Pricing Assistant",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize MongoDB Connection ---
@st.cache_resource
def get_mongo_client():
    """Initialize MongoDB client (cached)"""
    try:
        client = MongoClient(MONGODB_URI)
        client.admin.command('ping')
        return client
    except Exception as e:
        st.error(f"❌ Failed to connect to MongoDB: {e}")
        return None

# --- Helper Functions ---
def generate_embedding(text):
    """Generate embedding for a text using Voyage AI via MongoDB AI endpoint"""
    try:
        headers = {
            "Authorization": f"Bearer {VOYAGE_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "input": [text],
            "model": VOYAGE_MODEL
        }
        response = requests.post(VOYAGE_ENDPOINT, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["data"][0]["embedding"]
    except Exception as e:
        st.error(f"❌ Embedding generation error: {e}")
        return None

def hybrid_search(query, customer=None, top_k=5):
    """Perform hybrid search using MongoDB Atlas Search + Vector Search with $rankFusion"""
    try:
        client = get_mongo_client()
        if not client:
            return []

        db = client.pricing_demo
        collection = db.customer_pricing
        
        # Generate embedding for the query
        query_embedding = generate_embedding(query)
        if not query_embedding:
            return []
        
        # Build the hybrid search pipeline
        pipeline = [
            {
                "$rankFusion": {
                    "input": {
                        "pipelines": {
                            "text": [
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
                            "vector": [
                                {
                                    "$vectorSearch": {
                                        "index": "vector_search_index",
                                        "path": "embedding",
                                        "queryVector": query_embedding,
                                        "numCandidates": 50,
                                        "limit": 20
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
                    "_id": 0,
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
        
        results = list(collection.aggregate(pipeline))
        return results
    except Exception as e:
        st.error(f"❌ Search error: {e}")
        return []

def generate_recommendation(query, search_results):
    """Generate LLM recommendation based on search results"""
    try:
        # Format search results for the prompt
        results_text = "\n".join([
            f"- {r['drug']} ({r['generic']}) at {r['pharmacy']} in {r['location']}: ${r['price']} for {r.get('supply_days', 30)} days"
            for r in search_results
        ])
        
        prompt = f"""Based on the following pharmaceutical pricing options, provide a helpful recommendation for the user's query: "{query}"

Available options:
{results_text}

Provide a clear, concise recommendation highlighting the best value option and any relevant alternatives."""

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
        
        response = requests.post(GROVE_ENDPOINT, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"❌ LLM generation error: {e}")
        return "An error occurred while generating a recommendation."

# --- Main App ---
def main():
    # Header
    st.markdown('<div class="main-header">💊 Drug Pricing Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Find the best pharmaceutical prices using AI-powered hybrid search</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This assistant helps you find the best pharmaceutical prices using:
        - **MongoDB Atlas Search** for keyword matching
        - **Vector Search** for semantic understanding
        - **GPT-5.2** for intelligent recommendations
        """)
        
        st.header("📊 System Status")
        client = get_mongo_client()
        if client:
            st.success("✅ MongoDB Connected")
            try:
                db = client.pricing_demo
                drug_count = db.drug_pricing.count_documents({})
                customer_count = db.customer_pricing.count_documents({})
                st.info(f"📦 {drug_count} drug pricing records")
                st.info(f"🔍 {customer_count} searchable records")
            except:
                pass
        else:
            st.error("❌ MongoDB Disconnected")
        
        st.header("💡 Example Queries")
        st.markdown("""
        - What's the cheapest Metformin in Houston?
        - Find Ozempic prices in Los Angeles
        - Where can I get Lisinopril in Miami?
        - Show me Atorvastatin options in New York
        """)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about pharmaceutical prices..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching for best prices..."):
                # Perform hybrid search
                search_results = hybrid_search(prompt, top_k=5)
                
                if search_results:
                    # Generate LLM recommendation
                    with st.spinner("🤖 Generating recommendation..."):
                        recommendation = generate_recommendation(prompt, search_results)
                    
                    # Display recommendation
                    st.markdown(recommendation)
                    
                    # Display search results in an expander
                    with st.expander("📋 View all search results"):
                        for i, result in enumerate(search_results, 1):
                            st.markdown(f"""
                            **{i}. {result['drug']}** ({result['generic']})
                            - 📍 Location: {result['location']}
                            - 🏪 Pharmacy: {result['pharmacy']}
                            - 💰 Price: ${result['price']}
                            - 📅 Supply: {result.get('supply_days', 30)} days
                            - 🎯 Relevance Score: {result.get('score', 0):.2f}
                            """)
                    
                    response_content = recommendation
                else:
                    response_content = "I couldn't find any matching pharmaceutical prices. Please try a different query."
                    st.warning(response_content)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_content})

if __name__ == "__main__":
    main()

