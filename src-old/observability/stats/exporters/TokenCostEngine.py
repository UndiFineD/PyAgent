#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/exporters/TokenCostEngine.description.md

# TokenCostEngine

**File**: `src\observability\stats\exporters\TokenCostEngine.py`  
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
## Source: src-old/observability/stats/exporters/TokenCostEngine.improvements.md

# Improvements for TokenCostEngine

**File**: `src\observability\stats\exporters\TokenCostEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 30 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `TokenCostEngine_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""Utility for calculating token usage costs across different models.
Inspired by tokencost and other cost tracking tools.
"""


# Constants for common models (Jan 2026 estimates)
from .TokenCostCore import MODEL_COSTS, TokenCostCore


class TokenCostEngine:
    """Calculates estimated costs for LLM tokens based on model variety.
    Shell for TokenCostCore.
    """

    def __init__(self) -> None:
        self.core = TokenCostCore()
        # Keep global reference for backward compatibility if needed
        self.MODEL_COSTS = MODEL_COSTS

    def calculate_cost(
        self, model: str, input_tokens: int = 0, output_tokens: int = 0
    ) -> float:
        """Returns the estimated cost in USD for the given token counts."""
        return self.core.compute_usd(model, input_tokens, output_tokens)

    def get_supported_models(self) -> list:
        """Returns list of models with explicit pricing."""
        return self.core.list_models()
