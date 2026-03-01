# SignalBusOrchestrator

**File**: `src\infrastructure\orchestration\SignalBusOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 70  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for SignalBusOrchestrator.

## Classes (1)

### `SignalBusOrchestrator`

High-speed signal bus for low-latency agent-to-agent communication.
Uses an internal message queue and a pub-sub pattern to bypass slow JSON/HTTP overhead.

**Methods** (5):
- `__init__(self)`
- `subscribe(self, signal_type, callback)`
- `publish(self, signal_type, payload, sender)`
- `_process_bus(self)`
- `shutdown(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `collections.abc.Callable`
- `logging`
- `queue`
- `src.core.base.version.VERSION`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
