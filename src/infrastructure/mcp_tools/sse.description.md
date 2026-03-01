# sse

**File**: `src\infrastructure\mcp_tools\sse.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 16 imports  
**Lines**: 196  
**Complexity**: 2 (simple)

## Overview

SSE-based MCP tool server implementation.

## Classes (2)

### `SSEMCPServer`

**Inherits from**: MCPToolServer

MCP server using Server-Sent Events.

**Methods** (1):
- `__init__(self, config)`

### `MockSSEClient`

Mock SSE client for testing.

**Methods** (1):
- `__init__(self, url)`

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `aiohttp`
- `asyncio`
- `base.MCPToolServer`
- `logging`
- `models.MCPServerConfig`
- `models.MCPSession`
- `models.SessionState`
- `models.ToolCall`
- `models.ToolResult`
- `models.ToolSchema`
- `models.ToolStatus`
- `time`
- `typing.Any`
- `typing.List`
- ... and 1 more

---
*Auto-generated documentation*
