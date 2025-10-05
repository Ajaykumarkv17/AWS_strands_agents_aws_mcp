#!/usr/bin/env python3
"""
Shared Memory Configuration
Single source of truth for Mem0 memory instance
"""

import os
from mem0 import Memory
from dotenv import load_dotenv
from custom_nova_llm import NovaMem0LLM

load_dotenv()

# Set AWS environment variables
os.environ.setdefault('AWS_REGION', 'us-east-1')
os.environ.setdefault('OPENAI_API_KEY', 'dummy-key')

# Singleton memory instance
_memory_instance = None

def get_memory():
    """Get or create the shared memory instance"""
    global _memory_instance
    if _memory_instance is None:
        custom_llm = NovaMem0LLM({
            "model": "amazon.nova-micro-v1:0",
            "temperature": 0.2,
            "max_tokens": 500
        })
        
        config = {
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "ajay_memory_v2",
                    "embedding_model_dims": 1024,
                    "on_disk": True
                }
            },
            "embedder": {
                "provider": "aws_bedrock",
                "config": {
                    "model": "amazon.titan-embed-text-v2:0"
                }
            },
            "version": "v1.1"
        }
        
        _memory_instance = Memory.from_config(config)
        _memory_instance.llm = custom_llm
        
    return _memory_instance
