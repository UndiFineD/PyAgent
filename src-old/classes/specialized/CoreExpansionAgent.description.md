# CoreExpansionAgent

**File**: `src\classes\specialized\CoreExpansionAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 80  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for CoreExpansionAgent.

## Classes (1)

### `CoreExpansionAgent`

**Inherits from**: BaseAgent

Agent responsible for autonomous environment expansion.
Detects missing libraries and installs them into the active Python environment.

**Methods** (3):
- `__init__(self, file_path)`
- `install_missing_dependency(self, package_name)`
- `audit_environment(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `pkg_resources`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `subprocess`
- `sys`
- `typing.List`

---
*Auto-generated documentation*
