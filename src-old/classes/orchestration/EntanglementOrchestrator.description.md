# EntanglementOrchestrator

**File**: `src\classes\orchestration\EntanglementOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 53  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for EntanglementOrchestrator.

## Classes (1)

### `EntanglementOrchestrator`

Manages instantaneous state synchronization across distributed agent nodes.
Ensures that high-priority state changes in one node are mirrored to all entangled peers.

**Methods** (5):
- `__init__(self, signal_bus)`
- `update_state(self, key, value, propagate)`
- `get_state(self, key)`
- `_handle_sync_signal(self, payload, sender)`
- `get_all_state(self)`

## Dependencies

**Imports** (8):
- `json`
- `logging`
- `src.classes.orchestration.SignalBusOrchestrator.SignalBusOrchestrator`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
