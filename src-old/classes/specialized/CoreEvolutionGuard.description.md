# CoreEvolutionGuard

**File**: `src\classes\specialized\CoreEvolutionGuard.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 100  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for CoreEvolutionGuard.

## Classes (1)

### `CoreEvolutionGuard`

Monitors and validates changes to the agent's core source code.
Prevents unintended mutations or malicious injections into the agent logic.

**Methods** (5):
- `__init__(self, workspace_path)`
- `hash_file(self, file_path)`
- `snapshot_core_logic(self, core_paths)`
- `validate_code_integrity(self, file_path)`
- `generate_hardening_report(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `hashlib`
- `os`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
