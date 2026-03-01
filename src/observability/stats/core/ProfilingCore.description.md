# ProfilingCore

**File**: `src\observability\stats\core\ProfilingCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 4 imports  
**Lines**: 44  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ProfilingCore.

## Classes (2)

### `ProfileStats`

Class ProfileStats implementation.

### `ProfilingCore`

Pure logic for cProfile aggregation and bottleneck analysis.
Identifies slow methods and calculates optimization priority.

**Methods** (3):
- `analyze_stats(self, pstats_obj, limit)`
- `identify_bottlenecks(self, stats, threshold_ms)`
- `calculate_optimization_priority(self, stats)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `dataclasses.dataclass`
- `pstats`
- `typing.List`

---
*Auto-generated documentation*
