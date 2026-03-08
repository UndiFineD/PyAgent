#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/fleet/ScalingCore.description.md

# ScalingCore

**File**: `src\classes\fleet\ScalingCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 32  
**Complexity**: 4 (simple)

## Overview

ScalingCore logic for fleet expansion.
Pure logic for computing moving averages and scaling decisions.

## Classes (1)

### `ScalingCore`

Class ScalingCore implementation.

**Methods** (4):
- `__init__(self, scale_threshold, window_size)`
- `add_metric(self, key, value)`
- `should_scale(self, key)`
- `get_avg_latency(self, key)`

## Dependencies

**Imports** (3):
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/ScalingCore.improvements.md

# Improvements for ScalingCore

**File**: `src\classes\fleet\ScalingCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 32 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: ScalingCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ScalingCore_test.py` with pytest tests

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

"""
ScalingCore logic for fleet expansion.
Pure logic for computing moving averages and scaling decisions.
"""

from typing import Dict, List, Optional

class ScalingCore:
    def __init__(self, scale_threshold: float = 5.0, window_size: int = 10) -> None:
        self.scale_threshold = scale_threshold
        self.window_size = window_size
        self.load_metrics: Dict[str, List[float]] = {}

    def add_metric(self, key: str, value: float) -> None:
        if key not in self.load_metrics:
            self.load_metrics[key] = []
        self.load_metrics[key].append(value)
        if len(self.load_metrics[key]) > self.window_size:
            self.load_metrics[key].pop(0)

    def should_scale(self, key: str) -> bool:
        recent = self.load_metrics.get(key, [])
        if not recent:
            return False
        avg = sum(recent) / len(recent)
        return avg > self.scale_threshold

    def get_avg_latency(self, key: str) -> float:
        recent = self.load_metrics.get(key, [])
        return sum(recent) / len(recent) if recent else 0.0
