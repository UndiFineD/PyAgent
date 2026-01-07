#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from enum import Enum

class FederationMode(Enum):
    """Federation modes for multi-repo aggregation."""
    PULL = "pull"
    PUSH = "push"
    HYBRID = "hybrid"
