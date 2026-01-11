#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from enum import Enum


































from src.core.base.version import VERSION
__version__ = VERSION

class FederationMode(Enum):
    """Federation modes for multi-repo aggregation."""
    PULL = "pull"
    PUSH = "push"
    HYBRID = "hybrid"
