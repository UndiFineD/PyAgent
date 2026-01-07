#!/usr/bin/env python3

"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

from .ReportMetric import ReportMetric

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast
import ast
import hashlib
import json
import logging
import re
import sys
import time

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

        self.metrics: Dict[str, List[ReportMetric]] = {}
        logging.debug("MetricsCollector initialized")

    def record(
        self,
        file_path: str,
        name: str,
        value: float,
        unit: str = "",
        threshold: Optional[float] = None
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

        metric = ReportMetric(
            name=name,
            value=value,
            unit=unit,
            threshold=threshold
        )
        if file_path not in self.metrics:
            self.metrics[file_path] = []
        self.metrics[file_path].append(metric)
        return metric

    def get_metrics(self, file_path: str) -> List[ReportMetric]:
        """Get metrics for a file.
        Args:
            file_path: File path.
        Returns:
            List of metrics.
        """

        return self.metrics.get(file_path, [])

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics.
        Returns:
            Summary dictionary.
        """

        total_files = len(self.metrics)
        total_metrics = sum(len(m) for m in self.metrics.values())
        # Calculate averages by metric name
        averages: Dict[str, List[float]] = {}
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
            "averages": avg_summary
        }
