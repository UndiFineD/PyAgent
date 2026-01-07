#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .AlertSeverity import AlertSeverity

from dataclasses import dataclass
from typing import Optional

@dataclass
class Threshold:
    """Threshold configuration for alerting."""
    metric_name: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    severity: Optional[AlertSeverity] = None  # Will be set to MEDIUM (3) by default
    message: str = ""
    operator: str = ""  # For backwards compatibility
    value: float = 0.0  # For backwards compatibility

    def __post_init__(self) -> None:
        if self.severity is None:
            self.severity = AlertSeverity.MEDIUM
