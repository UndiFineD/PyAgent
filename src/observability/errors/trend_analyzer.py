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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .trend_data import TrendData
from .trend_direction import TrendDirection
from datetime import datetime

__version__ = VERSION


class TrendAnalyzer:
    """Analyzes error trends over time.

    Provides trend analysis with predictions based on
    historical error data.

    Attributes:
        data_points: Map of metric names to TrendData.
    """

    def __init__(self) -> None:
        """Initialize the trend analyzer."""
        self.data_points: dict[str, TrendData] = {}

    def record(self, metric: str, value: float) -> None:
        """Record a data point.

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
        """Analyze trend for a metric.

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
        avg_change = sum(recent[i] - recent[i - 1] for i in range(1, len(recent))) / (
            len(recent) - 1
        )
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
        """Predict future values.

        Args:
            metric: Metric name.
            periods: Number of periods to predict.

        Returns:
            List of predicted values.
        """
        data = self.analyze(metric)
        if not data.values:
            return []
        predictions: list[float] = []
        last_value = data.values[-1]
        avg_change = 0.0
        if len(data.values) >= 2:
            changes = [
                data.values[i] - data.values[i - 1] for i in range(1, len(data.values))
            ]
            avg_change = sum(changes) / len(changes)
        for i in range(periods):
            predictions.append(last_value + avg_change * (i + 1))
        return predictions
