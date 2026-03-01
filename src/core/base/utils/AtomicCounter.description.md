# AtomicCounter

**File**: `src\core\base\utils\AtomicCounter.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 4 imports  
**Lines**: 334  
**Complexity**: 36 (complex)

## Overview

AtomicCounter - Thread-safe counter with Rust acceleration.

Inspired by vLLM's counter.py patterns for high-frequency atomic operations.

Phase 17: vLLM Pattern Integration

## Classes (4)

### `Counter`

Simple non-atomic counter for single-threaded use.

Use AtomicCounter for multi-threaded scenarios.

**Methods** (6):
- `__init__(self, start)`
- `value(self)`
- `inc(self, delta)`
- `dec(self, delta)`
- `reset(self, value)`
- `__repr__(self)`

### `AtomicCounter`

Thread-safe atomic counter.

Uses a lock internally for thread safety. For extremely high-frequency
operations, consider using Rust-accelerated atomic operations.

Example:
    >>> counter = AtomicCounter()
    >>> counter.inc()
    1
    >>> counter.inc(5)
    6
    >>> counter.value
    6

**Methods** (12):
- `__init__(self, start, use_rust)`
- `value(self)`
- `inc(self, delta)`
- `dec(self, delta)`
- `add(self, delta)`
- `sub(self, delta)`
- `reset(self, value)`
- `compare_and_swap(self, expected, new_value)`
- `get_and_reset(self)`
- `__repr__(self)`
- ... and 2 more methods

### `AtomicFlag`

Thread-safe atomic boolean flag.

Useful for signaling between threads.

**Methods** (8):
- `__init__(self, initial)`
- `value(self)`
- `set(self)`
- `clear(self)`
- `toggle(self)`
- `test_and_set(self)`
- `__bool__(self)`
- `__repr__(self)`

### `AtomicGauge`

Thread-safe gauge that tracks min, max, and current value.

Useful for monitoring metrics that can go up and down.

**Methods** (10):
- `__init__(self, initial)`
- `value(self)`
- `min(self)`
- `max(self)`
- `set(self, value)`
- `inc(self, delta)`
- `dec(self, delta)`
- `snapshot(self)`
- `reset(self, value)`
- `__repr__(self)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `rust_core.rust_core`
- `threading`
- `typing.Optional`

---
*Auto-generated documentation*
