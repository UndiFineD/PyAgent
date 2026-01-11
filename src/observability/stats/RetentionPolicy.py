#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from dataclasses import dataclass
from typing import Optional


































from src.core.base.version import VERSION
__version__ = VERSION

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
