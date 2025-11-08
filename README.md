# AWS Strands Agents with MCP Integration

Memory-powered AI agent for creating and iterating on AWS architecture diagrams using Model Context Protocol (MCP).

## Features

- 🏗️ **AWS Diagram Generation**: Create professional AWS diagrams using natural language
- 🧠 **Memory Integration**: Remembers previous diagrams and conversations
- 🔄 **Iterative Design**: Modify diagrams based on previous versions
- 🎨 **MCP Protocol**: Integrates AWS Diagram MCP Server
- 💬 **Conversational UI**: Streamlit-based chat interface

## Quick Start

See [MCP_SETUP.md](strands-agents/MCP_SETUP.md) for detailed setup instructions.

```bash
cd strands-agents
pip install -r requirements.txt
python api.py  # Start backend
streamlit run streamlit_app.py  # Start UI
```

## Documentation

- [MCP Setup Guide](strands-agents/MCP_SETUP.md)
- [Memory Features](strands-agents/MEMORY_FEATURES.md)
- [Cognito Setup](strands-agents/COGNITO_SETUP.md)