# ThoughtDebugger

**File**: `src\interface\cli\ThoughtDebugger.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 90  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for ThoughtDebugger.

## Classes (1)

### `ThoughtDebugger`

Interactive CLI tool for real-time inspection of agent reasoning (thoughts).
Subscribes to the 'thought_stream' signal and provides formatting and control.

**Methods** (5):
- `__init__(self, interactive)`
- `start(self)`
- `stop(self)`
- `_handle_thought(self, event)`
- `_show_menu(self, data)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `asyncio`
- `json`
- `logging`
- `src.core.base.version.VERSION`
- `src.infrastructure.orchestration.SignalRegistry.SignalRegistry`
- `sys`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
