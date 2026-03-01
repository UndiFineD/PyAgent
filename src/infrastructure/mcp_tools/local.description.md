# local

**File**: `src\infrastructure\mcp_tools\local.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 16 imports  
**Lines**: 98  
**Complexity**: 2 (simple)

## Overview

Local (in-process) MCP tool server implementation.

## Classes (1)

### `LocalMCPServer`

**Inherits from**: MCPToolServer

In-process MCP server for local tool execution.

**Methods** (2):
- `__init__(self, config)`
- `register_tool(self, name, handler, description, parameters)`

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `asyncio`
- `base.MCPToolServer`
- `models.MCPServerConfig`
- `models.MCPSession`
- `models.SessionState`
- `models.ToolCall`
- `models.ToolResult`
- `models.ToolSchema`
- `models.ToolStatus`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- ... and 1 more

---
*Auto-generated documentation*
