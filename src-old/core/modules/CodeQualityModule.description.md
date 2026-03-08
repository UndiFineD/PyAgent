# CodeQualityModule

**File**: `src\core\modules\CodeQualityModule.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 88  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for CodeQualityModule.

## Classes (1)

### `CodeQualityModule`

**Inherits from**: BaseModule

Consolidated core module for code quality analysis.
Migrated from CodeQualityCore.

**Methods** (7):
- `initialize(self)`
- `execute(self, source, language)`
- `calculate_score(self, issues_count)`
- `check_python_source_quality(self, source)`
- `analyze_rust_source(self, source)`
- `analyze_js_source(self, source)`
- `shutdown(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `re`
- `src.core.base.modules.BaseModule`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
