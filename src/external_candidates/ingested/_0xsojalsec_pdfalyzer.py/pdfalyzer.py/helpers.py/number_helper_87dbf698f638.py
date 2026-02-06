# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdfalyzer\pdfalyzer\helpers\number_helper.py
"""
Some simple math helpers.
"""


def is_divisible_by(n: int, divisor: int) -> bool:
    """Returns True if 'n' is evenly divisible by 'divisor'."""
    return divmod(n, divisor)[1] == 0


def is_even(n: int) -> bool:
    """Returns True if 'n' is even."""
    return is_divisible_by(n, 2)
