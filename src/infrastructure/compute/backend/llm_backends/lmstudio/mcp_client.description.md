# mcp_client

**File**: `src\infrastructure\compute\backend\llm_backends\lmstudio\mcp_client.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 209  
**Complexity**: 6 (moderate)

## Overview

LM Studio MCP client and SDK session management.

## Classes (1)

### `MCPClient`

Manager for LM Studio SDK clients and sessions with Model Context Protocol support.

**Methods** (6):
- `__init__(self, base_url, api_token)`
- `get_sync_client(self)`
- `get_async_client(self)`
- `get_llm(self, client, model)`
- `get_embedding_model(self, client, model)`
- `close(self)`

## Dependencies

**Imports** (11):
- `inspect`
- `lmstudio`
- `logging`
- `typing.Any`
- `typing.Optional`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
