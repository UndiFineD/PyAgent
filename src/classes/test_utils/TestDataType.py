#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from enum import Enum

class TestDataType(Enum):
    __test__ = False
    """Types of test data."""

    PYTHON_CODE = "python_code"
    MARKDOWN = "markdown"
    JSON = "json"
    YAML = "yaml"
    TEXT = "text"
