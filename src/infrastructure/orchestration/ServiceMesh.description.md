# ServiceMesh

**File**: `src\infrastructure\orchestration\ServiceMesh.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 83  
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

**Imports** (6):
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
