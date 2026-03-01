# ModelFallbackEngine

**File**: `src\classes\stats\ModelFallbackEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 44  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ModelFallbackEngine.

## Classes (1)

### `ModelFallbackEngine`

Manages model redundancy and fallback strategies.
Shell for ModelFallbackCore.

**Methods** (3):
- `__init__(self, cost_engine, fleet)`
- `get_fallback_model(self, current_model, failure_reason)`
- `get_cheapest_model(self, models)`

## Dependencies

**Imports** (7):
- `ModelFallbackCore.ModelFallbackCore`
- `logging`
- `src.classes.stats.TokenCostEngine.TokenCostEngine`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
