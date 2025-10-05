#!/usr/bin/env python3
"""
Setup script for Strands Agent project
Helps configure AWS credentials and test the environment
"""

import os
import sys
import subprocess
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

def check_python_version():
    """Check if Python version is 3.10+"""
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10+ is required. Current version:", sys.version)
        return False
    print("OK: Python version:", sys.version.split()[0])
    return True

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print("OK: AWS credentials configured")
        print(f"   Account ID: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        return True
    except NoCredentialsError:
        print("ERROR: AWS credentials not found")
        print("   Please run 'aws configure' or set environment variables")
        return False
    except Exception as e:
        print(f"ERROR: AWS credential error: {str(e)}")
        return False

def check_bedrock_access():
    """Check if Bedrock service is accessible"""
    try:
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        models = bedrock.list_foundation_models()
        print("OK: Amazon Bedrock accessible")
        print(f"   Available models: {len(models.get('modelSummaries', []))}")
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            print("ERROR: No access to Amazon Bedrock")
            print("   Please enable Bedrock access in AWS Console")
        else:
            print(f"ERROR: Bedrock error: {str(e)}")
        return False
    except Exception as e:
        print(f"ERROR: Bedrock connection error: {str(e)}")
        return False

def check_model_access():
    """Check if Claude model is accessible"""
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        # Try to invoke a simple request to check model access
        response = bedrock.converse(
            modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[{"role": "user", "content": [{"text": "Hello"}]}],
            inferenceConfig={"maxTokens": 10}
        )
        print("OK: Claude model accessible")
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            print("ERROR: No access to Claude model")
            print("   Please enable Claude model access in Bedrock console")
        else:
            print(f"ERROR: Model access error: {str(e)}")
        return False
    except Exception as e:
        print(f"ERROR: Model test error: {str(e)}")
        return False

def install_dependencies():
    """Install required dependencies"""
    try:
        print("Installing dependencies...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("OK: Dependencies installed successfully")
            return True
        else:
            print(f"ERROR: Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR: Installation error: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("Strands Agent Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check AWS setup
    if not check_aws_credentials():
        print("\nTo configure AWS credentials:")
        print("   1. Install AWS CLI: pip install awscli")
        print("   2. Run: aws configure")
        print("   3. Enter your Access Key ID and Secret Access Key")
        return False
    
    # Check Bedrock access
    if not check_bedrock_access():
        print("\nTo enable Bedrock access:")
        print("   1. Go to AWS Console > Amazon Bedrock")
        print("   2. Navigate to 'Model access' in the left sidebar")
        print("   3. Request access to Claude models")
        return False
    
    # Check model access
    if not check_model_access():
        print("\nTo enable Claude model access:")
        print("   1. Go to AWS Console > Amazon Bedrock > Model access")
        print("   2. Enable 'Claude 3.5 Sonnet' model")
        print("   3. Wait for approval (usually instant)")
        return False
    
    print("\nSetup completed successfully!")
    print("You can now run: python main.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
