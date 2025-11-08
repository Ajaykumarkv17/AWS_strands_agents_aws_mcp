#!/usr/bin/env python3
"""
Enhanced FastAPI backend for Memory-Enabled Strands Agent
Exposes memory-aware agent functionality as REST API endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import os
import re
from pathlib import Path
from contextlib import asynccontextmanager
from memory_agent import create_memory_agent
from memory_config import get_memory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Request/Response models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    user_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    message: str
    success: bool
    user_id: str
    diagram_path: Optional[str] = None

class MemoryRequest(BaseModel):
    user_id: Optional[str] = "default"
    query: Optional[str] = None

class MemoryResponse(BaseModel):
    memories: List[Dict[str, Any]]
    success: bool

# Initialize memory and agents
memory = get_memory()
agents = {}  # Store agents per user

# Create diagrams directory
DIAGRAMS_DIR = Path("diagrams")
DIAGRAMS_DIR.mkdir(exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler"""
    logger.info("Memory-enabled Strands agent API initialized successfully")
    yield
    logger.info("Shutting down API")

app = FastAPI(title="Memory-Enabled Strands Agent API", version="2.0.0", lifespan=lifespan)

# Mount static files for diagrams
app.mount("/diagrams", StaticFiles(directory=str(DIAGRAMS_DIR)), name="diagrams")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_or_create_agent(user_id: str):
    """Get existing agent for user or create new one"""
    if user_id not in agents:
        agents[user_id] = create_memory_agent(user_id)
        logger.info(f"Created new agent for user: {user_id}")
    return agents[user_id]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Strands Agent API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process chat messages with memory-enabled agent
    """
    try:
        user_id = request.user_id or "default"
        
        if not request.messages:
            raise HTTPException(status_code=400, detail="No messages provided")
        
        latest_message = request.messages[-1]
        if latest_message.role != "user":
            raise HTTPException(status_code=400, detail="Last message must be from user")
        
        agent = get_or_create_agent(user_id)
        
        # Check if this is a diagram-related request
        is_diagram_request = any(keyword in latest_message.content.lower() 
                                for keyword in ['diagram', 'architecture', 'draw', 'visualize'])
        
        # If diagram request, include previous diagram context from memory
        if is_diagram_request:
            prev_diagrams = memory.search("diagram architecture", user_id=user_id, limit=3)
            if prev_diagrams and isinstance(prev_diagrams, dict):
                prev_diagrams = prev_diagrams.get('results', [])
            if prev_diagrams:
                context = "\n".join([m['memory'] for m in prev_diagrams])
                enhanced_query = f"{latest_message.content}\n\nPrevious diagram context: {context}"
                result = agent(enhanced_query)
            else:
                result = agent(latest_message.content)
        else:
            result = agent(latest_message.content)
        
        if hasattr(result, 'text'):
            response = result.text
        elif hasattr(result, 'content'):
            response = result.content
        else:
            response = str(result)
        
        response = re.sub(r'<thinking>.*?</thinking>', '', response, flags=re.DOTALL).strip()
        
        # Check if response contains diagram path
        diagram_path = None
        diagram_match = re.search(r'([\w_-]+\.png)', response)
        if diagram_match:
            diagram_filename = diagram_match.group(1)
            if (DIAGRAMS_DIR / diagram_filename).exists():
                diagram_path = f"/diagrams/{diagram_filename}"
        
        return ChatResponse(message=response, success=True, user_id=user_id, diagram_path=diagram_path)
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream chat responses"""
    from fastapi.responses import StreamingResponse
    import asyncio
    
    async def generate():
        try:
            user_id = request.user_id or "default"
            latest_message = request.messages[-1]
            agent = get_or_create_agent(user_id)
            result = agent(latest_message.content)
            
            if hasattr(result, 'text'):
                response = result.text
            elif hasattr(result, 'content'):
                response = result.content
            else:
                response = str(result)
            
            import re
            response = re.sub(r'<thinking>.*?</thinking>', '', response, flags=re.DOTALL).strip()
            
            # Stream word by word
            for word in response.split():
                yield f"{word} "
                await asyncio.sleep(0.05)
        except Exception as e:
            yield f"Error: {str(e)}"
    
    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "memory_ready": True, "active_users": len(agents)}

@app.post("/memory", response_model=MemoryResponse)
async def get_memories(request: MemoryRequest):
    """
    Retrieve user memories
    """
    try:
        user_id = request.user_id or "default"
        
        if request.query:
            # Search specific memories
            result = memory.search(request.query, user_id=user_id, limit=10)
            # Handle dict response with 'results' key
            memories = result.get('results', []) if isinstance(result, dict) else result
        else:
            # Get all memories
            result = memory.get_all(user_id=user_id)
            memories = result.get('results', []) if isinstance(result, dict) else result
        
        return MemoryResponse(memories=memories or [], success=True)
        
    except Exception as e:
        logger.error(f"Error retrieving memories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/memory/{user_id}")
async def clear_memories(user_id: str):
    """
    Clear all memories for a user
    """
    try:
        # Clear memories
        result = memory.get_all(user_id=user_id)
        memories = result.get('results', []) if isinstance(result, dict) else result
        if memories:
            for mem in memories:
                memory.delete(mem['id'])
        
        # Remove agent instance
        if user_id in agents:
            del agents[user_id]
        
        return {"message": f"Cleared memories for user {user_id}", "success": True}
        
    except Exception as e:
        logger.error(f"Error clearing memories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)