# MCPToolServer

**File**: `src\infrastructure\mcp_tools\MCPToolServer.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 14 imports  
**Lines**: 75  
**Complexity**: 4 (simple)

## Overview

Facade for MCP Tool Server Integration.
Delegates to modularized sub-packages in src/infrastructure/mcp_tools/.

## Functions (4)

### `adapt_tool_schema(schema)`

Legacy helper for adaptation.

### `discover_mcp_servers()`

Legacy helper for server discovery.

### `adapt_tool_schema(schema)`

Legacy helper for adaptation.

### `discover_mcp_servers()`

Legacy helper for server discovery.

## Dependencies

**Imports** (14):
- `adapter.SchemaAdapter`
- `base.MCPToolServer`
- `local.LocalToolServer`
- `models.MCPServerConfig`
- `models.MCPServerType`
- `models.MCPSession`
- `models.SessionState`
- `models.ToolCall`
- `models.ToolResult`
- `models.ToolSchema`
- `models.ToolStatus`
- `registry.MCPServerRegistry`
- `registry.SessionManager`
- `sse.SSEToolServer`

---
*Auto-generated documentation*
