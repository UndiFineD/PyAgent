#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from enum import Enum


































from src.core.base.version import VERSION
__version__ = VERSION

class AggregationType(Enum):
    """Types of metric aggregation for rollups."""
    SUM = "sum"
    AVG = "average"
    MIN = "minimum"
    MAX = "maximum"
    COUNT = "count"
    P50 = "percentile_50"
    P95 = "percentile_95"
    P99 = "percentile_99"
