# modules

**File**: `src\core\base\modules.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 41  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for modules.

## Classes (1)

### `BaseModule`

**Inherits from**: ABC

Base class for all core modules in the swarm.
Standardizes the lifecycle of global specialized logic.

**Methods** (4):
- `__init__(self, config)`
- `initialize(self)`
- `execute(self)`
- `shutdown(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
