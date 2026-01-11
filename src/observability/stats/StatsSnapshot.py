#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass
from typing import Any, Dict


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class StatsSnapshot:
    """A persisted snapshot for StatsSnapshotManager."""

    name: str
    data: Dict[str, Any]
    timestamp: str
