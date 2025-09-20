# Strands Agent with AWS Integration

A comprehensive example of building AI agents using the AWS Strands framework with integrated AWS services.

## Features

- 🤖 **AI Agent**: Built with Strands framework using Claude 4 Sonnet
- ☁️ **AWS Integration**: Direct integration with AWS services (S3, STS)
- 🛠️ **Custom Tools**: Calculator, time, letter counter, AWS info tools
- 🔧 **Easy Setup**: Automated setup and configuration checking
- 📊 **Testing**: Comprehensive testing suite included

## Prerequisites

- Python 3.10+
- AWS Account with Bedrock access
- AWS CLI configured or environment variables set

## Quick Start

### 1. Setup Environment

```powershell
# Navigate to project directory
cd strands-agents

# Run setup script to check configuration
python setup.py
```

### 2. Configure AWS Credentials

If setup script indicates missing credentials:

```powershell
# Install AWS CLI (if not already installed)
pip install awscli

# Configure credentials
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key  
- Default region (e.g., us-east-1)
- Output format (json)

### 3. Enable Bedrock Access

1. Go to [AWS Console > Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
2. Navigate to "Model access" in the left sidebar
3. Click "Request model access"
4. Enable "Claude 3.5 Sonnet" model
5. Submit request (usually approved instantly)

### 4. Run the Agent

```powershell
# Run the main agent
python main.py
```

## Project Structure

```
strands-agents/
├── main.py              # Main agent implementation
├── setup.py             # Setup and configuration checker
├── pyproject.toml       # Project dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Available Tools

The agent comes with these built-in tools:

- **Calculator**: Perform mathematical calculations
- **Current Time**: Get current date and time
- **Letter Counter**: Count letter occurrences in words
- **AWS Account Info**: Get AWS account ID and region
- **List S3 Buckets**: List S3 buckets in your account
- **System Info**: Get system and Python information

## Usage Examples

### Automated Testing
The agent runs through several test queries automatically:

```
Test 1: What is the current time?
Test 2: Calculate 1234 * 5678
Test 3: Count the letter 'a' in the word 'banana'
Test 4: What is my AWS account information?
Test 5: List my S3 buckets
Test 6: Show me system information
```

### Interactive Mode
After testing, you can interact with the agent directly:

```
🤔 Your question: What AWS services can you help me with?
🤖 Agent response: I can help you with S3 bucket management, account information, and more...
```

## Troubleshooting

### Common Issues

1. **AWS Credentials Not Found**
   ```
   Solution: Run 'aws configure' or set environment variables
   ```

2. **Bedrock Access Denied**
   ```
   Solution: Enable Bedrock access in AWS Console
   ```

3. **Model Access Denied**
   ```
   Solution: Request access to Claude models in Bedrock console
   ```

4. **Region Issues**
   ```
   Solution: Ensure your AWS region supports Bedrock (us-east-1, us-west-2, etc.)
   ```

### Debug Mode

Enable debug logging by setting environment variable:
```powershell
$env:LOG_LEVEL="DEBUG"
python main.py
```

## Extending the Agent

### Adding Custom Tools

```python
from strands import tool

@tool
def my_custom_tool(input_param: str) -> str:
    """
    Description of what your tool does.
    
    Args:
        input_param (str): Description of parameter
        
    Returns:
        str: Description of return value
    """
    # Your tool logic here
    return f"Processed: {input_param}"

# Add to agent tools list
tools.append(my_custom_tool)
```

### Using Different Models

```python
# Use different Bedrock model
agent = Agent(
    tools=tools,
    model="anthropic.claude-3-haiku-20240307-v1:0"  # Faster, cheaper model
)

# Use OpenAI model (requires API key)
from strands.models import OpenAIModel
agent = Agent(
    tools=tools,
    model=OpenAIModel(model_id="gpt-4")
)
```

## Dependencies

- `strands-agents`: Core Strands framework
- `strands-agents-tools`: Community tools package
- `boto3`: AWS SDK for Python

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- [Strands Agents GitHub](https://github.com/strands-agents/sdk-python)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Strands Documentation](https://strandsagents.com/)
