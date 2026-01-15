#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .PerformanceMetric import PerformanceMetric
from .PerformanceMetricType import PerformanceMetricType
from contextlib import contextmanager
from typing import Any
from collections.abc import Iterator
import time

__version__ = VERSION




class PerformanceTracker:
    """Tracks test execution performance.

    Example:
        tracker=PerformanceTracker()
        with tracker.track("test_function"):
            run_test()
        metrics=tracker.get_metrics()
    """

    def __init__(self) -> None:
        """Initialize performance tracker."""
        self._metrics: list[PerformanceMetric] = []
        self._start_times: dict[str, float] = {}

    @contextmanager
    def track(self, test_name: str) -> Iterator[None]:
        """Track execution time for a test.

        Args:
            test_name: Name of the test.
        """
        start = time.time()
        self._start_times[test_name] = start
        try:
            yield
        finally:
            duration = (time.time() - start) * 1000  # ms
            metric = PerformanceMetric(
                metric_type=PerformanceMetricType.EXECUTION_TIME,
                value=duration,
                unit="ms",
                test_name=test_name,
            )
            self._metrics.append(metric)
            del self._start_times[test_name]

    def record_metric(
        self,
        test_name: str,
        metric_type: PerformanceMetricType,
        value: float,
        unit: str,
    ) -> None:
        """Record a performance metric.

        Args:
            test_name: Test name.
            metric_type: Type of metric.
            value: Metric value.
            unit: Unit of measurement.
        """
        metric = PerformanceMetric(
            metric_type=metric_type,
            value=value,
            unit=unit,
            test_name=test_name,
        )
        self._metrics.append(metric)

    def get_metrics(self) -> list[PerformanceMetric]:
        """Get all recorded metrics."""
        return list(self._metrics)

    def get_summary(self) -> dict[str, Any]:
        """Get summary of performance metrics."""
        if not self._metrics:
            return {}

        execution_times = [
            m.value for m in self._metrics
            if m.metric_type == PerformanceMetricType.EXECUTION_TIME
        ]

        return {
            "total_metrics": len(self._metrics),
            "avg_execution_time_ms": (
                sum(execution_times) / len(execution_times)
                if execution_times else 0
            ),
            "max_execution_time_ms": max(execution_times) if execution_times else 0,
            "min_execution_time_ms": min(execution_times) if execution_times else 0,
        }

    def clear(self) -> None:
        """Clear all recorded metrics."""
        self._metrics.clear()
        self._start_times.clear()
