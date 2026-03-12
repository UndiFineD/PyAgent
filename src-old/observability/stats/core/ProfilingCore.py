r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/core/ProfilingCore.description.md

# ProfilingCore

**File**: `src\observability\stats\core\ProfilingCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 4 imports  
**Lines**: 44  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ProfilingCore.

## Classes (2)

### `ProfileStats`

Class ProfileStats implementation.

### `ProfilingCore`

Pure logic for cProfile aggregation and bottleneck analysis.
Identifies slow methods and calculates optimization priority.

**Methods** (3):
- `analyze_stats(self, pstats_obj, limit)`
- `identify_bottlenecks(self, stats, threshold_ms)`
- `calculate_optimization_priority(self, stats)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `dataclasses.dataclass`
- `pstats`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/core/ProfilingCore.improvements.md

# Improvements for ProfilingCore

**File**: `src\observability\stats\core\ProfilingCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 44 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: ProfileStats

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ProfilingCore_test.py` with pytest tests

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

from __future__ import annotations

import pstats
from dataclasses import dataclass


@dataclass(frozen=True)
class ProfileStats:
    function_name: str
    call_count: int
    total_time: float
    per_call: float


class ProfilingCore:
    """Pure logic for cProfile aggregation and bottleneck analysis.
    Identifies slow methods and calculates optimization priority.
    """

    def analyze_stats(
        self, pstats_obj: pstats.Stats, limit: int = 10
    ) -> list[ProfileStats]:
        """Converts raw pstats into a list of pure ProfileStats dataclasses."""
        results = []
        pstats_obj.sort_stats("cumulative")

        # pstats stores data in a complex tuple structure
        # (cc, nc, tt, ct, callers)
        for func, (cc, nc, tt, ct, callers) in pstats_obj.stats.items():
            if len(results) >= limit:
                break
            results.append(
                ProfileStats(
                    function_name=str(func),
                    call_count=cc,
                    total_time=ct,
                    per_call=ct / cc if cc > 0 else 0,
                )
            )

        return results

    def identify_bottlenecks(
        self, stats: list[ProfileStats], threshold_ms: float = 100.0
    ) -> list[str]:
        """Identifies functions exceeding the time threshold."""
        return [
            s.function_name for s in stats if s.total_time > (threshold_ms / 1000.0)
        ]

    def calculate_optimization_priority(self, stats: ProfileStats) -> float:
        """Heuristic for optimization: time * frequency."""
        return stats.total_time * stats.call_count
