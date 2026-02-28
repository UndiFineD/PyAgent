# Splice: src/infrastructure/services/mcp/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- MCPServerType
- ToolStatus
- SessionState
- MCPServerConfig
- ToolSchema
- ToolCall
- ToolResult
- MCPSession

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
