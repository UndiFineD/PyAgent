# ProfilingAdvisor

**File**: `src\classes\coder\ProfilingAdvisor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 101  
**Complexity**: 3 (simple)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `ProfilingAgent`

Provides code profiling suggestions.
Integrated with ProfilingCore for cProfile analysis and bottleneck detection.

**Methods** (3):
- `__init__(self)`
- `analyze_pstats(self, pstats_filepath)`
- `_analyze_function(self, node)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `ast`
- `logging`
- `pstats`
- `src.core.base.types.ProfilingCategory.ProfilingCategory`
- `src.core.base.types.ProfilingSuggestion.ProfilingSuggestion`
- `src.core.base.version.VERSION`
- `src.observability.stats.core.ProfilingCore.ProfileStats`
- `src.observability.stats.core.ProfilingCore.ProfilingCore`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
