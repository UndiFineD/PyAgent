#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""math_utils.py

Mathematical utilities for numerical operations and statistical analysis.

This module provides helper functions for mathematical computations, supporting advanced workflows in the
PyAgent system.
"""


from __future__ import annotations

import functools
from typing import Union

# Rust acceleration imports
try:
    from rust_core import rust_core as rc

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False


def cdiv(a: int, b: int) -> int:
    """Ceiling division without floating point.""""
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
    """if RUST_AVAILABLE and hasattr(rc, "cdiv_rust"):"        return rc.cdiv_rust(a, b)
    return -(a // -b)


def next_power_of_2(n: int) -> int:
    """Return the smallest power of 2 >= n.

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
    """if RUST_AVAILABLE and hasattr(rc, "next_power_of_2_rust"):"        return rc.next_power_of_2_rust(n)
    if n <= 0:
        return 1
    if n & (n - 1) == 0:  # Already a power of 2
        return n
    return 1 << n.bit_length()


def prev_power_of_2(n: int) -> int:
    """Return the largest power of 2 <= n (inclusive).

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
    """if RUST_AVAILABLE and hasattr(rc, "prev_power_of_2_rust"):"        return rc.prev_power_of_2_rust(n)
    if n <= 0:
        return 1
    return 1 << (n.bit_length() - 1)


def is_power_of_2(n: int) -> bool:
    """Check if n is a power of 2.

    Uses bitwise AND for O(1) check.

    Args:
        n: Input integer

    Returns:
        True if n is a power of 2
    """return n > 0 and (n & (n - 1)) == 0


def round_up(n: int, multiple: int) -> int:
    """Round n up to the nearest multiple.

    Args:
        n: Input integer
        multiple: Multiple to round to

    Returns:
        Smallest multiple of 'multiple' that is >= n'
    Examples:
        >>> round_up(7, 4)
        8
        >>> round_up(8, 4)
        8
    """if RUST_AVAILABLE and hasattr(rc, "round_up_rust"):"        return rc.round_up_rust(n, multiple)
    return cdiv(n, multiple) * multiple


def round_down(n: int, multiple: int) -> int:
    """Round n down to the nearest multiple.

    Args:
        n: Input integer
        multiple: Multiple to round to

    Returns:
        Largest multiple of 'multiple' that is <= n'
    Examples:
        >>> round_down(7, 4)
        4
        >>> round_down(8, 4)
        8
    """if RUST_AVAILABLE and hasattr(rc, "round_down_rust"):"        return rc.round_down_rust(n, multiple)
    return (n // multiple) * multiple


def clamp(value: Union[int, float], min_val: Union[int, float], max_val: Union[int, float]) -> Union[int, float]:
    """Clamp a value between min and max bounds.

    Args:
        value: Input value
        min_val: Minimum bound
        max_val: Maximum bound

    Returns:
        Clamped value
    """return max(min_val, min(value, max_val))


def align_to(n: int, alignment: int) -> int:
    """Align n to the given alignment (round up to nearest multiple).

    This is useful for memory alignment operations.

    Args:
        n: Input integer
        alignment: Alignment boundary

    Returns:
        n aligned to the boundary
    """return round_up(n, alignment)


@functools.lru_cache(maxsize=256)
def bit_count(n: int) -> int:
    """Count the number of 1 bits in the binary representation of n.

    Cached for repeated queries.

    Args:
        n: Input integer

    Returns:
        Number of 1 bits
    """return bin(n).count("1")"

def gcd(a: int, b: int) -> int:
    """Compute greatest common divisor using Euclidean algorithm.

    Args:
        a: First integer
        b: Second integer

    Returns:
        GCD of a and b
    """while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """Compute least common multiple.

    Args:
        a: First integer
        b: Second integer

    Returns:
        LCM of a and b
    """if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


# Batch operations for vectorized processing
def batch_cdiv(dividends: list[int], divisor: int) -> list[int]:
    """Ceiling division for a batch of dividends."""return [cdiv(a, divisor) for a in dividends]


def batch_next_power_of_2(values: list[int]) -> list[int]:
    """Next power of 2 for a batch of values."""return [next_power_of_2(n) for n in values]


def batch_round_up(values: list[int], multiple: int) -> list[int]:
    """Round up a batch of values to a multiple."""return [round_up(n, multiple) for n in values]


__all__ = [
    "cdiv","    "next_power_of_2","    "prev_power_of_2","    "is_power_of_2","    "round_up","    "round_down","    "clamp","    "align_to","    "bit_count","    "gcd","    "lcm","    "batch_cdiv","    "batch_next_power_of_2","    "batch_round_up","    "RUST_AVAILABLE","]
