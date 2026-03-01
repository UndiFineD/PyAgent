# TokenCostEngine

**File**: `src\classes\stats\TokenCostEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 30  
**Complexity**: 3 (simple)

## Overview

Utility for calculating token usage costs across different models.
Inspired by tokencost and other cost tracking tools.

## Classes (1)

### `TokenCostEngine`

Calculates estimated costs for LLM tokens based on model variety.
Shell for TokenCostCore.

**Methods** (3):
- `__init__(self)`
- `calculate_cost(self, model, input_tokens, output_tokens)`
- `get_supported_models(self)`

## Dependencies

**Imports** (6):
- `TokenCostCore.MODEL_COSTS`
- `TokenCostCore.TokenCostCore`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
