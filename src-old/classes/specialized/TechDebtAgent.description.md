# TechDebtAgent

**File**: `src\classes\specialized\TechDebtAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 95  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for TechDebtAgent.

## Classes (1)

### `TechDebtAgent`

**Inherits from**: BaseAgent

Analyzes the codebase for technical debt including high cyclomatic complexity,
missing docstrings, and large files.

**Methods** (3):
- `__init__(self, workspace_path)`
- `analyze_file(self, file_path)`
- `analyze_workspace(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `ast`
- `os`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
