# bridge

**File**: `src\tools\mcp\bridge.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 22 imports  
**Lines**: 619  
**Complexity**: 14 (moderate)

## Overview

PyAgent MCP Server Ecosystem Integration.

Based on awesome-mcp-servers repository with 500+ MCP servers.
Implements standardized protocol abstraction for 10x tool expansion.

## Classes (8)

### `MCPServerType`

**Inherits from**: Enum

Types of MCP servers.

### `MCPCategory`

**Inherits from**: Enum

MCP server categories.

### `MCPServerConfig`

Configuration for an MCP server.

### `MCPTool`

Represents an MCP tool.

### `MCPServerRegistry`

Registry of available MCP servers.

Manages discovery, configuration, and lifecycle of MCP servers.

**Methods** (8):
- `__init__(self, registry_path)`
- `_load_registry(self)`
- `_create_default_registry(self)`
- `_save_registry(self)`
- `register_server(self, config)`
- `unregister_server(self, name)`
- `get_servers_by_category(self, category)`
- `get_servers_by_capability(self, capability)`

### `MCPServerInstance`

Instance of a running MCP server.

Manages the lifecycle of an MCP server process.

**Methods** (1):
- `__init__(self, config)`

### `MCPBridge`

MCP Protocol Bridge.

Provides standardized interface for external services through MCP servers.

**Methods** (4):
- `__init__(self, registry)`
- `get_available_tools(self)`
- `get_servers_by_category(self, category)`
- `get_servers_by_capability(self, capability)`

### `MCPToolOrchestrator`

Intelligent tool selection and orchestration.

Uses AI to select the best MCP tools for a given task.

**Methods** (1):
- `__init__(self, mcp_bridge, inference_engine)`

## Dependencies

**Imports** (22):
- `__future__.annotations`
- `aiohttp`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `logging`
- `pathlib.Path`
- `requests`
- `src.core.base.models.communication_models.CascadeContext`
- `subprocess`
- `sys`
- `time`
- `typing.Any`
- ... and 7 more

---
*Auto-generated documentation*
