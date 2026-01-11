#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class ParallelTestResult:
    """Result from parallel test execution.

    Attributes:
        test_name: Name of the test.
        passed: Whether test passed.
        duration_ms: Test duration.
        error: Error if failed.
        worker_id: Worker that ran the test.
    """

    test_name: str
    passed: bool
    duration_ms: float
    error: Optional[str] = None
    worker_id: int = 0
