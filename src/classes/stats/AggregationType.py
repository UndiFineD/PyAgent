#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from enum import Enum

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
