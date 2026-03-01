# SignalRegistry

**File**: `src\infrastructure\orchestration\SignalRegistry.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 103  
**Complexity**: 5 (moderate)

## Overview

A simple event-driven signal registry for inter-agent communication.

## Classes (1)

### `SignalRegistry`

Central hub for publishing and subscribing to agent signals.
Phase 279: Refactored emit to be async with history pruning.

**Methods** (5):
- `__new__(cls)`
- `_on_capability_registration(self, event)`
- `get_agent_by_capability(self, capability)`
- `subscribe(self, signal_name, callback)`
- `get_history(self, limit)`

## Dependencies

**Imports** (11):
- `SignalCore.SignalCore`
- `__future__.annotations`
- `asyncio`
- `collections.abc.Callable`
- `collections.abc.Coroutine`
- `logging`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
