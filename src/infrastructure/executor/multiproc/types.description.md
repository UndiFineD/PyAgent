# types

**File**: `src\infrastructure\executor\multiproc\types.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 11 imports  
**Lines**: 58  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for types.

## Classes (5)

### `ExecutorBackend`

**Inherits from**: Enum

Executor backend types.

### `WorkerState`

**Inherits from**: Enum

Worker process states.

### `WorkerInfo`

Information about a worker process.

### `TaskMessage`

Message for task execution.

### `ResultMessage`

Message for task result.

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
