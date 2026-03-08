# SignalRegistry

**File**: `src\classes\orchestration\SignalRegistry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 50  
**Complexity**: 4 (simple)

## Overview

A simple event-driven signal registry for inter-agent communication.

## Classes (1)

### `SignalRegistry`

Central hub for publishing and subscribing to agent signals.
Shell for SignalCore.

**Methods** (4):
- `__new__(cls)`
- `subscribe(self, signal_name, callback)`
- `emit(self, signal_name, data, sender)`
- `get_history(self, limit)`

## Dependencies

**Imports** (8):
- `SignalCore.SignalCore`
- `datetime.datetime`
- `logging`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
