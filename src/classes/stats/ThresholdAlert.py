#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass
class ThresholdAlert:
    """A single threshold alert emitted by ThresholdAlertManager."""

    metric: str
    value: float
    severity: str
    threshold: float
