"""LLM_CONTEXT_START

## Source: src-old/logic/agents/specialized/FinancialAgent.description.md

# FinancialAgent

**File**: `src\\logic\agents\\specialized\\FinancialAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 52  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for FinancialAgent.

## Classes (1)

### `FinancialAgent`

**Inherits from**: BaseAgent

Phase 286: Financial Agent.
Estimates the real-world dollar cost of improvement cycles based on model usage.

**Methods** (1):
- `__init__(self, file_path)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/specialized/FinancialAgent.improvements.md

# Improvements for FinancialAgent

**File**: `src\\logic\agents\\specialized\\FinancialAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 52 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `FinancialAgent_test.py` with pytest tests

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

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Apache 2.0 License
from typing import Any

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool


class FinancialAgent(BaseAgent):
    """Phase 286: Financial Agent.
    Estimates the real-world dollar cost of improvement cycles based on model usage.
    """

    def __init__(self, file_path: str = "budget.audit") -> None:
        super().__init__(file_path)
        self.pricing = {
            "Ollama": 0.0,
            "GPT-4o": 15.00,  # Per 1M tokens
            "GPT-4o-mini": 0.15,
            "Claude-3.5-Sonnet": 3.00,
            "DeepSeek-V3": 0.20,
            "GLM-4": 0.10,
        }

    @as_tool
    async def calculate_run_cost(self, token_usage: dict[str, Any]) -> dict[str, Any]:
        """Calculates cost based on token usage.
        Example token_usage: {"GPT-4o": 500000, "Ollama": 1200000}
        """
        total_usd = 0.0
        details = []

        for model, count in token_usage.items():
            rate = self.pricing.get(model, 1.0)  # Default to 1.0/million if unknown
            cost = (count / 1_000_000) * rate
            total_usd += cost
            details.append(
                {"model": model, "tokens": count, "cost_usd": round(cost, 4)}
            )

        return {"total_usd": round(total_usd, 2), "breakdown": details}

    async def get_improvement_items(
        self, context: dict[str, Any]
    ) -> list[dict[str, Any]]:
        # Financial agent doesn't modify code directly, it audits.
        return []
