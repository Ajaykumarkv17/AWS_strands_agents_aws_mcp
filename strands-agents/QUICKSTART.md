# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install UV for MCP server
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install GraphViz
# Windows: Download from https://graphviz.org/download/
# macOS: brew install graphviz
# Linux: sudo apt-get install graphviz
```

## Run with Docker

```bash
docker-compose up
```

Access:
- API: http://localhost:8000
- UI: http://localhost:8501

## Run Locally

```bash
# Terminal 1: Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Terminal 2: Start API
python api.py

# Terminal 3: Start UI
streamlit run streamlit_app.py
```

## Example Usage

1. **Create diagram**: "Create a serverless web app with S3, Lambda, API Gateway"
2. **Iterate**: "Add DynamoDB and CloudWatch to the previous diagram"
3. **New diagram**: "Create a microservices architecture with ECS and RDS"

The agent remembers previous diagrams and builds upon them!
