#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass, field
from typing import Dict


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class MetricSnapshot:
    """A snapshot of metrics at a point in time."""
    name: str
    id: str
    timestamp: str
    metrics: Dict[str, float]
    tags: Dict[str, str] = field(default_factory=lambda: {})
