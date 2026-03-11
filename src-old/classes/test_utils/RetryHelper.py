#!/usr/bin/env python3
"""LLM_CONTEXT_START

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

"""Auto-extracted class from agent_test_utils.py"""


import threading
from typing import Callable, Optional


class RetryHelper:
    """Simple retry helper for flaky operations."""

    def __init__(self, max_retries: int = 3, delay_seconds: float = 0.0) -> None:
        self.max_retries = int(max_retries)
        self.delay_seconds = float(delay_seconds)

    def retry(self, fn: Callable[[], T]) -> T:
        last_exc: Optional[BaseException] = None
        for attempt in range(self.max_retries):
            try:
                return fn()
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if attempt == self.max_retries - 1:
                    raise
                if self.delay_seconds > 0:
                    threading.Event().wait(self.delay_seconds)
        if last_exc is not None:
            raise last_exc
        raise RuntimeError("RetryHelper failed without exception")
