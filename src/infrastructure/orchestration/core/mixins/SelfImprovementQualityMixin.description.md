# SelfImprovementQualityMixin

**File**: `src\infrastructure\orchestration\core\mixins\SelfImprovementQualityMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 139  
**Complexity**: 4 (simple)

## Overview

Quality and robustness analysis logic for SelfImprovementCore.

## Classes (1)

### `SelfImprovementQualityMixin`

Mixin for quality, complexity, and robustness analysis.

**Methods** (4):
- `_analyze_complexity(self, content, file_path_rel)`
- `_analyze_documentation(self, content, file_path_rel)`
- `_analyze_typing(self, content, file_path_rel)`
- `_analyze_robustness_and_perf(self, content, file_path_rel)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `ast`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
