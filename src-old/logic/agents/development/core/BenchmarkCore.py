"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/development/core/BenchmarkCore.description.md

# BenchmarkCore

**File**: `src\logic\agents\development\core\BenchmarkCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 5 imports  
**Lines**: 40  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for BenchmarkCore.

## Classes (2)

### `BenchmarkResult`

Class BenchmarkResult implementation.

### `BenchmarkCore`

Pure logic for agent performance benchmarking and regression gating.
Calculates baselines and validates performance constraints.

**Methods** (3):
- `calculate_baseline(self, results)`
- `check_regression(self, current_latency, baseline, threshold)`
- `score_efficiency(self, result)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `dataclasses.dataclass`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/development/core/BenchmarkCore.improvements.md

# Improvements for BenchmarkCore

**File**: `src\logic\agents\development\core\BenchmarkCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 40 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: BenchmarkResult

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `BenchmarkCore_test.py` with pytest tests

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

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkResult:
    agent_id: str
    latency_ms: float
    token_count: int
    success: bool


class BenchmarkCore:
    """Pure logic for agent performance benchmarking and regression gating.
    Calculates baselines and validates performance constraints.
    """

    def calculate_baseline(self, results: list[BenchmarkResult]) -> float:
        """Calculates the mean latency from a set of benchmark results."""
        if not results:
            return 0.0
        return sum(r.latency_ms for r in results) / len(results)

    def check_regression(
        self, current_latency: float, baseline: float, threshold: float = 0.1
    ) -> dict[str, Any]:
        """Checks if current latency exceeds the baseline by the given threshold."""
        if baseline <= 0:
            return {"regression": False, "delta": 0.0}

        delta = (current_latency - baseline) / baseline
        return {
            "regression": delta > threshold,
            "delta_percentage": delta * 100,
            "limit": threshold * 100,
        }

    def score_efficiency(self, result: BenchmarkResult) -> float:
        """Scores efficiency based on latency per token."""
        if result.token_count <= 0:
            return 0.0
        return result.latency_ms / result.token_count
