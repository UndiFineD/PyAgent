#!/usr/bin/env python3
"""Known-bad fixture used to verify strict-lane mypy failures."""


def require_int(value: int) -> int:
    """Return the provided integer value.

    Args:
        value: Integer input.

    Returns:
        int: The original value.

    """
    return value


BROKEN_VALUE: str = "not-an-int"
BROKEN_RESULT: int = require_int(BROKEN_VALUE)
