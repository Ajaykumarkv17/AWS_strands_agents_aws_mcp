#!/usr/bin/env python3
"""
Test MCP Tools Loading and Diagram Generation
"""

import asyncio
import logging
from mcp_diagram_client import get_diagram_mcp_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_diagram_generation(tools):
    """Test generate_diagram tool with sample input"""
    print("\n" + "="*60)
    print("Testing Diagram Generation")
    print("="*60)
    
    test_code = '''
from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.database import Dynamodb

with Diagram("Simple Serverless", show=False, filename="test_serverless"):
    api = APIGateway("API")
    lambda_fn = Lambda("Function")
    db = Dynamodb("Database")
    
    api >> lambda_fn >> db
'''
    
    print("\nTest Input:")
    print(test_code)
    print("\nGenerating diagram...")
    
    try:
        generate_tool = next((t for t in tools if t.tool_name == 'generate_diagram'), None)
        if not generate_tool:
            print("\n[FAILED]: generate_diagram tool not found")
            return False
        
        from strands import Agent
        temp_agent = Agent(tools=[generate_tool], model="us.amazon.nova-premier-v1:0")
        result = temp_agent(f"Generate a diagram with this code: {test_code}")
        print("\n[SUCCESS]")
        print(f"Result: {result}")
        return True
    except Exception as e:
        print(f"\n[FAILED]: {str(e)}")
        logger.error(f"Diagram generation failed: {e}", exc_info=True)
        return False

async def main():
    print("="*60)
    print("MCP Tools Test Suite")
    print("="*60)
    
    print("\n1. Loading MCP tools...")
    client = get_diagram_mcp_client()
    tools = await client.load_tools()
    
    print(f"\n2. Result: {len(tools)} tools loaded")
    
    if tools:
        print("\n3. Available tools:")
        for i, tool in enumerate(tools, 1):
            tool_name = getattr(tool, '_name', getattr(tool, 'tool_name', str(tool)))
            print(f"   {i}. {tool_name}")
    else:
        print("\n3. No tools loaded")
        return
    
    await test_diagram_generation(tools)
    
    print("\n" + "="*60)
    print("Test Complete")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
