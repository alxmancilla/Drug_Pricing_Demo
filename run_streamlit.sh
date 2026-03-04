#!/bin/bash

# Drug Pricing Assistant - Streamlit Quick Start Script

echo "======================================================================"
echo "💊 Drug Pricing Assistant - Streamlit UI"
echo "======================================================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "   Please create a .env file with your API keys and MongoDB URI"
    echo "   See .env.example for reference"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "❌ Error: Streamlit installation failed"
    echo "   Try manually: pip install streamlit"
    exit 1
fi

echo ""
echo "✅ All dependencies installed"
echo ""
echo "======================================================================"
echo "🚀 Starting Streamlit App..."
echo "======================================================================"
echo ""
echo "The app will open in your browser at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Streamlit app
streamlit run streamlit_app.py

