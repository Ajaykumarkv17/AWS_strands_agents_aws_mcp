#!/usr/bin/env python3
"""
MCP Client for AWS Diagram Server Integration
"""

import logging
import sys
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

logger = logging.getLogger(__name__)

def get_diagram_mcp_client():
    """Get AWS Diagram MCP client as ToolProvider"""
    try:
        logger.info("Initializing AWS Diagram MCP client...")
        
        # Windows requires different command format to avoid SIGALRM issues
        if sys.platform == "win32":
            command = "uv"
            args = ["tool", "run", "--from", "awslabs.aws-diagram-mcp-server@latest", "awslabs.aws-diagram-mcp-server.exe"]
        else:
            command = "uvx"
            args = ["awslabs.aws-diagram-mcp-server@latest"]
        
        mcp_client = MCPClient(
            lambda: stdio_client(
                StdioServerParameters(
                    command=command,
                    args=args
                )
            ),
            startup_timeout=120
        )
        
        logger.info("AWS Diagram MCP client initialized successfully")
        return mcp_client
                
    except Exception as e:
        logger.error(f"Failed to initialize MCP client: {e}", exc_info=True)
        return None
