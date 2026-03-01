# ModelFallbackCore

**File**: `src\classes\stats\ModelFallbackCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 40  
**Complexity**: 4 (simple)

## Overview

ModelFallbackCore logic for redundancy and cost optimization.
Pure logic for selecting fallback models and price comparisons.

## Classes (1)

### `ModelFallbackCore`

Pure logic core for model fallback strategies.

**Methods** (4):
- `__init__(self, fallback_chains)`
- `determine_next_model(self, current_model)`
- `rank_models_by_cost(self, models, model_price_map)`
- `validate_retry_limit(self, current_retry, max_retries)`

## Dependencies

**Imports** (4):
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
