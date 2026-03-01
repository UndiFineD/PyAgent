# StructuralAnalysisMixin

**File**: `src\infrastructure\orchestration\intel\mixins\StructuralAnalysisMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 79  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for StructuralAnalysisMixin.

## Classes (1)

### `StructuralAnalysisMixin`

Mixin for structural health and versioning checks in SelfImprovementAnalysis.

**Methods** (3):
- `check_versioning(self)`
- `add_structural_findings(self, findings, file_path, rel_path, content)`
- `add_hive_findings(self, findings, file_path, rel_path, active_tasks)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `os`
- `re`
- `src.infrastructure.orchestration.intel.SelfImprovementAnalysis.SelfImprovementAnalysis`
- `typing.Any`
- `typing.TYPE_CHECKING`

---
*Auto-generated documentation*
