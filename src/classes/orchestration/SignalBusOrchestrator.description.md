# SignalBusOrchestrator

**File**: `src\classes\orchestration\SignalBusOrchestrator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 53  
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
- `json`
- `logging`
- `queue`
- `threading`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
