# CodeQualityAgent

**File**: `src\classes\specialized\CodeQualityAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 66  
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

**Imports** (7):
- `json`
- `os`
- `src.classes.base_agent.BaseAgent`
- `subprocess`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
