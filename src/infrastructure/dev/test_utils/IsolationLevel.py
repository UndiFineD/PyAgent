#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from enum import Enum

class IsolationLevel(Enum):
    """File system isolation levels."""

    NONE = "none"
    TEMP_DIR = "temp_dir"
    COPY_ON_WRITE = "copy_on_write"
    SANDBOX = "sandbox"
