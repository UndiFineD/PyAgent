# exceptions

**File**: `src\core\base\exceptions.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 2 imports  
**Lines**: 40  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for exceptions.

## Classes (7)

### `PyAgentException`

**Inherits from**: Exception

Base exception for all PyAgent errors.

**Methods** (1):
- `__init__(self, message, error_code)`

### `InfrastructureError`

**Inherits from**: PyAgentException

Errors related to system infrastructure (I/O, Network).

### `LogicError`

**Inherits from**: PyAgentException

Errors related to agent logic or reasoning failure.

### `SecurityError`

**Inherits from**: PyAgentException

Errors related to unauthorized access or safety violations.

### `ModelError`

**Inherits from**: PyAgentException

Errors related to LLM connectivity or output parsing.

### `ConfigurationError`

**Inherits from**: PyAgentException

Errors in settings or manifest validation.

### `CycleInterrupt`

**Inherits from**: PyAgentException

Interruption of an agent cycle (e.g., quota exceeded).

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `typing.Optional`

---
*Auto-generated documentation*
