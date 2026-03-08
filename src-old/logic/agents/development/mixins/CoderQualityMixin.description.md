# CoderQualityMixin

**File**: `src\logic\agents\development\mixins\CoderQualityMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 122  
**Complexity**: 2 (simple)

## Overview

Quality scoring and refactoring suggestion logic for CoderCore.

## Classes (1)

### `CoderQualityMixin`

Mixin for computing quality scores and refactoring suggestions.

**Methods** (2):
- `calculate_quality_score(self, metrics, violations, smells, coverage)`
- `suggest_refactorings(self, content)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `src.core.base.types.CodeMetrics.CodeMetrics`
- `src.core.base.types.CodeSmell.CodeSmell`
- `src.core.base.types.QualityScore.QualityScore`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
