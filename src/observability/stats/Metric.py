#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from .MetricType import MetricType

from dataclasses import dataclass, field
from typing import Dict


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class Metric:
    """A single metric."""
    name: str
    value: float
    metric_type: MetricType
    timestamp: str = ""
    namespace: str = "default"
    tags: Dict[str, str] = field(default_factory=lambda: {})

    # Compatibility: some tests treat history entries as (timestamp, value) tuples.
    def __iter__(self) -> Any:
        yield self.timestamp
        yield self.value

    def __getitem__(self, index: int) -> Any:
        return (self.timestamp, self.value)[index]
