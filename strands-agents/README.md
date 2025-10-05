# Memory-Enabled AI Agent with Amazon Bedrock

A production-ready AI agent with persistent memory using Amazon Nova and Bedrock services.

## Features

- 🧠 **Persistent Memory**: Remembers user preferences across sessions
- ☁️ **AWS Native**: Built with Amazon Nova Premier, Nova Micro, and Titan Embeddings
- 🔒 **User Isolation**: Per-user memory with unique IDs

## Architecture

```
User → Streamlit UI → FastAPI → Strands Agent (Nova Premier)
                                      ↓
                                  Mem0 Library
                                      ↓
                        ┌─────────────┴─────────────┐
                        ↓                           ↓
                Nova Micro (Facts)      Titan Embed (Vectors)
                        ↓                           ↓
                        └─────────────┬─────────────┘
                                      ↓
                              Qdrant Vector DB
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set AWS credentials
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1

# Run
python run.py
```

## AWS Services Used

- **Amazon Nova Premier**: Main conversation model
- **Amazon Nova Micro**: Memory fact extraction
- **Amazon Titan Embeddings v2**: Vector generation (1024-dim)
- **Amazon Bedrock**: Model hosting


## License

MIT
