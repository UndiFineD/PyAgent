# InterfaceSyncCore

**File**: `src\interface\core\InterfaceSyncCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 50  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for InterfaceSyncCore.

## Classes (1)

### `InterfaceSyncCore`

InterfaceSyncCore handles synchronization logic between CLI, GUI, and Web.
It manages the central state and 'Theme Engine' propagation.

**Methods** (4):
- `__init__(self)`
- `get_theme_payload(self, theme_name)`
- `broadcast_action(self, action_type, payload)`
- `resolve_topology_state(self, agents, connections)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
