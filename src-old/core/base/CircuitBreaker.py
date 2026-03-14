#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/CircuitBreaker.description.md

# CircuitBreaker

**File**: `src\\core\base\\CircuitBreaker.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 213  
**Complexity**: 7 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `CircuitBreaker`

Circuit breaker pattern for failing backends with Jittered Backoff.

Manages failing backends with exponential backoff and recovery.
Tracks failure state and prevents cascading failures.
Includes Phase 144 Jitter and 2-min max failure TTL.
Delegates transition logic to ResilienceCore (Phase 231).

States:
    CLOSED: Normal operation, requests pass through
    OPEN: Too many failures, requests fail immediately
    HALF_OPEN: Testing if backend recovered

**Methods** (7):
- `__init__(self, name, failure_threshold, recovery_timeout, backoff_multiplier, otel_manager)`
- `_get_thresholds(self)`
- `_get_current_timeout(self)`
- `_export_to_otel(self, old_state, new_state)`
- `call(self, func)`
- `on_success(self)`
- `on_failure(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `asyncio`
- `collections.abc.Callable`
- `inspect`
- `logging`
- `src.core.base.Version.VERSION`
- `src.core.base.core.ResilienceCore.ResilienceCore`
- `src.observability.stats.exporters.OTelManager`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/core/base/CircuitBreaker.improvements.md

# Improvements for CircuitBreaker

**File**: `src\\core\base\\CircuitBreaker.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 213 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CircuitBreaker_test.py` with pytest tests

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


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


r"""Auto-extracted class from agent.py"""
