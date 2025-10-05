# Memory-Enabled Strands Agent Features

## 🧠 Memory Integration with Mem0

### Core Memory Features

1. **Persistent Memory**: Remembers user information across sessions
2. **Personalized Responses**: Adapts responses based on user history
3. **Context Awareness**: Maintains conversation context and continuity
4. **User Preferences**: Learns and stores user likes, dislikes, and preferences
5. **Semantic Search**: Finds relevant memories using intelligent search

### Memory Tools Available

#### `search_memory(query, user_id)`
- Searches through user's stored memories
- Uses semantic similarity for intelligent retrieval
- Returns relevant past conversations and information

#### `save_memory(content, user_id)`
- Stores important information to user's memory
- Automatically extracts key details from conversations
- Maintains persistent storage across sessions

#### `get_user_preferences(user_id)`
- Retrieves user preferences and personal information
- Focuses on likes, dislikes, favorites, and personal details
- Enables personalized recommendations

#### `personalized_greeting(user_id)`
- Generates personalized greetings based on memory
- References user's name and interests when available
- Creates continuity in conversations

## 🛠️ Enhanced Agent Tools

### AWS Integration Tools
- **aws_account_info()**: Get AWS account details
- **list_s3_buckets()**: List S3 buckets in account

### Utility Tools
- **calculator**: Perform mathematical calculations
- **current_time**: Get current date and time
- **letter_counter**: Count letter occurrences in words
- **system_info**: Get system and environment information

## 🌐 Web Interface Features

### Streamlit Frontend
- **Beautiful UI**: Modern, responsive design
- **Real-time Chat**: Interactive conversation interface
- **Memory Visualization**: View and search stored memories
- **User Management**: Switch between different user profiles
- **Memory Management**: Clear or search specific memories

### API Endpoints
- **POST /chat**: Send messages to memory-enabled agent
- **POST /memory**: Retrieve user memories with optional search
- **DELETE /memory/{user_id}**: Clear all memories for a user
- **GET /health**: Check system status and active users

## 🚀 Deployment Options

### Local Development
```bash
# Run FastAPI backend
uvicorn api:app --reload --port 8000

# Run Streamlit frontend
streamlit run streamlit_app.py --server.port 8501
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```



## 💡 Usage Examples

### Basic Memory Interaction
```
User: "Hi, my name is Alice and I love machine learning"
Agent: "Nice to meet you, Alice! I'll remember that you love machine learning. How can I help you today?"

User: "What do you remember about me?"
Agent: "I remember that your name is Alice and you love machine learning. Is there anything specific about ML you'd like to discuss?"
```

### Personalized Responses
```
User: "Recommend some tools for my projects"
Agent: "Based on your interest in machine learning, I'd recommend tools like TensorFlow, PyTorch, or scikit-learn. Would you like specific recommendations for any particular type of ML project?"
```

### Memory Search
```
User: "What did we discuss about Python last week?"
Agent: [Searches memory for Python-related conversations and provides relevant context]
```

## 🔧 Configuration

### Environment Variables
```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

### Memory Configuration
- **Storage**: Local SQLite database (default)
- **Search**: Semantic similarity using embeddings
- **Persistence**: Automatic across sessions
- **User Isolation**: Separate memory spaces per user

## 🛡️ Security Features

- **User Isolation**: Each user has separate memory space
- **AWS Integration**: Secure credential management
- **API Security**: Input validation and error handling
- **Memory Privacy**: User-specific data access only

## 📊 Performance Features

- **Efficient Search**: Fast semantic memory retrieval
- **Caching**: Per-user agent instances for performance
- **Scalability**: Supports multiple concurrent users
- **Resource Management**: Automatic cleanup and optimization