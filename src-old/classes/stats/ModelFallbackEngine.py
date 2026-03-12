#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/stats/ModelFallbackEngine.description.md

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
## Source: src-old/classes/stats/ModelFallbackEngine.improvements.md

# Improvements for ModelFallbackEngine

**File**: `src\classes\stats\ModelFallbackEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 44 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ModelFallbackEngine_test.py` with pytest tests

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

import logging
from typing import List, Optional, Dict, Any
from src.classes.stats.TokenCostEngine import TokenCostEngine
from .ModelFallbackCore import ModelFallbackCore


class ModelFallbackEngine:
    """
    Manages model redundancy and fallback strategies.
    Shell for ModelFallbackCore.
    """

    def __init__(
        self, cost_engine: Optional[TokenCostEngine] = None, fleet: Optional[Any] = None
    ) -> None:
        if fleet and hasattr(fleet, "telemetry") and not cost_engine:
            self.cost_engine = fleet.telemetry.cost_engine
        else:
            self.cost_engine = cost_engine
        self.core = ModelFallbackCore()
        self.max_retries = 3

    def get_fallback_model(
        self, current_model: str, failure_reason: str = ""
    ) -> Optional[str]:
        """Determines the next model to use after a failure."""
        logging.warning(
            f"Fallback requested for {current_model}. Reason: {failure_reason}"
        )
        next_model = self.core.determine_next_model(current_model)
        if next_model:
            logging.info(f"Stepping to next model: {next_model}")
        return next_model

    def get_cheapest_model(self, models: List[str]) -> str:
        """Returns the cheapest model from the list based on the cost engine."""
        price_map = {}
        if self.cost_engine:
            price_map = self.cost_engine.MODEL_COSTS

        ranked = self.core.rank_models_by_cost(models, price_map)
        return ranked[0]


if __name__ == "__main__":
    cost_engine = TokenCostEngine()
    fallback = ModelFallbackEngine(cost_engine)

    print(f"Fallback for gpt-4o: {fallback.get_fallback_model('gpt-4o')}")
    print(
        f"Cheapest of [gpt-4o, gpt-4o-mini]: {fallback.get_cheapest_model(['gpt-4o', 'gpt-4o-mini'])}"
    )
