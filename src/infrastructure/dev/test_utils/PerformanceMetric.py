#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from .PerformanceMetricType import PerformanceMetricType

from dataclasses import dataclass, field
import time

@dataclass
class PerformanceMetric:
    """Performance metric from test execution.

    Attributes:
        metric_type: Type of metric.
        value: Metric value.
        unit: Unit of measurement.
        test_name: Associated test.
        timestamp: When captured.
    """

    metric_type: PerformanceMetricType
    value: float
    unit: str
    test_name: str
    timestamp: float = field(default_factory=time.time)
