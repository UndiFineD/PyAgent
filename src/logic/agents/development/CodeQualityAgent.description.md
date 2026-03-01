# CodeQualityAgent

**File**: `src\logic\agents\development\CodeQualityAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 111  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for CodeQualityAgent.

## Classes (1)

### `CodeQualityAgent`

**Inherits from**: BaseAgent

Automated Code Quality Guard: Performs linting, formatting checks, 
and complexity analysis for Python, Rust, and JavaScript.

**Methods** (6):
- `__init__(self, workspace_path)`
- `analyze_file_quality(self, file_path)`
- `_check_python_quality(self, path)`
- `_check_rust_quality(self, path)`
- `_check_js_quality(self, path)`
- `get_aggregate_score(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `os`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.version.VERSION`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
