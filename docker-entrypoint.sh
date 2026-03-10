#!/bin/bash
# Docker entrypoint script for Drug Pricing AI Agent

set -e

echo "🚀 Starting Drug Pricing AI Agent..."

# Check if required environment variables are set
if [ -z "$MONGODB_URI" ]; then
    echo "❌ ERROR: MONGODB_URI is not set"
    exit 1
fi

if [ -z "$GROVE_API_KEY" ]; then
    echo "❌ ERROR: GROVE_API_KEY is not set"
    exit 1
fi

if [ -z "$VOYAGE_API_KEY" ]; then
    echo "❌ ERROR: VOYAGE_API_KEY is not set"
    exit 1
fi

echo "✅ Environment variables validated"

# Check if dataset exists
if [ ! -f "/app/dataset/pricing_demo.customer_pricing.json" ]; then
    echo "⚠️  Dataset not found. Generating dataset..."
    python generate_datasets.py
    echo "✅ Dataset generated"
fi

# Optional: Setup database (uncomment if you want to auto-setup on container start)
# echo "🔧 Setting up database..."
# python setup_database.py

echo "🌐 Starting Streamlit UI on port 8501..."

# Execute the main command
exec "$@"

