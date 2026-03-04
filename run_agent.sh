#!/bin/bash
# Drug Pricing AI Agent - Launcher Script

echo "🤖 Drug Pricing AI Agent Launcher"
echo "=================================="
echo ""
echo "Select an option:"
echo "  1) Run CLI Agent (Interactive)"
echo "  2) Run Streamlit Web UI"
echo "  3) Run Tests (All)"
echo "  4) Run Specific Test"
echo "  5) Install Dependencies"
echo "  6) Setup Database"
echo "  7) Exit"
echo ""
read -p "Enter choice [1-7]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting CLI Agent..."
        echo ""
        python agent_app.py
        ;;
    2)
        echo ""
        echo "🌐 Starting Streamlit Web UI..."
        echo "Opening browser at http://localhost:8501"
        echo ""
        streamlit run agent_streamlit_app.py
        ;;
    3)
        echo ""
        echo "🧪 Running All Tests..."
        echo ""
        python test_agent.py
        ;;
    4)
        echo ""
        echo "Select test:"
        echo "  1) Basic Search"
        echo "  2) Preference Saving"
        echo "  3) Search History"
        echo "  4) Conversation Context"
        echo "  5) Personalized Recommendations"
        echo ""
        read -p "Enter test number [1-5]: " test_num
        python test_agent.py $test_num
        ;;
    5)
        echo ""
        echo "📦 Installing Dependencies..."
        echo ""
        pip install -r requirements.txt
        echo ""
        echo "✅ Dependencies installed!"
        ;;
    6)
        echo ""
        echo "🗄️ Setting up Database..."
        echo ""
        python setup_database.py
        echo ""
        echo "✅ Database setup complete!"
        ;;
    7)
        echo ""
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Please run again and select 1-7."
        exit 1
        ;;
esac

