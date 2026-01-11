#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from .AggregationType import AggregationType

from dataclasses import dataclass
from typing import List


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class RollupConfig:
    """Configuration for metric rollups."""
    name: str
    source_metrics: List[str]
    aggregation: AggregationType
    interval_minutes: int = 60
    keep_raw: bool = True
