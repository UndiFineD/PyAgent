#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class ThresholdAlert:
    """A single threshold alert emitted by ThresholdAlertManager."""

    metric: str
    value: float
    severity: str
    threshold: float
