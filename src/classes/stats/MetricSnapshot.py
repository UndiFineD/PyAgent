#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class MetricSnapshot:
    """A snapshot of metrics at a point in time."""
    name: str
    id: str
    timestamp: str
    metrics: Dict[str, float]
    tags: Dict[str, str] = field(default_factory=lambda: {})
