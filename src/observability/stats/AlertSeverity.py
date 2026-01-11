#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from enum import Enum


































from src.core.base.version import VERSION
__version__ = VERSION

class AlertSeverity(Enum):
    """Alert severity levels."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1
