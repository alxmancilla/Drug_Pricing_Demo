"""
LangGraph AI Agent for Drug Pricing Assistant (Version 2)
Uses direct API calls to Grove Gateway instead of LangChain's ChatOpenAI
This version properly handles Grove Gateway authentication
"""

import os
import json
import requests
from typing import TypedDict, Annotated, Sequence, Dict, Any
from datetime import datetime
import operator

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool as langchain_tool
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

from agent_tools import (
    ALL_TOOLS,
    get_conversation_history,
    search_drug_prices,
    get_customer_preferences,
    save_customer_preference,
    get_customer_search_history,
    save_search_to_history
)

load_dotenv()

# Configuration
GROVE_API_KEY = os.getenv("GROVE_API_KEY")
GROVE_ENDPOINT = os.getenv("GROVE_ENDPOINT", "https://grove-gateway-prod.azure-api.net/grove-foundry-prod/openai/v1/chat/completions")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")


# Define the agent state
class AgentState(TypedDict):
    """State of the agent conversation"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    customer_id: str
    session_id: str
    customer_preferences: dict
    search_results: list


def call_grove_api(messages: list, tools: list = None) -> Dict[str, Any]:
    """
    Call Grove Gateway API directly with proper authentication
    
    Args:
        messages: List of message dicts for the conversation
        tools: Optional list of tool definitions
    
    Returns:
        API response dict
    """
    headers = {
        "Content-Type": "application/json",
        "api-key": GROVE_API_KEY  # Grove Gateway uses "api-key" header
    }
    
    payload = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "max_completion_tokens": 500,
        "temperature": 0.7
    }
    
    # Add tools if provided
    if tools:
        payload["tools"] = tools
    
    try:
        response = requests.post(GROVE_ENDPOINT, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ Grove API Error: {e}")
        print(f"Response: {e.response.text}")
        raise
    except Exception as e:
        print(f"❌ Error calling Grove API: {e}")
        raise


def convert_langchain_tools_to_openai_format(langchain_tools: list) -> list:
    """Convert LangChain tools to OpenAI function calling format"""
    openai_tools = []
    
    for tool in langchain_tools:
        tool_def = {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
        
        # Extract parameters from tool schema
        if hasattr(tool, 'args_schema') and tool.args_schema:
            schema = tool.args_schema.schema()
            if 'properties' in schema:
                tool_def["function"]["parameters"]["properties"] = schema['properties']
            if 'required' in schema:
                tool_def["function"]["parameters"]["required"] = schema['required']
        
        openai_tools.append(tool_def)
    
    return openai_tools


def execute_tool_call(tool_name: str, tool_args: dict) -> str:
    """Execute a tool by name with given arguments"""
    tool_map = {tool.name: tool for tool in ALL_TOOLS}
    
    if tool_name not in tool_map:
        return f"Error: Tool {tool_name} not found"
    
    try:
        tool = tool_map[tool_name]
        result = tool.invoke(tool_args)
        return json.dumps(result) if not isinstance(result, str) else result
    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"


def should_continue(state: AgentState) -> str:
    """Determine if the agent should continue or end"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Check if last message is an AIMessage with tool calls
    if isinstance(last_message, AIMessage) and hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    
    # Check if last message has additional_kwargs with tool_calls (OpenAI format)
    if isinstance(last_message, AIMessage) and last_message.additional_kwargs.get("tool_calls"):
        return "continue"
    
    return "end"


def call_model(state: AgentState) -> dict:
    """Call the LLM with the current state"""
    messages = state["messages"]
    customer_id = state.get("customer_id", "unknown")
    
    # Build system message
    system_content = f"""You are a helpful pharmaceutical pricing assistant.
You have access to tools to search drug prices, manage customer preferences, and access search history.

Current customer ID: {customer_id}

When helping customers:
1. Use search_drug_prices to find current pricing information
2. Use get_customer_preferences to understand their preferences (preferred pharmacy, location, etc.)
3. Use save_customer_preference to remember important preferences they mention
4. Use get_customer_search_history to understand their past searches
5. Use save_search_to_history to track their searches

Always provide clear, actionable recommendations based on the data you find.
"""
    
    # Convert messages to API format
    api_messages = [{"role": "system", "content": system_content}]
    
    for msg in messages:
        if isinstance(msg, HumanMessage):
            api_messages.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            msg_dict = {"role": "assistant", "content": msg.content or ""}
            if msg.additional_kwargs.get("tool_calls"):
                msg_dict["tool_calls"] = msg.additional_kwargs["tool_calls"]
            api_messages.append(msg_dict)
        elif isinstance(msg, ToolMessage):
            api_messages.append({
                "role": "tool",
                "tool_call_id": msg.tool_call_id,
                "content": msg.content
            })
    
    # Convert tools to OpenAI format
    tools = convert_langchain_tools_to_openai_format(ALL_TOOLS)
    
    # Call Grove API
    response = call_grove_api(api_messages, tools)

    # Extract response
    choice = response["choices"][0]
    message = choice["message"]

    # Get content - ensure it's never None
    content = message.get("content") or ""

    # Create AIMessage
    ai_message = AIMessage(
        content=content,
        additional_kwargs={"tool_calls": message.get("tool_calls", [])}
    )

    return {"messages": [ai_message]}


def call_tools(state: AgentState) -> dict:
    """Execute the tools requested by the LLM"""
    messages = state["messages"]
    last_message = messages[-1]

    tool_messages = []

    # Get tool calls from the last message
    tool_calls = last_message.additional_kwargs.get("tool_calls", [])

    if not tool_calls:
        print("⚠️ No tool calls found in message")
        return {"messages": []}

    for tool_call in tool_calls:
        try:
            function = tool_call["function"]
            tool_name = function["name"]
            tool_call_id = tool_call["id"]

            # Parse arguments safely
            try:
                tool_args = json.loads(function["arguments"])
            except json.JSONDecodeError as e:
                print(f"⚠️ Failed to parse tool arguments: {function['arguments']}")
                tool_args = {}

            print(f"🔧 Executing tool: {tool_name} with args: {tool_args}")

            # Execute the tool
            result = execute_tool_call(tool_name, tool_args)

            print(f"✅ Tool result: {result[:200] if isinstance(result, str) else result}")

            # Create tool message
            tool_message = ToolMessage(
                content=str(result),  # Ensure content is always a string
                tool_call_id=tool_call_id,
                name=tool_name
            )
            tool_messages.append(tool_message)

        except Exception as e:
            print(f"❌ Error executing tool {tool_call.get('function', {}).get('name', 'unknown')}: {e}")
            # Create error message
            tool_message = ToolMessage(
                content=f"Error: {str(e)}",
                tool_call_id=tool_call.get("id", "unknown"),
                name=tool_call.get("function", {}).get("name", "unknown")
            )
            tool_messages.append(tool_message)

    return {"messages": tool_messages}


# Build the graph
def create_agent_graph():
    """Create the LangGraph agent workflow"""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tools)

    # Set entry point
    workflow.set_entry_point("agent")

    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )

    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")

    # Compile with memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    return app


# Create the agent
agent_graph = create_agent_graph()


def run_agent(user_input: str, customer_id: str = "acmehealth123", session_id: str = None) -> str:
    """
    Run the agent with a user input

    Args:
        user_input: User's query
        customer_id: Customer identifier
        session_id: Session identifier (auto-generated if not provided)

    Returns:
        Agent's response
    """
    if session_id is None:
        session_id = f"{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Get customer preferences
    try:
        preferences_result = get_customer_preferences.invoke({"customer_id": customer_id})
        preferences = {p["preference_type"]: p["preference_value"] for p in preferences_result}
    except:
        preferences = {}

    # Create initial state
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "customer_id": customer_id,
        "session_id": session_id,
        "customer_preferences": preferences,
        "search_results": []
    }

    # Run the agent
    config = {"configurable": {"thread_id": session_id}}

    try:
        result = agent_graph.invoke(initial_state, config)

        # Extract the final response - look for the last AIMessage with content
        for message in reversed(result["messages"]):
            if isinstance(message, AIMessage) and message.content:
                return message.content

        # If no AIMessage with content found, return a default message
        return "I processed your request but didn't generate a response. Please try rephrasing your question."

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Agent error: {error_msg}")
        import traceback
        traceback.print_exc()

        # Provide more helpful error messages
        if "validation error" in error_msg.lower():
            return "I encountered a technical issue processing your request. Please try again with a simpler query."
        elif "401" in error_msg:
            return "Authentication error: Please check your Grove API key in the .env file."
        elif "timeout" in error_msg.lower():
            return "The request timed out. Please try again."
        else:
            return f"I encountered an error: {error_msg}"

