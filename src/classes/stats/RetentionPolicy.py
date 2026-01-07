#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class RetentionPolicy:
    """Policy for data retention."""
    name: str = ""  # Changed from metric_name to name for constructor
    retention_days: int = 0
    resolution: str = "1m"
    metric_name: Optional[str] = None
    namespace: str = ""
    max_age_days: int = 0
    max_points: int = 0
    compression_after_days: int = 7
