# AWS Diagram Agent with MCP Integration

A memory-powered AI agent that creates and iterates on AWS architecture diagrams using Model Context Protocol (MCP) and Strands Agents framework.

## Features

- 🏗️ **AWS Diagram Generation**: Create professional AWS architecture diagrams using natural language
- 🧠 **Memory-Powered**: Remembers previous diagrams and user preferences
- 🔄 **Iterative Design**: Modify and improve diagrams based on previous versions
- 🎨 **MCP Integration**: Uses AWS Diagram MCP Server for diagram generation
- 💬 **Conversational Interface**: Natural language interaction via Streamlit UI

## Architecture

```
User → Streamlit UI → FastAPI Backend → Strands Agent → MCP Server
                                              ↓
                                         Mem0 Memory
```

## Prerequisites

1. **Python 3.10+**
2. **UV Package Manager**: Install from [Astral](https://docs.astral.sh/uv/getting-started/installation/)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **GraphViz**: Required for diagram rendering
   - **Windows**: Download from [graphviz.org](https://graphviz.org/download/)
   - **macOS**: `brew install graphviz`
   - **Linux**: `sudo apt-get install graphviz`

4. **AWS Credentials**: Configure AWS CLI
   ```bash
   aws configure
   ```

## Installation

1. **Clone and navigate to project**:
   ```bash
   cd strands-agents
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install AWS Diagram MCP Server**:
   ```bash
   uvx awslabs.aws-diagram-mcp-server@latest
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials
   ```

## Configuration

### Environment Variables (.env)

```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Qdrant (for memory)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_key

# Optional: MCP Server settings
FASTMCP_LOG_LEVEL=ERROR
```

### MCP Server Configuration

The AWS Diagram MCP Server is automatically initialized via the `mcp_diagram_client.py` module:

```python
# Connects to: uvx awslabs.aws-diagram-mcp-server@latest
```

## Usage

### 1. Start Qdrant (Memory Store)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 2. Start FastAPI Backend

```bash
python api.py
```

The API will be available at `http://localhost:8000`

### 3. Start Streamlit Frontend

```bash
streamlit run streamlit_app.py
```

The UI will open at `http://localhost:8501`

### 4. Interact with the Agent

**Example Conversations:**

1. **Create Initial Diagram**:
   ```
   User: Create a diagram for a serverless web application with S3, Lambda, and API Gateway
   Agent: [Generates diagram and saves to memory]
   ```

2. **Iterate on Diagram**:
   ```
   User: Add a DynamoDB database and CloudFront CDN to the previous diagram
   Agent: [Retrieves previous diagram from memory, enhances it]
   ```

3. **Complex Architecture**:
   ```
   User: Create a microservices architecture with ECS, ALB, RDS, and ElastiCache
   Agent: [Generates comprehensive diagram]
   ```

## How It Works

### Memory-Powered Iteration

1. **First Request**: User asks for a diagram
   - Agent generates diagram using MCP tools
   - Saves diagram context to Mem0 memory

2. **Follow-up Request**: User asks to modify diagram
   - Agent searches memory for previous diagram context
   - Retrieves previous diagram code/structure
   - Generates enhanced version with modifications
   - Updates memory with new diagram

### MCP Integration Flow

```python
# 1. Initialize MCP Client
mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["awslabs.aws-diagram-mcp-server@latest"]
        )
    )
)

# 2. Get MCP Tools
tools = mcp_client.tools

# 3. Create Agent with MCP Tools
agent = Agent(
    tools=[...standard_tools, *mcp_tools],
    model="us.amazon.nova-premier-v1:0"
)

# 4. Agent uses MCP tools to generate diagrams
result = agent("Create AWS diagram...")
```

## API Endpoints

### POST /chat
Chat with the memory-enabled agent

**Request**:
```json
{
  "messages": [
    {"role": "user", "content": "Create a diagram..."}
  ],
  "user_id": "user123"
}
```

**Response**:
```json
{
  "message": "I've created the diagram...",
  "success": true,
  "user_id": "user123",
  "diagram_path": "/diagrams/aws_architecture.png"
}
```

### POST /memory
Retrieve user memories

**Request**:
```json
{
  "user_id": "user123",
  "query": "diagram"
}
```

### DELETE /memory/{user_id}
Clear user memories

## Project Structure

```
strands-agents/
├── api.py                    # FastAPI backend
├── memory_agent.py           # Agent with memory integration
├── memory_config.py          # Memory configuration
├── mcp_diagram_client.py     # MCP client for diagrams
├── streamlit_app.py          # Streamlit UI
├── requirements.txt          # Dependencies
├── diagrams/                 # Generated diagrams
└── .env                      # Environment variables
```

## Troubleshooting

### MCP Server Not Starting

```bash
# Test MCP server manually
uvx awslabs.aws-diagram-mcp-server@latest

# Check UV installation
uv --version
```

### GraphViz Not Found

```bash
# Verify GraphViz installation
dot -V

# Add to PATH (Windows)
setx PATH "%PATH%;C:\Program Files\Graphviz\bin"
```

### Memory Not Persisting

```bash
# Check Qdrant is running
curl http://localhost:6333/health

# Restart Qdrant
docker restart <qdrant_container_id>
```

## Advanced Features

### Custom Diagram Styles

The agent can generate various diagram types:
- AWS Architecture Diagrams
- Sequence Diagrams
- Flow Diagrams
- Class Diagrams

### Memory Search

The agent automatically searches memory for:
- Previous diagram requests
- User preferences
- Architecture patterns
- Component relationships

## References

- [Strands Agents Documentation](https://strandsagents.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [AWS Diagram MCP Server](https://awslabs.github.io/mcp/servers/aws-diagram-mcp-server/)
- [Python Diagrams Package](https://diagrams.mingrammer.com/)

## License

Apache 2.0
