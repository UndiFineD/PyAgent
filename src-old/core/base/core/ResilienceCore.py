#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/core/ResilienceCore.description.md

# ResilienceCore

**File**: `src\core\base\core\ResilienceCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 2 imports  
**Lines**: 86  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ResilienceCore.

## Classes (1)

### `ResilienceCore`

Pure logic for Circuit Breaker and Retry mechanisms.
Audited for Rust conversion.

**Methods** (3):
- `calculate_backoff(failure_count, threshold, base_timeout, multiplier, max_timeout, jitter_mode)`
- `should_attempt_recovery(last_failure_time, current_time, timeout)`
- `evaluate_state_transition(current_state, success_count, consecutive_successes_needed, failure_count, failure_threshold)`

## Dependencies

**Imports** (2):
- `__future__.annotations`
- `random`

---
*Auto-generated documentation*
## Source: src-old/core/base/core/ResilienceCore.improvements.md

# Improvements for ResilienceCore

**File**: `src\core\base\core\ResilienceCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 86 lines (small)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ResilienceCore_test.py` with pytest tests

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

import random

class ResilienceCore:
    """
    Pure logic for Circuit Breaker and Retry mechanisms.
    Audited for Rust conversion.
    """

    @staticmethod
    def calculate_backoff(
        failure_count: int,
        threshold: int,
        base_timeout: float,
        multiplier: float,
        max_timeout: float,
        jitter_mode: str = "full"
    ) -> float:
        """
        Phase 145: Enhanced backoff with Full Jitter.
        Prevents thundering herd better than standard 10% jitter.
        """
        if failure_count < threshold:
            return 0.0
        
        exponent = max(0, failure_count - threshold)
        backoff = min(max_timeout, base_timeout * (multiplier ** exponent))
        
        if jitter_mode == "full":
            # AWS style Full Jitter: random between 0 and exponential backoff
            return random.uniform(base_timeout / 2, backoff)
        elif jitter_mode == "equal":
            # Half of backoff + random half
            return (backoff / 2) + random.uniform(0, backoff / 2)
        else:
            # Legacy 10% jitter
            jitter = backoff * 0.1 * random.uniform(-1, 1)
            return max(base_timeout / 2, backoff + jitter)

    @staticmethod
    def should_attempt_recovery(
        last_failure_time: float,
        current_time: float,
        timeout: float
    ) -> bool:
        """Determines if the cooldown period has passed."""
        return (current_time - last_failure_time) > timeout

    @staticmethod
    def evaluate_state_transition(
        current_state: str,
        success_count: int,
        consecutive_successes_needed: int,
        failure_count: int,
        failure_threshold: int
    ) -> str:
        """
        Pure state machine logic for transition.
        Transitions:
            CLOSED -> OPEN (if failure_count >= threshold)
            OPEN -> HALF_OPEN (externally timed)
            HALF_OPEN -> CLOSED (if success_count >= needed)
            HALF_OPEN -> OPEN (if any failure during half-open)
        """
        if current_state == "CLOSED":
            if failure_count >= failure_threshold:
                return "OPEN"
        elif current_state == "HALF_OPEN":
            if success_count >= consecutive_successes_needed:
                return "CLOSED"
        
        return current_state