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
