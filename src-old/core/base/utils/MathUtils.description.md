# MathUtils

**File**: `src\core\base\utils\MathUtils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 14 functions, 4 imports  
**Lines**: 271  
**Complexity**: 14 (moderate)

## Overview

MathUtils - Centralized mathematical utilities with Rust acceleration.

Inspired by vLLM's math_utils.py patterns for high-performance operations.

Phase 17: vLLM Pattern Integration

## Functions (14)

### `cdiv(a, b)`

Ceiling division without floating point.

Uses the identity: -(a // -b) == ceil(a / b)
This is faster than (a + b - 1) // b and handles negative numbers correctly.

Args:
    a: Dividend
    b: Divisor (must not be zero)
    
Returns:
    Ceiling of a / b
    
Examples:
    >>> cdiv(7, 3)
    3
    >>> cdiv(6, 3)
    2
    >>> cdiv(1, 3)
    1

### `next_power_of_2(n)`

Return the smallest power of 2 >= n.

Uses bit_length() for O(1) performance.

Args:
    n: Input integer (must be positive)
    
Returns:
    Smallest power of 2 that is >= n
    
Examples:
    >>> next_power_of_2(7)
    8
    >>> next_power_of_2(8)
    8
    >>> next_power_of_2(1)
    1

### `prev_power_of_2(n)`

Return the largest power of 2 <= n (inclusive).

Args:
    n: Input integer (must be positive)
    
Returns:
    Largest power of 2 that is <= n
    
Examples:
    >>> prev_power_of_2(7)
    4
    >>> prev_power_of_2(8)
    8
    >>> prev_power_of_2(1)
    1

### `is_power_of_2(n)`

Check if n is a power of 2.

Uses bitwise AND for O(1) check.

Args:
    n: Input integer
    
Returns:
    True if n is a power of 2

### `round_up(n, multiple)`

Round n up to the nearest multiple.

Args:
    n: Input integer
    multiple: Multiple to round to
    
Returns:
    Smallest multiple of 'multiple' that is >= n
    
Examples:
    >>> round_up(7, 4)
    8
    >>> round_up(8, 4)
    8

### `round_down(n, multiple)`

Round n down to the nearest multiple.

Args:
    n: Input integer
    multiple: Multiple to round to
    
Returns:
    Largest multiple of 'multiple' that is <= n
    
Examples:
    >>> round_down(7, 4)
    4
    >>> round_down(8, 4)
    8

### `clamp(value, min_val, max_val)`

Clamp a value between min and max bounds.

Args:
    value: Input value
    min_val: Minimum bound
    max_val: Maximum bound
    
Returns:
    Clamped value

### `align_to(n, alignment)`

Align n to the given alignment (round up to nearest multiple).

This is useful for memory alignment operations.

Args:
    n: Input integer
    alignment: Alignment boundary
    
Returns:
    n aligned to the boundary

### `bit_count(n)`

Count the number of 1 bits in the binary representation of n.

Cached for repeated queries.

Args:
    n: Input integer
    
Returns:
    Number of 1 bits

### `gcd(a, b)`

Compute greatest common divisor using Euclidean algorithm.

Args:
    a: First integer
    b: Second integer
    
Returns:
    GCD of a and b

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `functools`
- `rust_core.rust_core`
- `typing.Union`

---
*Auto-generated documentation*
