#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from enum import Enum

class CleanupStrategy(Enum):
    """Cleanup strategies for test resources."""

    IMMEDIATE = "immediate"
    DEFERRED = "deferred"
    ON_SUCCESS = "on_success"
    NEVER = "never"
