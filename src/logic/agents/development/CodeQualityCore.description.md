# CodeQualityCore

**File**: `src\logic\agents\development\CodeQualityCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 67  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for CodeQualityCore.

## Classes (1)

### `CodeQualityCore`

Pure logic for code quality analysis.
Decoupled from file I/O and subprocesses.

**Methods** (4):
- `calculate_score(issues_count)`
- `check_python_source_quality(source)`
- `analyze_rust_source(source)`
- `analyze_js_source(source)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
