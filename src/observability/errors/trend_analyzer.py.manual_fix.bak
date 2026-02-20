#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
TrendAnalyzer - Error trend analysis and prediction

"""

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
    from trend_analyzer import TrendAnalyzer
    ta = TrendAnalyzer()
    ta.record("errors_per_minute", 5.0)
    analysis = ta.analyze("errors_per_minute")
    preds = ta.predict("errors_per_minute", periods=3)

WHAT IT DOES:
    Provides a lightweight in-memory collector for numeric metric points,
    computes a simple recent-average change to set a TrendDirection
    (INCREASING / DECREASING / STABLE), and produces short-term linear
    predictions based on average change.

WHAT IT SHOULD DO BETTER:
    - Persist timestamps as datetime objects (not ISO strings) and
      normalize time deltas in prediction.
    - Use configurable windowing, weighting (e.g., EMA) and robust
      outlier handling instead of a fixed recent slice and fixed ±0.1
      thresholds.
    - Add input validation, concurrency protection, configurable
      thresholds, error handling, and unit-tested prediction accuracy;
      consider statistical or ML-based forecasting for better long-range
      predictions.
"""
try:
    from datetime import datetime
except ImportError:
    from datetime import datetime


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .trend_data import TrendData
except ImportError:
    from .trend_data import TrendData

try:
    from .trend_direction import TrendDirection
except ImportError:
    from .trend_direction import TrendDirection


__version__ = VERSION


class TrendAnalyzer:
"""
Analyzes error trends over time.
    Provides trend analysis with predictions based on
    historical error data.

    Attributes:
        data_points: Map of metric names to TrendData.
"""
def __init__(self) -> None:
"""
Initialize the trend analyzer.""
self.data_points: dict[str, TrendData] = {}


    def record(self, metric: str, value: float) -> None:
"""
Record a data point.
        Args:
            metric: Metric name.
            value: Value to record.
"""
if metric not in self.data_points:
            self.data_points[metric] = TrendData(metric_name=metric)
        data = self.data_points[metric]
        data.values.append(value)
        data.timestamps.append(datetime.now().isoformat())


    def analyze(self, metric: str) -> TrendData:
"""
Analyze trend for a metric.
        
        Args:
            metric: Metric name.

        Returns:
            TrendData with direction and prediction.
"""
if metric not in self.data_points:
            return TrendData(metric_name=metric)
        data = self.data_points[metric]
        if len(data.values) < 2:
            data.direction = TrendDirection.STABLE
            return data
        # Calculate direction
        recent = data.values[-5:] if len(data.values) >= 5 else data.values
        avg_change = sum(recent[i] - recent[i - 1] for i in range(1, len(recent))) / (len(recent) - 1)
        if avg_change > 0.1:
            data.direction = TrendDirection.INCREASING
        elif avg_change < -0.1:
            data.direction = TrendDirection.DECREASING
        else:
            data.direction = TrendDirection.STABLE
        # Simple prediction
        data.prediction = data.values[-1] + avg_change
        return data


    def predict(self, metric: str, periods: int = 1) -> list[float]:
"""
Predict future values.

        Args:
            metric: Metric name.
            periods: Number of periods to predict.

        Returns:
            List of predicted values.
        ""
data = self.analyze(metric)
        if not data.values:
            return []
        predictions: list[float] = []
        last_value = data.values[-1]
        avg_change = 0.0
        if len(data.values) >= 2:
            changes = [data.values[i] - data.values[i - 1] for i in range(1, len(data.values))]
            avg_change = sum(changes) / len(changes)
        for i in range(periods):
            predictions.append(last_value + avg_change * (i + 1))
        return predictions
