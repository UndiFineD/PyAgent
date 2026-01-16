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

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from .ReportMetric import ReportMetric
from typing import Any
import logging

__version__ = VERSION


class MetricsCollector:
    """Collector for custom report metrics and KPIs.
    Tracks and calculates metrics across reports.
    Attributes:
        metrics: Collected metrics by file.
    Example:
        collector=MetricsCollector()
        collector.record("file.py", "issues_count", 5)
        summary=collector.get_summary()
    """

    def __init__(self) -> None:
        """Initialize metrics collector."""

        self.metrics: dict[str, list[ReportMetric]] = {}
        logging.debug("MetricsCollector initialized")

    def record(
        self,
        file_path: str,
        name: str,
        value: float,
        unit: str = "",
        threshold: float | None = None,
    ) -> ReportMetric:
        """Record a metric.
        Args:
            file_path: File being measured.
            name: Metric name.
            value: Metric value.
            unit: Unit of measurement.
            threshold: Alert threshold.
        Returns:
            Created metric.
        """

        metric = ReportMetric(name=name, value=value, unit=unit, threshold=threshold)
        if file_path not in self.metrics:
            self.metrics[file_path] = []
        self.metrics[file_path].append(metric)
        return metric

    def get_metrics(self, file_path: str) -> list[ReportMetric]:
        """Get metrics for a file.
        Args:
            file_path: File path.
        Returns:
            List of metrics.
        """

        return self.metrics.get(file_path, [])

    def get_summary(self) -> dict[str, Any]:
        """Get summary of all metrics.
        Returns:
            Summary dictionary.
        """

        total_files = len(self.metrics)
        total_metrics = sum(len(m) for m in self.metrics.values())
        # Calculate averages by metric name
        averages: dict[str, list[float]] = {}
        for metrics in self.metrics.values():
            for metric in metrics:
                if metric.name not in averages:
                    averages[metric.name] = []
                averages[metric.name].append(metric.value)
        avg_summary = {
            name: sum(vals) / len(vals) if vals else 0
            for name, vals in averages.items()
        }
        return {
            "total_files": total_files,
            "total_metrics": total_metrics,
            "averages": avg_summary,
        }
