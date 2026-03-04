#!/usr/bin/env python3
"""
Drug Pricing Demo - Database Setup Script
==========================================
This script creates the MongoDB database, collections, indexes, and loads sample data
for the Drug Pricing Assistant application.

Requirements:
- MongoDB Atlas cluster (or local MongoDB instance)
- .env file with MONGODB_URI and VOYAGE_API_KEY configured
- pymongo, requests, python-dotenv packages installed
- Dataset files in the 'dataset' folder

Usage:
    python setup_database.py

The script will automatically:
1. Load configuration from .env file
2. Connect to MongoDB Atlas
3. Create pricing_demo database and collections
4. Load 53 pricing records from dataset files
5. Generate embeddings using Voyage AI
6. Create Atlas Search indexes (text + vector)
"""

import pymongo
from pymongo.operations import SearchIndexModel
from datetime import datetime
import sys
import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
print("=" * 70)
print("Drug Pricing Demo - Database Setup")
print("=" * 70)

# Get MongoDB URI from environment
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    print("❌ Error: MONGODB_URI not found in .env file")
    print("💡 Please add MONGODB_URI to your .env file")
    sys.exit(1)

# Get Voyage AI API Key from environment (needed for embeddings)
VOYAGE_KEY = os.getenv("VOYAGE_API_KEY")
if not VOYAGE_KEY:
    print("❌ Error: VOYAGE_API_KEY not found in .env file")
    print("💡 Please add VOYAGE_API_KEY to your .env file")
    sys.exit(1)

print("✅ Loaded configuration from .env file")

# MongoDB AI endpoint configuration
VOYAGE_ENDPOINT = "https://ai.mongodb.com/v1/embeddings"
VOYAGE_MODEL = "voyage-4-large"

# --- Connect to MongoDB ---
print("\n📡 Connecting to MongoDB...")
try:
    client = pymongo.MongoClient(MONGODB_URI)
    # Test connection
    client.admin.command('ping')
    print("✅ Connected to MongoDB successfully")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    sys.exit(1)

# --- Test MongoDB AI Endpoint ---
print("\n🚀 Testing MongoDB AI endpoint...")
try:
    headers = {
        "Authorization": f"Bearer {VOYAGE_KEY}",
        "Content-Type": "application/json"
    }
    test_payload = {
        "input": ["test"],
        "model": VOYAGE_MODEL
    }
    test_response = requests.post(VOYAGE_ENDPOINT, headers=headers, json=test_payload)
    test_response.raise_for_status()
    print("✅ MongoDB AI endpoint accessible")
except Exception as e:
    print(f"❌ Failed to access MongoDB AI endpoint: {e}")
    sys.exit(1)

# --- Create Database ---
db_name = "pricing_demo"
db = client[db_name]
print(f"\n🗄️  Using database: {db_name}")

# --- Create Collections ---
print("\n📦 Creating collections...")

# Collection 1: drug_pricing (for structured queries)
drug_pricing = db.drug_pricing
print("  ✅ Collection 'drug_pricing' ready")

# Collection 2: customer_pricing (for vector search with embeddings)
customer_pricing = db.customer_pricing
print("  ✅ Collection 'customer_pricing' ready")

# --- Load Data from Dataset Files ---
print("\n📝 Loading data from dataset folder...")

# Define dataset file paths
dataset_dir = Path("dataset")
drug_pricing_file = dataset_dir / "pricing_demo.drug_pricing.json"
customer_pricing_file = dataset_dir / "pricing_demo.customer_pricing.json"

# Check if dataset files exist
if not drug_pricing_file.exists():
    print(f"  ❌ Error: Dataset file not found: {drug_pricing_file}")
    sys.exit(1)

if not customer_pricing_file.exists():
    print(f"  ❌ Error: Dataset file not found: {customer_pricing_file}")
    sys.exit(1)

# Load drug_pricing data
print(f"  📂 Loading drug_pricing data from {drug_pricing_file}...")
try:
    with open(drug_pricing_file, 'r') as f:
        drug_pricing_data = json.load(f)
    print(f"  ✅ Loaded {len(drug_pricing_data)} drug_pricing records")
except Exception as e:
    print(f"  ❌ Error loading drug_pricing data: {e}")
    sys.exit(1)

# Load customer_pricing data
print(f"  📂 Loading customer_pricing data from {customer_pricing_file}...")
try:
    with open(customer_pricing_file, 'r') as f:
        customer_pricing_data = json.load(f)
    print(f"  ✅ Loaded {len(customer_pricing_data)} customer_pricing records")
except Exception as e:
    print(f"  ❌ Error loading customer_pricing data: {e}")
    sys.exit(1)

# Process MongoDB Extended JSON format (convert $oid and $date)
def process_mongodb_json(data):
    """Convert MongoDB Extended JSON format to Python objects"""
    processed = []
    for record in data:
        new_record = {}
        for key, value in record.items():
            if key == "_id" and isinstance(value, dict) and "$oid" in value:
                # Skip _id, let MongoDB generate new ones
                continue
            elif key == "last_updated" and isinstance(value, dict) and "$date" in value:
                # Convert $date to datetime
                new_record[key] = datetime.fromisoformat(value["$date"].replace("Z", "+00:00"))
            else:
                new_record[key] = value
        processed.append(new_record)
    return processed

drug_pricing_data = process_mongodb_json(drug_pricing_data)
customer_pricing_data = process_mongodb_json(customer_pricing_data)

print(f"  📊 Processed {len(drug_pricing_data)} drug_pricing records")
print(f"  📊 Processed {len(customer_pricing_data)} customer_pricing records")

# --- Insert into drug_pricing collection ---
print("\n💾 Inserting data into 'drug_pricing' collection...")
try:
    # Clear existing data
    drug_pricing.delete_many({})
    # Insert new data
    result = drug_pricing.insert_many(drug_pricing_data)
    print(f"  ✅ Inserted {len(result.inserted_ids)} documents")
except Exception as e:
    print(f"  ❌ Error inserting data: {e}")
    sys.exit(1)

# --- Process and insert customer_pricing data ---
print("\n🧠 Processing customer_pricing data...")

try:
    # Clear existing data
    customer_pricing.delete_many({})

    # Check if customer_pricing data already has embeddings
    has_embeddings = all("embedding" in record for record in customer_pricing_data)

    if has_embeddings:
        print(f"  ✅ Customer pricing data already has embeddings")

        # Add missing fields if needed (customer_id, supply_days, text)
        for record in customer_pricing_data:
            # Map 'customer' to 'customer_id' if needed
            if "customer" in record and "customer_id" not in record:
                # Convert customer name to customer_id format
                customer_name = record["customer"]
                record["customer_id"] = customer_name.lower().replace(" ", "") + "123"

            # Add supply_days if missing (default to 30)
            if "supply_days" not in record:
                record["supply_days"] = 30

            # Generate text field if missing
            if "text" not in record:
                generic = record.get("generic", record["drug"])
                supply_days = record.get("supply_days", 30)
                record["text"] = f"{record['drug']} {generic} at {record['pharmacy']} in {record['location']} for ${record['price']} ({supply_days} day supply)"

        # Insert documents with existing embeddings
        result = customer_pricing.insert_many(customer_pricing_data)
        print(f"  ✅ Inserted {len(result.inserted_ids)} documents with embeddings")

    else:
        print(f"  📍 No embeddings found, generating new embeddings...")

        # Prepare documents with embeddings
        documents_with_embeddings = []

        # Prepare all texts for batch embedding
        texts_for_embedding = []
        for record in customer_pricing_data:
            # Add missing fields
            if "customer" in record and "customer_id" not in record:
                customer_name = record["customer"]
                record["customer_id"] = customer_name.lower().replace(" ", "") + "123"

            if "supply_days" not in record:
                record["supply_days"] = 30

            generic = record.get("generic", record["drug"])
            supply_days = record.get("supply_days", 30)
            text = f"{record['drug']} {generic} at {record['pharmacy']} in {record['location']} for ${record['price']} ({supply_days} day supply)"
            texts_for_embedding.append(text)

        # Generate embeddings in batches using MongoDB AI endpoint
        print(f"  📍 Generating embeddings for {len(texts_for_embedding)} documents...")

        headers = {
            "Authorization": f"Bearer {VOYAGE_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "input": texts_for_embedding,
            "model": VOYAGE_MODEL
        }

        response = requests.post(VOYAGE_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()

        # Extract embeddings from response
        embedding_data = response.json()
        embeddings = [item["embedding"] for item in embedding_data["data"]]

        print(f"  ✅ Generated {len(embeddings)} embeddings")

        # Create documents with embeddings
        for i, (record, embedding, text) in enumerate(zip(customer_pricing_data, embeddings, texts_for_embedding)):
            doc_with_embedding = record.copy()
            doc_with_embedding["embedding"] = embedding
            doc_with_embedding["text"] = text
            documents_with_embeddings.append(doc_with_embedding)

        # Insert documents with embeddings
        result = customer_pricing.insert_many(documents_with_embeddings)
        print(f"  ✅ Inserted {len(result.inserted_ids)} documents with embeddings")

except Exception as e:
    print(f"  ❌ Error processing customer_pricing data: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# --- Create Indexes ---
print("\n🔍 Creating indexes...")

# Index for drug_pricing collection (structured queries)
try:
    # Index on drug name (case-insensitive searches)
    drug_pricing.create_index([("drug", pymongo.ASCENDING)])
    print("  ✅ Created index on 'drug' field")

    # Index on location
    drug_pricing.create_index([("location", pymongo.ASCENDING)])
    print("  ✅ Created index on 'location' field")

    # Compound index for drug + location queries
    drug_pricing.create_index([("drug", pymongo.ASCENDING), ("location", pymongo.ASCENDING)])
    print("  ✅ Created compound index on 'drug' and 'location'")

    # Index on price for sorting
    drug_pricing.create_index([("price", pymongo.ASCENDING)])
    print("  ✅ Created index on 'price' field")

    # Index on customer_id
    drug_pricing.create_index([("customer_id", pymongo.ASCENDING)])
    print("  ✅ Created index on 'customer_id' field")

except Exception as e:
    print(f"  ⚠️  Warning: Error creating indexes on drug_pricing: {e}")

# --- Create Atlas Search Indexes ---
print("\n🔍 Creating Atlas Search indexes...")

# Get the customer_pricing collection
collection = db["customer_pricing"]

# Vector Search Index using SearchIndexModel
print("  📍 Creating vector search index...")
try:
    vector_search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 1024,
                    "similarity": "cosine",
                    "quantization": "scalar"
                }
            ]
        },
        name="vector_search_index",
        type="vectorSearch"
    )

    result = collection.create_search_index(model=vector_search_index_model)
    print(f"  ✅ Vector search index '{result}' created successfully")
    print(f"  ⏳ Index is building in the background...")

except Exception as e:
    if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
        print(f"  ℹ️  Vector search index already exists")
    else:
        print(f"  ⚠️  Warning: Could not create vector search index: {e}")
        print(f"  💡 You may need to create it manually in MongoDB Atlas UI")

# Text Search Index using SearchIndexModel
print("  📍 Creating text search index...")
try:
    text_search_index_model = SearchIndexModel(
        definition={
            "mappings": {
                "dynamic": False,
                "fields": {
                    "drug": {
                        "type": "string",
                        "analyzer": "lucene.standard"
                    },
                    "generic": {
                        "type": "string",
                        "analyzer": "lucene.standard"
                    },
                    "location": {
                        "type": "string",
                        "analyzer": "lucene.standard"
                    },
                    "pharmacy": {
                        "type": "string",
                        "analyzer": "lucene.standard"
                    },
                    "customer_id": {
                        "type": "string"
                    }
                }
            }
        },
        name="text_search_index",
        type="search"
    )

    result = collection.create_search_index(model=text_search_index_model)
    print(f"  ✅ Text search index '{result}' created successfully")
    print(f"  ⏳ Index is building in the background...")

except Exception as e:
    if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
        print(f"  ℹ️  Text search index already exists")
    else:
        print(f"  ⚠️  Warning: Could not create text search index: {e}")
        print(f"  💡 You may need to create it manually in MongoDB Atlas UI")

# --- Manual Index Creation Instructions (Fallback) ---
print("\n" + "=" * 70)
print("📋 Atlas Search Index Definitions (for manual creation if needed)")
print("=" * 70)
print("""
If the automatic index creation failed, create these indexes manually:

================================================================================
INDEX 1: Vector Search Index (for semantic search)
================================================================================
Database: pricing_demo
Collection: customer_pricing
Index Name: vector_search_index

{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1024,
      "similarity": "cosine"
    }
  ]
}

================================================================================
INDEX 2: Text Search Index (for keyword search)
================================================================================
Database: pricing_demo
Collection: customer_pricing
Index Name: text_search_index

{
  "mappings": {
    "dynamic": false,
    "fields": {
      "drug": {
        "type": "string",
        "analyzer": "lucene.standard"
      },
      "generic": {
        "type": "string",
        "analyzer": "lucene.standard"
      },
      "location": {
        "type": "string",
        "analyzer": "lucene.standard"
      },
      "pharmacy": {
        "type": "string",
        "analyzer": "lucene.standard"
      },
      "customer_id": {
        "type": "string"
      }
    }
  }
}

To create manually:
1. Go to MongoDB Atlas (https://cloud.mongodb.com)
2. Navigate to your cluster → Atlas Search tab
3. Click "Create Search Index" → "JSON Editor"
4. Select database: pricing_demo, collection: customer_pricing
5. Paste the JSON definition above
6. Click "Create Search Index"

Note: voyage-4-large uses 1024 dimensions for embeddings
""")

# --- Summary ---
print("=" * 70)
print("✅ Database Setup Complete!")
print("=" * 70)
print(f"""
Database: {db_name}
Collections created:
  - drug_pricing: {drug_pricing.count_documents({})} documents
  - customer_pricing: {customer_pricing.count_documents({})} documents

Sample queries you can try:
  - "What's the cheapest Metformin in Houston?"
  - "Find Lipitor prices in Chicago"
  - "Where can I get Atorvastatin in New York?"
  - "Ozempic pricing in Los Angeles"
  - "Trulicity in Atlanta"

Next steps:
  1. ✅ Database and collections created
  2. ✅ Data loaded and embeddings generated
  3. ✅ Atlas Search indexes created (or check instructions above if failed)
  4. Run the application:
     - CLI: python app.py
     - Web UI: ./run_streamlit.sh (or run_streamlit.bat on Windows)

Configuration loaded from .env file:
  - MONGODB_URI: {MONGODB_URI[:30]}...
  - VOYAGE_API_KEY: ✅ Configured
  - GROVE_API_KEY: Required for running the app

""")
print("=" * 70)

