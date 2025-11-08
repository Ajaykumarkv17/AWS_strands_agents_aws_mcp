# MCP Tools Debugging Guide

## Issue
`'MCPClient' object has no attribute 'tools'`

## Root Cause
The Strands MCPClient may use a different API than expected. Need to check actual implementation.

## Debug Steps

### 1. Test MCP Tools Loading
```bash
python test_mcp_tools.py
```

### 2. Check Strands MCP Documentation
The MCPClient from `strands.tools.mcp` might use:
- `get_tools()` method instead of `.tools` property
- Different initialization pattern
- Async context manager

### 3. Alternative Approaches

#### Option A: Use MCPClient as ToolProvider (Experimental)
```python
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

# MCPClient implements ToolProvider interface
mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["awslabs.aws-diagram-mcp-server@latest"]
        )
    )
)

# Pass directly to Agent
agent = Agent(
    tools=mcp_client,  # Pass MCPClient directly
    model="us.amazon.nova-premier-v1:0"
)
```

#### Option B: Manual Context Management
```python
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

# Use with statement
with MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["awslabs.aws-diagram-mcp-server@latest"]
        )
    )
) as mcp:
    agent = Agent(
        tools=[...other_tools, mcp],
        model="us.amazon.nova-premier-v1:0"
    )
    result = agent("Create diagram...")
```

#### Option C: Get Tools List
```python
# If MCPClient has get_tools() method
tools_list = mcp_client.get_tools()

# Or check for list_tools()
tools_list = mcp_client.list_tools()
```

## Next Steps

1. Run `test_mcp_tools.py` to see actual error
2. Check Strands documentation: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/mcp-tools/
3. Try alternative approaches above
4. Update `mcp_diagram_client.py` based on findings
