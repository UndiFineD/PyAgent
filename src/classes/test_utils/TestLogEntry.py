#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time

@dataclass
class TestLogEntry:
    __test__ = False
    """A test log entry.

    Attributes:
        level: Log level.
        message: Log message.
        timestamp: When logged.
        test_name: Associated test.
        extra: Extra data.
    """

    level: str
    message: str
    timestamp: float = field(default_factory=time.time)
    test_name: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=lambda: {})
