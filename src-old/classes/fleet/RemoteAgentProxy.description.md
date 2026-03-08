# RemoteAgentProxy

**File**: `src\classes\fleet\RemoteAgentProxy.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 135  
**Complexity**: 7 (moderate)

## Overview

Proxy for agents running on remote nodes.
Allows FleetManager to transparently call tools on other machines.

## Classes (1)

### `RemoteAgentProxy`

**Inherits from**: BaseAgent

Encapsulates a remote agent accessible via HTTP/JSON-RPC.

Resilience (Phase 108): Implements a 15-minute TTL status cache for remote nodes.
Intelligence (Phase 108): Records remote interactions to local shards.

**Methods** (7):
- `__init__(self, file_path, node_url, agent_name)`
- `_is_node_working(self)`
- `_update_node_status(self, is_up)`
- `call_remote_tool(self, tool_name)`
- `call_remote_tool_binary(self, tool_name, compress)`
- `_record_interaction(self, tool_name, payload, response)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `logging`
- `os`
- `requests`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.ConnectivityManager.ConnectivityManager`
- `src.core.base.connectivity.BinaryTransport`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
