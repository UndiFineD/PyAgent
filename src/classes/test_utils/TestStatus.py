#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from enum import Enum

class TestStatus(Enum):
    __test__ = False
    """Status of a test execution."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    PENDING = "pending"
