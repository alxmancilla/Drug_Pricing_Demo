#!/usr/bin/env python3
"""
Drug Pricing AI Agent - CLI Interface
Uses LangGraph for intelligent conversation with memory
"""

import sys
from datetime import datetime
from langgraph_agent_v2 import run_agent
from agent_tools import get_customer_preferences, get_customer_search_history


def display_customer_info(customer_id: str):
    """Display customer preferences and recent history"""
    print(f"\n{'='*60}")
    print(f"👤 Customer: {customer_id}")
    print(f"{'='*60}")
    
    # Get preferences
    preferences = get_customer_preferences.invoke({"customer_id": customer_id})
    if preferences:
        print("\n📋 Saved Preferences:")
        for pref in preferences:
            print(f"  • {pref['preference_type']}: {pref['preference_value']}")
    
    # Get recent searches
    history = get_customer_search_history.invoke({"customer_id": customer_id, "limit": 5})
    if history:
        print("\n🔍 Recent Searches:")
        for item in history[:3]:
            timestamp = item.get('timestamp', 'Unknown')
            query = item.get('query', 'Unknown')
            print(f"  • {query} ({timestamp})")
    
    print(f"{'='*60}\n")


def run_cli():
    """Run the interactive CLI"""
    print("\n💊 Drug Pricing AI Agent (LangGraph Edition)")
    print("=" * 60)
    print("Powered by LangGraph + LangChain with Memory")
    print("=" * 60)
    
    # Get customer ID
    customer_id = input("\n👤 Enter Customer ID (default: acmehealth123): ").strip()
    if not customer_id:
        customer_id = "acmehealth123"
    
    # Create session ID
    session_id = f"{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Display customer info
    display_customer_info(customer_id)
    
    print("Type 'exit' to quit, 'info' to see customer info, 'help' for commands.\n")
    
    while True:
        try:
            user_input = input("🧑‍⚕️ You: ").strip()
            
            if not user_input:
                print("⚠️ Please enter a valid query.")
                continue
            
            if user_input.lower() in ["exit", "quit"]:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == "info":
                display_customer_info(customer_id)
                continue
            
            if user_input.lower() == "help":
                print("\n📚 Available Commands:")
                print("  • exit/quit - Exit the application")
                print("  • info - Display customer preferences and history")
                print("  • help - Show this help message")
                print("\n💡 Example Queries:")
                print("  • What's the cheapest Metformin in Houston?")
                print("  • I prefer CVS pharmacy")
                print("  • Find Ozempic prices in Los Angeles")
                print("  • Show me my preferred pharmacy options\n")
                continue
            
            # Run the agent
            print("\n🤖 Agent: ", end="", flush=True)
            response = run_agent(user_input, customer_id, session_id)
            print(f"{response}\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    run_cli()

