# SignalCore

**File**: `src\infrastructure\orchestration\SignalCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 39  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for SignalCore.

## Classes (1)

### `SignalCore`

Pure logic for the Signal Registry.
Handles event structure and history windowing.

**Methods** (2):
- `create_event(self, signal_name, data, sender)`
- `prune_history(self, history, limit)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `datetime.datetime`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
