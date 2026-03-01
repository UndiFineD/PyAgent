# safe_executor

**File**: `src\logic\agents\interpreter\safe_executor.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 13 imports  
**Lines**: 133  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for safe_executor.

## Classes (2)

### `ExecutionResult`

Class ExecutionResult implementation.

### `SafeLocalInterpreter`

Safely executes Python code within the agent's context.
Ported from 0xSojalSec-cai/cai/agents/meta/local_python_executor.py

**Methods** (4):
- `__init__(self, safe_globals)`
- `_get_safe_builtins(self)`
- `_setup_allowed_modules(self)`
- `_execute_sync(self, code)`

## Dependencies

**Imports** (13):
- `ast`
- `asyncio`
- `builtins`
- `dataclasses.dataclass`
- `io`
- `logging`
- `sys`
- `traceback`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
