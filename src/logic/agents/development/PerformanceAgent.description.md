# PerformanceAgent

**File**: `src\logic\agents\development\PerformanceAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 82  
**Complexity**: 2 (simple)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `PerformanceAgent`

Identifies and suggests code optimizations.

Analyzes code for performance bottlenecks and suggests
improvements.

Attributes:
    suggestions: List of optimization suggestions.

Example:
    >>> optimizer=PerformanceAgent()
    >>> suggestions=optimizer.analyze("for i in range(len(items)):")

**Methods** (2):
- `__init__(self)`
- `analyze(self, content)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `re`
- `src.core.base.types.OptimizationSuggestion.OptimizationSuggestion`
- `src.core.base.types.OptimizationType.OptimizationType`
- `src.core.base.version.VERSION`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
