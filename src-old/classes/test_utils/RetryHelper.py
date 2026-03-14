#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/test_utils/RetryHelper.description.md

# RetryHelper

**File**: `src\\classes\test_utils\\RetryHelper.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 31  
**Complexity**: 2 (simple)

## Overview

Auto-extracted class from agent_test_utils.py

## Classes (1)

### `RetryHelper`

Simple retry helper for flaky operations.

**Methods** (2):
- `__init__(self, max_retries, delay_seconds)`
- `retry(self, fn)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `threading`
- `time`
- `typing.Callable`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/test_utils/RetryHelper.improvements.md

# Improvements for RetryHelper

**File**: `src\\classes\test_utils\\RetryHelper.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 31 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `RetryHelper_test.py` with pytest tests

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


r"""Auto-extracted class from agent_test_utils.py"""
