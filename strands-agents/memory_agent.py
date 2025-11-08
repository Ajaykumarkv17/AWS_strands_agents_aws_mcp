#!/usr/bin/env python3
"""
Enhanced Strands Agent with Mem0 Memory Integration
Provides personalized AI interactions with persistent memory
"""

import os
import logging
from typing import Optional, Dict, Any, List
from strands import Agent, tool
from strands_tools import calculator, current_time
import boto3
import json
from memory_config import get_memory
from diagram_generator import create_diagram_tool
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get shared memory instance
memory = get_memory()

@tool
def search_memory(query: str, user_id: str = "default") -> str:
    """
    Search through user's memory for relevant information.
    
    Args:
        query (str): Search query to find relevant memories
        user_id (str): User identifier for personalized memory
        
    Returns:
        str: Relevant memories or indication if none found
    """
    try:
        result = memory.search(query, user_id=user_id, limit=5)
        memories = result.get('results', []) if isinstance(result, dict) else result
        if memories:
            memory_text = "\n".join([f"- {mem['memory']}" for mem in memories])
            return f"Found relevant memories:\n{memory_text}"
        return "No relevant memories found."
    except Exception as e:
        return f"Error searching memory: {str(e)}"

@tool
def save_memory(content: str, user_id: str = "default") -> str:
    """
    Save important information to user's memory.
    
    Args:
        content (str): Information to save to memory
        user_id (str): User identifier for personalized memory
        
    Returns:
        str: Confirmation of memory save
    """
    try:
        result = memory.add(content, user_id=user_id)
        return f"Successfully saved to memory"
    except Exception as e:
        return f"Error saving memory: {str(e)}"

@tool
def get_user_preferences(user_id: str = "default") -> str:
    """
    Retrieve user preferences and personal information.
    
    Args:
        user_id (str): User identifier
        
    Returns:
        str: User preferences and personal details
    """
    try:
        result = memory.search("preferences likes dislikes favorite", user_id=user_id, limit=10)
        preferences = result.get('results', []) if isinstance(result, dict) else result
        if preferences:
            pref_text = "\n".join([f"- {mem['memory']}" for mem in preferences])
            return f"User preferences:\n{pref_text}"
        return "No user preferences found yet."
    except Exception as e:
        return f"Error retrieving preferences: {str(e)}"

@tool
def aws_account_info() -> str:
    """Get current AWS account information."""
    try:
        sts_client = boto3.client('sts')
        response = sts_client.get_caller_identity()
        account_id = response.get('Account', 'Unknown')
        session = boto3.Session()
        region = session.region_name or 'Unknown'
        return f"AWS Account ID: {account_id}, Region: {region}"
    except Exception as e:
        return f"Error getting AWS info: {str(e)}"

@tool
def list_s3_buckets() -> str:
    """List S3 buckets in the current AWS account."""
    try:
        s3_client = boto3.client('s3')
        response = s3_client.list_buckets()
        if not response.get('Buckets'):
            return "No S3 buckets found in this account."
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        return f"S3 Buckets ({len(bucket_names)}): {', '.join(bucket_names)}"
    except Exception as e:
        return f"Error listing S3 buckets: {str(e)}"

@tool
def letter_counter(word: str, letter: str) -> int:
    """Count occurrences of a specific letter in a word."""
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0
    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")
    return word.lower().count(letter.lower())

@tool
def system_info() -> str:
    """Get system information about the current environment."""
    import sys
    import platform
    
    info = {
        'Python Version': sys.version,
        'Platform': platform.platform(),
        'Architecture': platform.architecture()[0],
        'Processor': platform.processor() or 'Unknown'
    }
    
    return '\n'.join([f"{key}: {value}" for key, value in info.items()])

@tool
def personalized_greeting(user_id: str = "default") -> str:
    """
    Generate a personalized greeting based on user's memory.
    
    Args:
        user_id (str): User identifier
        
    Returns:
        str: Personalized greeting message
    """
    try:
        # Search for user's name and preferences
        name_result = memory.search("name called", user_id=user_id, limit=3)
        name_memories = name_result.get('results', []) if isinstance(name_result, dict) else name_result
        
        pref_result = memory.search("likes enjoys favorite", user_id=user_id, limit=3)
        pref_memories = pref_result.get('results', []) if isinstance(pref_result, dict) else pref_result
        
        greeting = "Hello"
        if name_memories:
            for mem in name_memories:
                if "name is" in mem['memory'].lower() or "called" in mem['memory'].lower():
                    greeting = f"Hello {mem['memory'].split()[-1]}"
                    break
        
        if pref_memories:
            interests = ", ".join([mem['memory'] for mem in pref_memories[:2]])
            greeting += f"! I remember you're interested in {interests}."
        else:
            greeting += "! Nice to see you again."
            
        return greeting
    except Exception as e:
        return f"Hello! Error retrieving personalized info: {str(e)}"

def create_memory_agent(user_id: str = "default") -> Agent:
    """
    Create and configure a Strands agent with memory capabilities.
    
    Args:
        user_id (str): User identifier for personalized memory
        
    Returns:
        Agent: Configured memory-enabled Strands agent
    """
    tools = [
        calculator,
        current_time,
        search_memory,
        save_memory,
        aws_account_info,
        list_s3_buckets
    ]
    
    # Add diagram generation tool (Windows-compatible)
    try:
        diagram_tool = create_diagram_tool()
        tools.append(diagram_tool)
        logger.info("Added Windows-compatible diagram generator")
    except Exception as e:
        logger.warning(f"Could not load diagram generator: {e}")
    
    system_prompt = f"""
You are a helpful AI assistant with memory and diagram generation capabilities.

When users share personal info (name, preferences, goals), save it using save_memory.
When users ask about past conversations, use search_memory.
When users ask to create or modify diagrams, use diagram tools and search memory for previous diagram context.

For diagrams:
1. Use MCP tools to create AWS architecture diagrams
2. Search memory for previous diagrams to iterate
3. Save diagram context to memory

User: {user_id}

Be concise. No thinking tags.
    """
    
    agent = Agent(
        tools=tools,
        model="us.amazon.nova-premier-v1:0",
        system_prompt=system_prompt
    )
    
    return agent

def test_memory_agent():
    """Test the memory-enabled Strands agent."""
    logger.info("Creating memory-enabled Strands agent...")
    
    user_id = "test_user"
    agent = create_memory_agent(user_id)
    
    test_scenarios = [
        "Hi, my name is Alice and I love machine learning and AWS",
        "What's my name?",
        "What do I like?",
        "I'm planning to build a chatbot using Python",
        "What projects am I working on?",
        "Calculate 15 * 23",
        "What's the current time?",
        "What's my AWS account info?"
    ]
    
    logger.info("Testing memory agent with conversation scenarios...")
    
    for i, query in enumerate(test_scenarios, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {query}")
        print('='*60)
        
        try:
            result = agent(query)
            print(f"Response: {result}")
        except Exception as e:
            print(f"Error: {str(e)}")
            logger.error(f"Error processing query '{query}': {str(e)}")

def interactive_memory_chat():
    """Interactive chat with memory-enabled agent."""
    print("Enhanced Strands Agent with Memory")
    print("==================================")
    
    # Get user ID
    user_id = input("Enter your user ID (or press Enter for 'default'): ").strip() or "default"
    
    agent = create_memory_agent(user_id)
    
    print(f"\nMemory-enabled chat started for user: {user_id}")
    print("Type 'quit' to exit, 'memory' to see your memories")
    print('='*60)
    
    while True:
        try:
            user_input = input(f"\n[{user_id}]: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! Your memories have been saved.")
                break
            
            if user_input.lower() == 'memory':
                # Show user's memories
                result = memory.get_all(user_id=user_id)
                memories = result.get('results', []) if isinstance(result, dict) else result
                if memories:
                    print("\nYour stored memories:")
                    for i, mem in enumerate(memories[:10], 1):
                        print(f"{i}. {mem['memory']}")
                else:
                    print("No memories stored yet.")
                continue
            
            if not user_input:
                continue
            
            print(f"\nAgent: ", end="")
            result = agent(user_input)
            print(result)
            
        except KeyboardInterrupt:
            print("\nGoodbye! Your memories have been saved.")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Check AWS credentials
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"AWS credentials configured for account: {identity['Account']}")
    except Exception as e:
        print(f"AWS credentials not configured: {str(e)}")
    
    # Run tests first
    # print("\n" + "="*60)
    # print("RUNNING AUTOMATED TESTS")
    # print("="*60)
    # test_memory_agent()
    
    # # Then interactive mode
    # print("\n" + "="*60)
    # print("STARTING INTERACTIVE MODE")
    # print("="*60)
    # interactive_memory_chat()