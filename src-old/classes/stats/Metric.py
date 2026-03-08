#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/stats/Metric.description.md

# Metric

**File**: `src\classes\stats\Metric.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 28  
**Complexity**: 2 (simple)

## Overview

Auto-extracted class from agent_stats.py

## Classes (1)

### `Metric`

A single metric.

**Methods** (2):
- `__iter__(self)`
- `__getitem__(self, index)`

## Dependencies

**Imports** (5):
- `MetricType.MetricType`
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/classes/stats/Metric.improvements.md

# Improvements for Metric

**File**: `src\classes\stats\Metric.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 28 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `Metric_test.py` with pytest tests

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

"""Auto-extracted class from agent_stats.py"""


from .MetricType import MetricType

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Metric:
    """A single metric."""
    name: str
    value: float
    metric_type: MetricType
    timestamp: str = ""
    namespace: str = "default"
    tags: Dict[str, str] = field(default_factory=lambda: {})

    # Compatibility: some tests treat history entries as (timestamp, value) tuples.
    def __iter__(self) -> Any:
        yield self.timestamp
        yield self.value

    def __getitem__(self, index: int) -> Any:
        return (self.timestamp, self.value)[index]
