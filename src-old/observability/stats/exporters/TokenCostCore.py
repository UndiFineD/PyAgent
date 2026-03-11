r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/exporters/TokenCostCore.description.md

# TokenCostCore

**File**: `src\observability\stats\exporters\TokenCostCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 41  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for TokenCostCore.

## Classes (1)

### `TokenCostCore`

Pure logic for cost calculations.
No I/O or state management.

**Methods** (3):
- `compute_usd(self, model, input_tokens, output_tokens)`
- `_find_pricing(self, model_key)`
- `list_models(self)`

## Dependencies

**Imports** (3):
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/exporters/TokenCostCore.improvements.md

# Improvements for TokenCostCore

**File**: `src\observability\stats\exporters\TokenCostCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 41 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TokenCostCore_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from typing import Dict, List

# Constants for common models (Jan 2026 estimates)
MODEL_COSTS = {
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "claude-3-5-sonnet": {"input": 0.003, "output": 0.015},
    "claude-3-opus": {"input": 0.015, "output": 0.075},
    "gemini-1-5-pro": {"input": 0.0035, "output": 0.0105},
    "gemini-2-0-flash": {"input": 0.0001, "output": 0.0004},
    "default": {"input": 0.002, "output": 0.002},
}


class TokenCostCore:
    """Pure logic for cost calculations.
    No I/O or state management.
    """

    def compute_usd(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Returns the estimated cost in USD."""
        model_key = model.lower()
        pricing = self._find_pricing(model_key)

        # Cost per 1k tokens
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]

        return round(input_cost + output_cost, 6)

    def _find_pricing(self, model_key: str) -> Dict[str, float]:
        """Heuristic for finding model pricing."""
        pricing = MODEL_COSTS.get(model_key)
        if not pricing:
            for key in MODEL_COSTS:
                if key != "default" and key in model_key:
                    return MODEL_COSTS[key]
        return pricing or MODEL_COSTS["default"]

    def list_models(self) -> List[str]:
        return list(MODEL_COSTS.keys())
