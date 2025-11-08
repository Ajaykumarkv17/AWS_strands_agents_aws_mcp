#!/usr/bin/env python3
"""
Test script for MCP integration with Strands Agent
"""

import logging
from memory_agent import create_memory_agent
from memory_config import get_memory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_diagram_generation():
    """Test diagram generation with memory"""
    
    print("="*60)
    print("Testing MCP Diagram Integration")
    print("="*60)
    
    user_id = "test_diagram_user"
    agent = create_memory_agent(user_id)
    memory = get_memory()
    
    # Test 1: Create initial diagram
    print("\n[Test 1] Creating initial serverless diagram...")
    query1 = "Create a simple AWS diagram with S3, Lambda, and API Gateway for a serverless web app"
    
    try:
        result1 = agent(query1)
        print(f"Response: {result1}")
        print("✓ Initial diagram created")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 2: Iterate on diagram
    print("\n[Test 2] Adding components to previous diagram...")
    query2 = "Add DynamoDB and CloudWatch to the previous diagram"
    
    try:
        result2 = agent(query2)
        print(f"Response: {result2}")
        print("✓ Diagram iteration successful")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 3: Check memory
    print("\n[Test 3] Checking stored memories...")
    try:
        memories = memory.search("diagram", user_id=user_id, limit=5)
        if isinstance(memories, dict):
            memories = memories.get('results', [])
        
        print(f"Found {len(memories)} diagram-related memories:")
        for i, mem in enumerate(memories, 1):
            print(f"  {i}. {mem.get('memory', '')[:100]}...")
        print("✓ Memory retrieval successful")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 4: Create different diagram type
    print("\n[Test 4] Creating microservices architecture...")
    query3 = "Create a microservices diagram with ECS, ALB, RDS, and ElastiCache"
    
    try:
        result3 = agent(query3)
        print(f"Response: {result3}")
        print("✓ Complex diagram created")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*60)
    print("Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    test_diagram_generation()
