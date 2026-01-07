#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .AggregationType import AggregationType

from dataclasses import dataclass
from typing import List

@dataclass
class RollupConfig:
    """Configuration for metric rollups."""
    name: str
    source_metrics: List[str]
    aggregation: AggregationType
    interval_minutes: int = 60
    keep_raw: bool = True
