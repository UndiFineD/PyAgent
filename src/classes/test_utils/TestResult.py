#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from .TestStatus import TestStatus

from dataclasses import dataclass, field
from typing import Optional
import time

@dataclass
class TestResult:
    __test__ = False
    """Result of a test execution.

    Attributes:
        test_name: Name of the test.
        status: Test status.
        duration_ms: Test duration.
        error_message: Error message if failed.
        assertions_count: Number of assertions.
        timestamp: When test was run.
    """

    test_name: str
    status: TestStatus
    duration_ms: float = 0.0
    error_message: Optional[str] = None
    assertions_count: int = 0
    timestamp: float = field(default_factory=time.time)
