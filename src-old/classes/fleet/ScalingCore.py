#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/ScalingCore.description.md

# ScalingCore

**File**: `src\\classes\fleet\\ScalingCore.py`  
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

**File**: `src\\classes\fleet\\ScalingCore.py`  
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

"""
ScalingCore logic for fleet expansion.
Pure logic for computing moving averages and scaling decisions.
"""
