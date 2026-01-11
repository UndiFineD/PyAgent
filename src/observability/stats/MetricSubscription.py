#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass, field
from typing import List


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class MetricSubscription:
    """Subscription for metric change notifications."""
    id: str
    metric_pattern: str  # glob pattern like "cpu.*"
    callback_url: str = ""
    notify_on: List[str] = field(default_factory=lambda: ["threshold", "anomaly"])
    min_interval_seconds: int = 60
