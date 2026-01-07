#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class StatsSnapshot:
    """A persisted snapshot for StatsSnapshotManager."""

    name: str
    data: Dict[str, Any]
    timestamp: str
