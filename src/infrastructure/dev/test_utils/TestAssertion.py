#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

@dataclass
class TestAssertion:
    __test__ = False
    """Custom assertion for agent testing.

    Attributes:
        name: Assertion name.
        expected: Expected value.
        actual: Actual value.
        passed: Whether assertion passed.
        message: Assertion message.
    """

    name: str
    expected: Any
    actual: Any
    passed: bool = False
    message: str = ""
