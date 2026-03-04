#!/usr/bin/env python3
"""
Test script for the Drug Pricing AI Agent
Demonstrates agent capabilities with memory
"""

from langgraph_agent import run_agent
from agent_tools import (
    get_customer_preferences,
    get_customer_search_history,
    save_customer_preference
)


def test_basic_search():
    """Test basic drug price search"""
    print("\n" + "="*60)
    print("TEST 1: Basic Drug Price Search")
    print("="*60)
    
    customer_id = "test_customer_001"
    query = "Find the cheapest Metformin in Houston"
    
    print(f"\nCustomer: {customer_id}")
    print(f"Query: {query}")
    print("\nAgent Response:")
    print("-" * 60)
    
    response = run_agent(query, customer_id)
    print(response)
    print("-" * 60)


def test_preference_saving():
    """Test saving customer preferences"""
    print("\n" + "="*60)
    print("TEST 2: Saving Customer Preferences")
    print("="*60)
    
    customer_id = "test_customer_002"
    
    # First interaction - set preference
    query1 = "I prefer CVS pharmacy"
    print(f"\nCustomer: {customer_id}")
    print(f"Query: {query1}")
    print("\nAgent Response:")
    print("-" * 60)
    
    response1 = run_agent(query1, customer_id)
    print(response1)
    print("-" * 60)
    
    # Check if preference was saved
    print("\nChecking saved preferences...")
    preferences = get_customer_preferences.invoke({"customer_id": customer_id})
    print(f"Saved preferences: {preferences}")
    
    # Second interaction - use preference
    query2 = "Show me Lipitor prices"
    print(f"\nQuery: {query2}")
    print("\nAgent Response:")
    print("-" * 60)
    
    response2 = run_agent(query2, customer_id)
    print(response2)
    print("-" * 60)


def test_search_history():
    """Test search history tracking"""
    print("\n" + "="*60)
    print("TEST 3: Search History Tracking")
    print("="*60)
    
    customer_id = "test_customer_003"
    
    # Perform multiple searches
    queries = [
        "Find Metformin in Houston",
        "What about Lipitor prices?",
        "Show me Ozempic in Los Angeles"
    ]
    
    print(f"\nCustomer: {customer_id}")
    print("\nPerforming multiple searches...")
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: {query}")
        response = run_agent(query, customer_id)
        print(f"   Response: {response[:100]}...")
    
    # Check search history
    print("\n" + "-" * 60)
    print("Search History:")
    print("-" * 60)
    
    history = get_customer_search_history.invoke({"customer_id": customer_id, "limit": 10})
    for i, item in enumerate(history, 1):
        query = item.get('query', 'Unknown')
        timestamp = item.get('timestamp', 'Unknown')
        print(f"{i}. {query} - {timestamp}")


def test_conversation_context():
    """Test conversation context (short-term memory)"""
    print("\n" + "="*60)
    print("TEST 4: Conversation Context (Short-term Memory)")
    print("="*60)
    
    customer_id = "test_customer_004"
    session_id = f"{customer_id}_test_session"
    
    # Multi-turn conversation
    conversation = [
        "Find Metformin in Houston",
        "What's the second cheapest option?",
        "How much would I save compared to the most expensive?"
    ]
    
    print(f"\nCustomer: {customer_id}")
    print(f"Session: {session_id}")
    print("\nConversation:")
    print("-" * 60)
    
    for i, query in enumerate(conversation, 1):
        print(f"\nTurn {i}")
        print(f"User: {query}")
        response = run_agent(query, customer_id, session_id)
        print(f"Agent: {response}")
        print("-" * 40)


def test_personalized_recommendations():
    """Test personalized recommendations based on preferences"""
    print("\n" + "="*60)
    print("TEST 5: Personalized Recommendations")
    print("="*60)
    
    customer_id = "test_customer_005"
    
    # Set multiple preferences
    print(f"\nCustomer: {customer_id}")
    print("\nSetting preferences...")
    
    save_customer_preference.invoke({
        "customer_id": customer_id,
        "preference_type": "preferred_pharmacy",
        "preference_value": "Walmart"
    })
    
    save_customer_preference.invoke({
        "customer_id": customer_id,
        "preference_type": "preferred_location",
        "preference_value": "Houston"
    })
    
    print("✓ Preferred pharmacy: Walmart")
    print("✓ Preferred location: Houston")
    
    # Get personalized recommendation
    query = "I need to refill my Metformin prescription"
    print(f"\nQuery: {query}")
    print("\nAgent Response:")
    print("-" * 60)
    
    response = run_agent(query, customer_id)
    print(response)
    print("-" * 60)


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 DRUG PRICING AI AGENT - TEST SUITE")
    print("="*60)
    
    try:
        test_basic_search()
        test_preference_saving()
        test_search_history()
        test_conversation_context()
        test_personalized_recommendations()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        if test_name == "1":
            test_basic_search()
        elif test_name == "2":
            test_preference_saving()
        elif test_name == "3":
            test_search_history()
        elif test_name == "4":
            test_conversation_context()
        elif test_name == "5":
            test_personalized_recommendations()
        else:
            print("Usage: python test_agent.py [1-5]")
            print("  1: Basic Search")
            print("  2: Preference Saving")
            print("  3: Search History")
            print("  4: Conversation Context")
            print("  5: Personalized Recommendations")
    else:
        run_all_tests()

