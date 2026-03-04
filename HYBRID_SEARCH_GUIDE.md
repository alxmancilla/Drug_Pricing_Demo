# Hybrid Search Implementation Guide

## Overview

The BPE Pricing Demo now uses **MongoDB Atlas Hybrid Search** combining:
- **Text Search** (`$search`) for keyword matching
- **Vector Search** (`$vectorSearch`) for semantic similarity  
- **Rank Fusion** (`$rankFusion`) to combine and rank results

This replaces the old `$regex` queries and hardcoded matching logic.

## What Changed

### ❌ Old Approach (Removed)

```python
# Old: $regex queries
def find_cheapest_drug(drug_name, city_name):
    query = {
        "drug": {"$regex": drug_name, "$options": "i"},
        "location": {"$regex": city_name, "$options": "i"}
    }
    result = drug_pricing.find(query).sort("price", 1).limit(1)
    return list(result)

# Old: Hardcoded matching in CLI
if "metformin" in user_input.lower() and "houston" in user_input.lower():
    results = find_cheapest_drug("Metformin", "Houston")
elif "lipitor" in user_input.lower() and "chicago" in user_input.lower():
    results = find_cheapest_drug("Lipitor", "Chicago")
# ... more hardcoded conditions
```

### ✅ New Approach (Hybrid Search)

```python
# New: Hybrid search with $rankFusion
def hybrid_search(query, customer=None, top_k=5):
    pipeline = [
        {
            "$rankFusion": {
                "input": {
                    "pipelines": {
                        # Text search for keywords
                        "textSearch": [
                            {
                                "$search": {
                                    "index": "text_search_index",
                                    "text": {
                                        "query": query,
                                        "path": ["drug", "generic", "location", "pharmacy"]
                                    }
                                }
                            }
                        ],
                        # Vector search for semantic similarity
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
        }
    ]
    return list(db.customer_pricing.aggregate(pipeline))
```

## Required Atlas Search Indexes

You must create **TWO** Atlas Search indexes on the `customer_pricing` collection:

### Index 1: Vector Search Index

**Name:** `vector_search_index`

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    },
    {
      "type": "filter",
      "path": "customer_id"
    }
  ]
}
```

### Index 2: Text Search Index

**Name:** `text_search_index`

```json
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
```

## How to Create Indexes

1. Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. Navigate to your cluster
3. Click **"Atlas Search"** tab
4. Click **"Create Search Index"**
5. Choose **"JSON Editor"**
6. Select database: `bpe_demo_structured`
7. Select collection: `customer_pricing`
8. Enter index name and JSON definition (see above)
9. Click **"Create Search Index"**
10. Repeat for the second index
11. Wait for both indexes to build (status: "Active")

## How Hybrid Search Works

### 1. User Query
```
"What's the cheapest Metformin in Houston?"
```

### 2. Text Search Pipeline
- Searches for keywords: "Metformin", "Houston"
- Matches against fields: `drug`, `generic`, `location`, `pharmacy`
- Returns top 20 keyword matches

### 3. Vector Search Pipeline
- Generates embedding for the query using Voyage AI
- Performs semantic similarity search
- Returns top 20 semantically similar documents

### 4. Rank Fusion
- Combines results from both pipelines
- Uses Reciprocal Rank Fusion (RRF) algorithm
- Produces final ranked list of top 5 results

### 5. LLM Generation
- Passes top results to GPT-5.2
- Generates natural language recommendation

## Benefits

### vs. $regex Queries
- ✅ **Faster**: Uses indexes instead of collection scans
- ✅ **More flexible**: Handles typos, synonyms, variations
- ✅ **Better ranking**: Combines keyword + semantic relevance
- ✅ **Scalable**: Performance doesn't degrade with data size

### vs. Hardcoded Matching
- ✅ **No maintenance**: No need to update code for new drugs/cities
- ✅ **Handles any query**: Works with any user input
- ✅ **Better UX**: More natural, conversational interface
- ✅ **Semantic understanding**: Understands intent, not just keywords

## Testing

```bash
# Run the application
python app.py
```

Try these queries:
```
What's the cheapest Metformin in Houston?
Find diabetes medication in Texas
I need blood pressure pills in New York
Ozempic pricing near Los Angeles
Generic Lipitor in Chicago
```

All queries now use hybrid search - no hardcoded logic!

## Troubleshooting

### "No results found"
- ✅ Check both Atlas Search indexes are "Active"
- ✅ Verify index names match: `text_search_index` and `vector_search_index`
- ✅ Ensure data exists in `customer_pricing` collection
- ✅ Run `python setup_database.py` to regenerate data

### "Index not found" error
- ✅ Create both required indexes (see above)
- ✅ Wait for indexes to finish building
- ✅ Check index names are exactly as specified

### Poor search results
- ✅ Verify embeddings were generated correctly
- ✅ Check vector index dimensions (should be 1536)
- ✅ Try adjusting `top_k` parameter in `hybrid_search()`

## Architecture Diagram

```
User Query
    ↓
Generate Embedding (Voyage AI)
    ↓
┌─────────────────────────────────────┐
│         $rankFusion                 │
├─────────────────┬───────────────────┤
│  Text Search    │  Vector Search    │
│  ($search)      │  ($vectorSearch)  │
│                 │                   │
│  Keywords:      │  Semantic:        │
│  - drug         │  - embedding      │
│  - generic      │  - similarity     │
│  - location     │  - 1536 dims      │
│  - pharmacy     │                   │
└─────────────────┴───────────────────┘
    ↓
Combined & Ranked Results (RRF)
    ↓
Top 5 Results
    ↓
LLM Generation (GPT-5.2)
    ↓
Natural Language Response
```

## Next Steps

1. ✅ Create both Atlas Search indexes
2. ✅ Run `python setup_database.py` to populate data
3. ✅ Test with `python app.py`
4. ✅ Try various queries to see hybrid search in action

## References

- [MongoDB Atlas Search Documentation](https://www.mongodb.com/docs/atlas/atlas-search/)
- [Vector Search Guide](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/)
- [$rankFusion Documentation](https://www.mongodb.com/docs/atlas/atlas-search/rank-fusion/)

