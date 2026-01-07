#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .AlertSeverity import AlertSeverity

from dataclasses import dataclass

@dataclass
class Alert:
    """An alert triggered by a threshold breach."""
    id: str
    metric_name: str
    current_value: float
    threshold_value: float
    severity: AlertSeverity
    message: str
    timestamp: str
