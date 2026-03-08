# DerivedMetricCalculator

**File**: `src\classes\stats\DerivedMetricCalculator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 146  
**Complexity**: 5 (moderate)

## Overview

Auto-extracted class from agent_stats.py

## Classes (1)

### `DerivedMetricCalculator`

Calculate derived metrics from dependencies using safe AST evaluation.

**Methods** (5):
- `__init__(self)`
- `_eval_node(self, node)`
- `register_derived(self, name, dependencies, formula, description)`
- `calculate(self, name, metric_values)`
- `get_all_derived(self, metric_values)`

## Dependencies

**Imports** (9):
- `DerivedMetric.DerivedMetric`
- `__future__.annotations`
- `ast`
- `logging`
- `math`
- `operator`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
