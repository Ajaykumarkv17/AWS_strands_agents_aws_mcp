#!/usr/bin/env python3
"""
Strands Agent with AWS Integration
A comprehensive example of building AI agents with the Strands framework
"""

import os
import logging
from typing import Optional
from strands import Agent, tool
from strands_tools import calculator, current_time
import boto3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set AWS environment variables for proper configuration
os.environ.setdefault('AWS_REGION', 'us-east-1')

@tool
def aws_account_info() -> str:
    """
    Get current AWS account information.
    
    Returns:
        str: AWS account ID and region information
    """
    try:
        sts_client = boto3.client('sts')
        response = sts_client.get_caller_identity()
        account_id = response.get('Account', 'Unknown')
        
        # Get current region
        session = boto3.Session()
        region = session.region_name or 'Unknown'
        
        return f"AWS Account ID: {account_id}, Region: {region}"
    except Exception as e:
        return f"Error getting AWS info: {str(e)}"

@tool
def list_s3_buckets() -> str:
    """
    List S3 buckets in the current AWS account.
    
    Returns:
        str: List of S3 bucket names
    """
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
    """
    Count occurrences of a specific letter in a word.

    Args:
        word (str): The input word to search in
        letter (str): The specific letter to count

    Returns:
        int: The number of occurrences of the letter in the word
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0

    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")

    return word.lower().count(letter.lower())

@tool
def system_info() -> str:
    """
    Get system information about the current environment.
    
    Returns:
        str: System information including Python version and platform
    """
    import sys
    import platform
    
    info = {
        'Python Version': sys.version,
        'Platform': platform.platform(),
        'Architecture': platform.architecture()[0],
        'Processor': platform.processor() or 'Unknown'
    }
    
    return '\n'.join([f"{key}: {value}" for key, value in info.items()])

def create_strands_agent() -> Agent:
    """
    Create and configure a Strands agent with AWS tools.
    
    Returns:
        Agent: Configured Strands agent
    """
    # Define tools for the agent
    tools = [
        calculator,
        current_time,
        letter_counter,
        aws_account_info,
        list_s3_buckets,
        system_info
    ]
    
    # Create agent with accessible Bedrock model
    agent = Agent(
        tools=tools,
        model="us.amazon.nova-premier-v1:0"  # Using accessible model
    )
    
    return agent

def test_agent():
    """Test the Strands agent with various queries."""
    logger.info("Creating Strands agent...")
    agent = create_strands_agent()
    
    test_queries = [
        "What is the current time?",
        # "Calculate 1234 * 5678",
        # "Count the letter 'a' in the word 'banana'",
        "What is my AWS account information?",
        "List my S3 buckets",
        # "Show me system information"
    ]
    
    logger.info("Testing agent with multiple queries...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {query}")
        print('='*60)
        
        try:
            result = agent(query)
            print(f"Response: {result}")
        except Exception as e:
            print(f"Error: {str(e)}")
            logger.error(f"Error processing query '{query}': {str(e)}")

def main():
    """Main function to run the Strands agent."""
    print("Strands Agent with AWS Integration")
    print("=====================================")
    
    # Check AWS credentials
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"AWS credentials configured for account: {identity['Account']}")
    except Exception as e:
        print(f"AWS credentials not configured: {str(e)}")
        print("Please configure AWS credentials using 'aws configure' or environment variables")
        return
    
    # Run tests
    test_agent()
    
    # Interactive mode
    print(f"\n{'='*60}")
    print("Interactive Mode - Ask me anything!")
    print("Type 'quit' to exit")
    print('='*60)
    
    agent = create_strands_agent()
    
    while True:
        try:
            user_input = input("\nYour question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print(f"\nAgent response:")
            result = agent(user_input)
            print(result)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
