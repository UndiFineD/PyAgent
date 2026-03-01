# FleetRoutingMixin

**File**: `src\infrastructure\fleet\mixins\FleetRoutingMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 49  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for FleetRoutingMixin.

## Classes (1)

### `FleetRoutingMixin`

Mixin for task routing and remote node registration in FleetManager.

**Methods** (2):
- `register_remote_node(self, node_url, agent_names, remote_version)`
- `route_task(self, task_type, task_data)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `src.core.base.Version.SDK_VERSION`
- `src.infrastructure.fleet.FleetManager.FleetManager`
- `src.infrastructure.fleet.RemoteAgentProxy.RemoteAgentProxy`
- `src.infrastructure.fleet.VersionGate.VersionGate`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
