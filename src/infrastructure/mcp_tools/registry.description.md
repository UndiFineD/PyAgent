# registry

**File**: `src\infrastructure\mcp_tools\registry.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 12 imports  
**Lines**: 124  
**Complexity**: 9 (moderate)

## Overview

Registry for MCP tool servers and session management.

## Classes (2)

### `MCPServerRegistry`

Registry for MCP servers.

**Methods** (6):
- `__new__(cls)`
- `servers(self)`
- `register(self, server)`
- `unregister(self, name)`
- `get(self, name)`
- `get_all_tools(self)`

### `SessionManager`

Manage MCP sessions.

**Methods** (3):
- `__init__(self, registry)`
- `get_session(self, session_id)`
- `active_sessions(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `asyncio`
- `base.MCPToolServer`
- `logging`
- `models.MCPSession`
- `models.ToolCall`
- `models.ToolResult`
- `models.ToolSchema`
- `models.ToolStatus`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
