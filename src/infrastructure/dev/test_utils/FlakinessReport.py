#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

@dataclass
class FlakinessReport:
    """Report of test flakiness analysis.

    Attributes:
        test_name: Name of the test.
        runs: Number of test runs.
        passes: Number of passed runs.
        failures: Number of failed runs.
        flakiness_score: Score from 0 (stable) to 1 (very flaky).
        failure_messages: Unique failure messages.
    """

    test_name: str
    runs: int
    passes: int
    failures: int
    flakiness_score: float
    failure_messages: List[str] = field(default_factory=lambda: [])
