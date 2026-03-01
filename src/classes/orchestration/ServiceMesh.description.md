# ServiceMesh

**File**: `src\classes\orchestration\ServiceMesh.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 63  
**Complexity**: 5 (moderate)

## Overview

Service Mesh for synchronizing tools and capabilities across distributed fleet nodes.

## Classes (1)

### `ServiceMesh`

Manages cross-node tool discovery and capability synchronization.

**Methods** (5):
- `__init__(self, fleet_manager)`
- `_on_tool_registered(self, payload)`
- `_broadcast_capability(self, tool_name)`
- `sync_with_remote(self, node_url)`
- `get_mesh_status(self)`

## Dependencies

**Imports** (7):
- `json`
- `logging`
- `src.classes.orchestration.SignalRegistry.SignalRegistry`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
