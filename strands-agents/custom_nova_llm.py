#!/usr/bin/env python3
"""Custom Nova LLM wrapper for Mem0 compatibility"""

import json
import boto3
from typing import List, Dict, Any, Optional, Union

class NovaMem0LLM:
    """Custom LLM wrapper for Amazon Nova models compatible with Mem0"""
    
    def __init__(self, config: Dict[str, Any]):
        self.model = config.get("model", "amazon.nova-micro-v1:0")
        self.temperature = config.get("temperature", 0.2)
        self.max_tokens = config.get("max_tokens", 500)
        self.client = boto3.client("bedrock-runtime")
    
    def generate_response(
        self,
        messages: Union[List[Dict[str, Any]], str],
        **kwargs
    ) -> str:
        """Generate response compatible with Mem0 expectations"""
        
        # Handle string input (convert to message format)
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        
        # Convert messages to Nova Converse API format
        formatted_messages = []
        system_prompts = []
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            # Extract system messages separately
            if role == "system":
                if isinstance(content, str):
                    system_prompts.append({"text": content})
                elif isinstance(content, list):
                    system_prompts.extend(content)
                continue
            
            # Format user/assistant messages
            if isinstance(content, str):
                formatted_messages.append({
                    "role": role,
                    "content": [{"text": content}]
                })
            elif isinstance(content, list):
                formatted_messages.append({
                    "role": role,
                    "content": content
                })
            else:
                formatted_messages.append(msg)
        
        # Prepare converse parameters
        converse_params = {
            "modelId": self.model,
            "messages": formatted_messages,
            "inferenceConfig": {
                "maxTokens": self.max_tokens,
                "temperature": self.temperature,
            }
        }
        
        # Add system prompts if present
        if system_prompts:
            converse_params["system"] = system_prompts
        
        # Call Nova using Converse API
        response = self.client.converse(**converse_params)
        
        # Extract text from response
        return response["output"]["message"]["content"][0]["text"]
