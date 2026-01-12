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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



import hashlib
import json
import logging
import math
import zlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, TYPE_CHECKING

from .Alert import Alert
from .AlertSeverity import AlertSeverity
from .Metric import Metric
from .MetricSnapshot import MetricSnapshot
from .MetricType import MetricType
from .RetentionPolicy import RetentionPolicy
from .Threshold import Threshold



































if TYPE_CHECKING:
    from .StatsAgent import StatsAgent

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    has_matplotlib = True
except (ImportError, RuntimeError, Exception):
    has_matplotlib = False

class StatsCore:
    """Core logic for statistics processing, separated from the Agent shell."""

    @staticmethod
    def detect_anomaly(
        history: List[Metric],
        value: float,
        threshold_std: float = 2.0
    ) -> Tuple[bool, float]:
        """Detect if a value is anomalous using standard deviation."""
        if len(history) < 2:
            return False, 0.0
            
        values = [m.value for m in history]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std = math.sqrt(variance) if variance > 0 else 0.001
        z_score = abs((value - mean) / std)
        return z_score > threshold_std, z_score

    @staticmethod
    def forecast(history: List[Metric], periods: int = 5) -> List[float]:
        """Simple linear forecasting for a metric."""
        if len(history) < 3:
            return []
        values = [m.value for m in history]
        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        if denominator == 0:
            return [y_mean] * periods
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        return [slope * (n + i) + intercept for i in range(periods)]

    @staticmethod
    def compress_metrics(metrics: List[Metric]) -> bytes:
        """Compress metric history."""
        if not metrics:
            return b''
        data = json.dumps([
            {"value": m.value, "timestamp": m.timestamp, "tags": m.tags}
            for m in metrics
        ])
        return zlib.compress(data.encode("utf-8"))

    @staticmethod
    def visualize_stats(stats: Dict[str, Any]) -> None:
        """Generate CLI graphs for stats visualization."""
        if not has_matplotlib:
            logging.warning("matplotlib not available for visualization")
            return
        labels = list(stats.keys())
        values = list(stats.values())
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.xlabel('Metrics')
        plt.ylabel('Values')
        plt.title('Stats Visualization')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def compare_snapshots(s1: MetricSnapshot, s2: MetricSnapshot) -> Dict[str, Dict[str, Union[float, int]]]:
        """Compare two snapshots."""
        comparison: Dict[str, Dict[str, Union[float, int]]] = {}
        all_keys = set(s1.metrics.keys()) | set(s2.metrics.keys())
        for key in all_keys:
            v1 = s1.metrics.get(key, 0.0)
            v2 = s2.metrics.get(key, 0.0)
            comparison[key] = {
                "snapshot1": v1,
                "snapshot2": v2,
                "difference": v2 - v1,
                "percentage_change": ((v2 - v1) / v1 * 100) if v1 != 0 else 0
            }
        return comparison

    @staticmethod
    def apply_retention(
        metrics_dict: Dict[str, List[Metric]], 
        policies: Dict[str, RetentionPolicy]
    ) -> int:
        """Apply retention policies to metrics."""
        removed = 0
        now = datetime.now()
        for key, metrics in list(metrics_dict.items()):
            namespace = metrics[0].namespace if metrics else "default"
            policy = policies.get(key) or policies.get(namespace)
            if not policy:
                continue
            
            if policy.max_age_days > 0:
                cutoff = now - timedelta(days=policy.max_age_days)
                orig = len(metrics)
                metrics_dict[key] = [m for m in metrics if datetime.fromisoformat(m.timestamp) > cutoff]
                removed += orig - len(metrics_dict[key])
                
            if policy.max_points > 0 and len(metrics_dict[key]) > policy.max_points:
                removed += len(metrics_dict[key]) - policy.max_points
                metrics_dict[key] = metrics_dict[key][-policy.max_points:]
        return removed
