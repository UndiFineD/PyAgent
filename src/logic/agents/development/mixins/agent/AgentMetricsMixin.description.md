# AgentMetricsMixin

**File**: `src\logic\agents\development\mixins\agent\AgentMetricsMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 110  
**Complexity**: 4 (simple)

## Overview

Code metrics and quality logic for CoderAgent.

## Classes (1)

### `AgentMetricsMixin`

Mixin for code metrics, quality scoring, and smell detection.

**Methods** (4):
- `calculate_metrics(self, content)`
- `_get_test_coverage(self)`
- `calculate_quality_score(self, content)`
- `detect_code_smells(self, content)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `re`
- `shutil`
- `src.core.base.types.CodeMetrics.CodeMetrics`
- `src.core.base.types.CodeSmell.CodeSmell`
- `src.core.base.types.QualityScore.QualityScore`
- `subprocess`
- `sys`

---
*Auto-generated documentation*
