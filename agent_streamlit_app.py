#!/usr/bin/env python3
"""
Drug Pricing AI Agent - Streamlit UI
Uses LangGraph for intelligent conversation with memory
"""

import streamlit as st
from datetime import datetime
from langgraph_agent_v2 import run_agent
from agent_tools import (
    get_customer_preferences,
    get_customer_search_history,
    get_conversation_history
)

# Page Configuration
st.set_page_config(
    page_title="Drug Pricing AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    .preference-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Header
    st.markdown('<div class="main-header">🤖 Drug Pricing AI Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent assistant with memory powered by LangGraph</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("👤 Customer Settings")
        
        # Customer ID input
        customer_id = st.text_input(
            "Customer ID",
            value=st.session_state.get("customer_id", "acmehealth123"),
            help="Enter your customer ID"
        )
        st.session_state.customer_id = customer_id
        
        # Session management
        if "session_id" not in st.session_state:
            st.session_state.session_id = f"{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if st.button("🔄 New Session"):
            st.session_state.session_id = f"{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state.messages = []
            st.rerun()
        
        st.info(f"Session: {st.session_state.session_id[-15:]}")
        
        # Display customer preferences
        st.header("📋 Your Preferences")
        try:
            preferences = get_customer_preferences.invoke({"customer_id": customer_id})
            if preferences:
                for pref in preferences:
                    st.markdown(f"""
                    <div class="preference-box">
                        <strong>{pref['preference_type'].replace('_', ' ').title()}</strong><br>
                        {pref['preference_value']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No preferences saved yet. Tell the agent your preferences!")
        except Exception as e:
            st.error(f"Error loading preferences: {e}")
        
        # Display search history
        st.header("🔍 Recent Searches")
        try:
            history = get_customer_search_history.invoke({"customer_id": customer_id, "limit": 5})
            if history:
                for item in history[:5]:
                    query = item.get('query', 'Unknown')
                    timestamp = item.get('timestamp', 'Unknown')
                    st.text(f"• {query}")
            else:
                st.info("No search history yet")
        except Exception as e:
            st.error(f"Error loading history: {e}")
        
        # About section
        st.header("ℹ️ About")
        st.markdown("""
        This AI agent uses:
        - **LangGraph** for state management
        - **LangChain** for tool orchestration
        - **MongoDB** for long-term memory
        - **Hybrid Search** for drug pricing
        - **GPT-5.2** for intelligent responses
        """)
        
        st.header("💡 Try These")
        st.markdown("""
        - "Find cheapest Metformin in Houston"
        - "I prefer CVS pharmacy"
        - "What are my saved preferences?"
        - "Show Ozempic prices in LA"
        - "Remember I'm in New York"
        """)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about drug prices or set preferences..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                try:
                    response = run_agent(
                        prompt,
                        customer_id=st.session_state.customer_id,
                        session_id=st.session_state.session_id
                    )
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})


if __name__ == "__main__":
    main()

