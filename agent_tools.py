"""
LangChain Tools for Drug Pricing Agent
Provides tools for hybrid search, memory management, and customer preferences
"""

import os
import requests
from typing import Optional, Dict, List, Any
from datetime import datetime
from langchain_core.tools import tool
from langchain_mongodb import MongoDBChatMessageHistory
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
VOYAGE_ENDPOINT = os.getenv("VOYAGE_ENDPOINT", "https://ai.mongodb.com/v1/embeddings")
VOYAGE_MODEL = os.getenv("VOYAGE_MODEL", "voyage-4-large")

# MongoDB Client
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client.pricing_demo


def generate_embedding(text: str) -> Optional[List[float]]:
    """Generate embedding using Voyage AI"""
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
        return response.json()["data"][0]["embedding"]
    except Exception as e:
        print(f"Embedding error: {e}")
        return None


@tool
def search_drug_prices(query: str, customer_id: Optional[str] = None, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for drug prices using hybrid search (text + vector).
    
    Args:
        query: Natural language query about drug pricing (e.g., "Metformin in Houston")
        customer_id: Optional customer ID to filter results
        top_k: Number of results to return (default: 5)
    
    Returns:
        List of drug pricing records with drug, pharmacy, location, price, etc.
    """
    try:
        # Generate embedding for the query
        query_embedding = generate_embedding(query)
        if not query_embedding:
            return []
        
        # Build hybrid search pipeline with $rankFusion
        pipeline = [
            {
                "$rankFusion": {
                    "input": {
                        "pipelines": {
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
                            "vectorSearch": [
                                {
                                    "$vectorSearch": {
                                        "queryVector": query_embedding,
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
        
        # Add customer filter if provided
        if customer_id:
            pipeline.insert(1, {"$match": {"customer_id": customer_id}})
        
        results = list(db.customer_pricing.aggregate(pipeline))
        return results
    
    except Exception as e:
        print(f"Search error: {e}")
        return []


@tool
def save_customer_preference(customer_id: str, preference_type: str, preference_value: str) -> str:
    """
    Save a customer preference to long-term memory.

    Args:
        customer_id: Customer identifier
        preference_type: Type of preference (e.g., "preferred_pharmacy", "preferred_location", "medication")
        preference_value: The preference value

    Returns:
        Confirmation message
    """
    try:
        db.customer_preferences.update_one(
            {"customer_id": customer_id, "preference_type": preference_type},
            {
                "$set": {
                    "preference_value": preference_value,
                    "last_updated": datetime.utcnow()
                }
            },
            upsert=True
        )
        return f"Saved {preference_type}: {preference_value} for customer {customer_id}"
    except Exception as e:
        return f"Error saving preference: {e}"


@tool
def get_customer_preferences(customer_id: str) -> List[Dict[str, Any]]:
    """
    Retrieve customer preferences from long-term memory.

    Args:
        customer_id: Customer identifier

    Returns:
        List of customer preferences
    """
    try:
        preferences = list(db.customer_preferences.find(
            {"customer_id": customer_id},
            {"_id": 0, "preference_type": 1, "preference_value": 1, "last_updated": 1}
        ))
        return preferences
    except Exception as e:
        print(f"Error retrieving preferences: {e}")
        return []


@tool
def get_customer_search_history(customer_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Retrieve customer's recent search history from long-term memory.

    Args:
        customer_id: Customer identifier
        limit: Number of recent searches to return

    Returns:
        List of recent searches
    """
    try:
        history = list(db.customer_search_history.find(
            {"customer_id": customer_id}
        ).sort("timestamp", -1).limit(limit))

        # Convert ObjectId to string for JSON serialization
        for item in history:
            item["_id"] = str(item["_id"])

        return history
    except Exception as e:
        print(f"Error retrieving search history: {e}")
        return []


@tool
def save_search_to_history(customer_id: str, query: str, results_count: int) -> str:
    """
    Save a search query to customer's search history.

    Args:
        customer_id: Customer identifier
        query: The search query
        results_count: Number of results returned

    Returns:
        Confirmation message
    """
    try:
        db.customer_search_history.insert_one({
            "customer_id": customer_id,
            "query": query,
            "results_count": results_count,
            "timestamp": datetime.utcnow()
        })
        return f"Saved search to history for customer {customer_id}"
    except Exception as e:
        return f"Error saving search history: {e}"


# Helper function to get conversation history (short-term memory)
def get_conversation_history(session_id: str) -> MongoDBChatMessageHistory:
    """
    Get conversation history for a session (short-term memory).

    Args:
        session_id: Unique session identifier (e.g., customer_id + timestamp)

    Returns:
        MongoDBChatMessageHistory instance
    """
    return MongoDBChatMessageHistory(
        connection_string=MONGODB_URI,
        database_name="pricing_demo",
        collection_name="conversation_history",
        session_id=session_id
    )


# Export all tools
ALL_TOOLS = [
    search_drug_prices,
    save_customer_preference,
    get_customer_preferences,
    get_customer_search_history,
    save_search_to_history
]

