#!/usr/bin/env python3
"""
Check available Bedrock models
"""

import boto3
import json

def check_available_models():
    """Check what Bedrock models are available"""
    try:
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        response = bedrock.list_foundation_models()
        
        anthropic_models = []
        for model in response.get('modelSummaries', []):
            if 'anthropic' in model['modelId'].lower():
                anthropic_models.append({
                    'modelId': model['modelId'],
                    'modelName': model['modelName'],
                    'providerName': model['providerName']
                })
        
        print("Available Anthropic Models:")
        print("=" * 50)
        for model in anthropic_models:
            print(f"ID: {model['modelId']}")
            print(f"Name: {model['modelName']}")
            print(f"Provider: {model['providerName']}")
            print("-" * 30)
            
        return anthropic_models
        
    except Exception as e:
        print(f"Error checking models: {str(e)}")
        return []

def test_model_access(model_id):
    """Test if we can access a specific model"""
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        response = bedrock.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": "Hello"}]}],
            inferenceConfig={"maxTokens": 10}
        )
        print(f"SUCCESS: Can access model {model_id}")
        return True
    except Exception as e:
        print(f"FAILED: Cannot access model {model_id} - {str(e)}")
        return False

if __name__ == "__main__":
    models = check_available_models()
    
    print("\nTesting model access:")
    print("=" * 50)
    
    # Test common models
    test_models = [
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "us.anthropic.claude-sonnet-4-20250514-v1:0"
    ]
    
    accessible_models = []
    for model_id in test_models:
        if test_model_access(model_id):
            accessible_models.append(model_id)
    
    print(f"\nAccessible models: {accessible_models}")
