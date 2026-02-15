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

"""
Reading the repository for the prediction_engine.py file so its exact contents can be included in the FILE CONTENT SUMMARY.

Reading prediction_engine.py to include its exact contents in the FILE CONTENT SUMMARY.

Prediction Engine - Forecasting & Change Detection

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate StatsChangeDetector to monitor numeric metrics and trigger listeners when metrics change beyond a relative threshold.
- Instantiate StatsForecaster to maintain simple history-based forecasts, request point predictions, multi-step predictions, and basic confidence intervals; optionally uses rust_core for optimized confidence computations.

WHAT IT DOES:
- Provides StatsChangeDetector:
  - Tracks previous metric values and detects relative changes against a configurable threshold (or threshold_percent).
  - Records change events (old/new values and percent change), stores them, and notifies registered listeners safely (exceptions suppressed).
  - Exposes get_changes() to retrieve accumulated changes and on_change() to register callbacks.
- Provides StatsForecaster:
  - Maintains a sliding history and computes next-value prediction as a simple moving average over a configurable window.
  - Produces a basic confidence interval around the next prediction (±10% by default).
  - Predicts multi-step futures using a last-difference (delta) extrapolation, with fallback delta computed from a window when recent delta is zero.
  - Offers predict_with_confidence that prefers a rust_core implementation (if available) and otherwise computes predictions with a simple margin based on sample std/mean.

WHAT IT SHOULD DO BETTER:
- Use statistically sound forecasting methods (ARIMA, exponential smoothing, Prophet, or lightweight ML models) rather than naive delta extrapolation and fixed-percentage margins.
- Improve change detection by supporting absolute thresholds, adaptive thresholds, seasonal/daily baselining, and robust outlier handling (e.g., median-based or rolling MAD).
- Make detection and forecasting resilient to zero and near-zero baselines (avoid division-by-zero semantics and misleading percent-change).
- Add better observability: structured logging, metric tagging, timestamps for change events, and rate-limiting or batching listener notifications.
- Expose configuration for confidence calculation (e.g., confidence levels, windowing strategy) and add unit tests covering edge cases (empty history, single-point history, non-finite values).
- Improve concurrency and persistence: allow durable storage of previous_values/history, thread-safe or async-safe APIs, and backpressure for high-frequency metrics.
- Hardening: validate inputs, raise informative exceptions, and avoid suppressing all listener exceptions silently (or log them).

FILE CONTENT SUMMARY:
Prediction engine.py module.
"""
# Forecasting and change detection engine.

from __future__ import annotations

import contextlib
import logging
import math
from typing import Any, Callable

logger = logging.getLogger(__name__)


class StatsChangeDetector:
    """Detects changes in metric values."""

    def __init__(self, threshold: float = 0.1, threshold_percent: float | None = None) -> None:
        if threshold_percent is not None:
            threshold = float(threshold_percent) / 100.0
        self.threshold = float(threshold)
        self.previous_values: dict[str, float] = {}
        self._changes: list[dict[str, Any]] = []
        self._listeners: list[Callable[[dict[str, Any]], None]] = []

    def detect_change(self, metric: str, value: float) -> bool:
        if metric not in self.previous_values:
            self.previous_values[metric] = value
            return False
        prev = self.previous_values[metric]
        if prev == 0:
            change = abs(value - prev) > 0
        else:
            change = abs((value - prev) / prev) > self.threshold
        self.previous_values[metric] = value
        return change

    def record(self, metric: str, value: float) -> bool:
        prev = self.previous_values.get(metric)
        changed = self.detect_change(metric, float(value))

        if changed:
            old_val = 0.0 if prev is None else float(prev)
            new_val = float(value)
            change_percent = (
                abs((new_val - old_val) / old_val) * 100.0 if old_val != 0.0 else (100.0 if new_val != 0.0 else 0.0)
            )

            change_info = {
                "metric": metric,
                "old": old_val,
                "new": new_val,
                "change_percent": change_percent,
            }
            self._changes.append(change_info)
            for listener in list(self._listeners):
                with contextlib.suppress(Exception):
                    listener(change_info)
        return changed

    def on_change(self, callback: Callable[[dict[str, Any]], None]) -> None:
        self._listeners.append(callback)

    def get_changes(self) -> list[dict[str, Any]]:
        return list(self._changes)


class StatsForecaster:
    """Forecasts future metric values."""

    def __init__(self, window_size: int = 10) -> None:
        self.window_size = window_size
        self.history: list[float] = []

    def add_value(self, value: float) -> None:
        self.history.append(value)

    def predict_next(self) -> float:
        if not self.history:
            return 0.0
        return sum(self.history[-self.window_size :]) / min(len(self.history), self.window_size)

    def confidence_interval(self) -> tuple[float, float]:
        prediction = self.predict_next()
        margin = prediction * 0.1
        return (prediction - margin, prediction + margin)

    def predict(self, historical: list[float], periods: int = 3) -> list[float]:
        if periods <= 0 or not historical:
            return []
        if len(historical) == 1:
            return [float(historical[0])] * periods
        last, prev = float(historical[-1]), float(historical[-2])
        delta = last - prev
        if delta == 0.0:
            window = [float(v) for v in historical[-min(len(historical), self.window_size) :]]
            delta = (window[-1] - window[0]) / max(1, (len(window) - 1))
        return [last + delta * (i + 1) for i in range(periods)]

    def predict_with_confidence(self, historical: list[float], periods: int = 2) -> dict[str, list[float]]:
        # Rust optimization
        with contextlib.suppress(ImportError, AttributeError, Exception):
            import rust_core as rc

            preds, lower, upper = rc.predict_with_confidence_rust([float(v) for v in historical], periods)
            return {
                "predictions": preds,
                "confidence_lower": lower,
                "confidence_upper": upper,
            }

        # Python fallback
        preds = self.predict(historical, periods=periods)
        if not historical:
            margin = 0.0
        else:
            values = [float(v) for v in historical]
            mean = sum(values) / len(values)
            var = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(var)
            margin = max(std, abs(mean) * 0.05)
        return {
            "predictions": preds,
            "confidence_lower": [p - margin for p in preds],
            "confidence_upper": [p + margin for p in preds],
        }
"""
# Forecasting and change detection engine.

from __future__ import annotations

import contextlib
import logging
import math
from typing import Any, Callable

logger = logging.getLogger(__name__)


class StatsChangeDetector:
    """Detects changes in metric values."""

    def __init__(self, threshold: float = 0.1, threshold_percent: float | None = None) -> None:
        if threshold_percent is not None:
            threshold = float(threshold_percent) / 100.0
        self.threshold = float(threshold)
        self.previous_values: dict[str, float] = {}
        self._changes: list[dict[str, Any]] = []
        self._listeners: list[Callable[[dict[str, Any]], None]] = []

    def detect_change(self, metric: str, value: float) -> bool:
        if metric not in self.previous_values:
            self.previous_values[metric] = value
            return False
        prev = self.previous_values[metric]
        if prev == 0:
            change = abs(value - prev) > 0
        else:
            change = abs((value - prev) / prev) > self.threshold
        self.previous_values[metric] = value
        return change

    def record(self, metric: str, value: float) -> bool:
        prev = self.previous_values.get(metric)
        changed = self.detect_change(metric, float(value))

        if changed:
            old_val = 0.0 if prev is None else float(prev)
            new_val = float(value)
            change_percent = (
                abs((new_val - old_val) / old_val) * 100.0 if old_val != 0.0 else (100.0 if new_val != 0.0 else 0.0)
            )

            change_info = {
                "metric": metric,
                "old": old_val,
                "new": new_val,
                "change_percent": change_percent,
            }
            self._changes.append(change_info)
            for listener in list(self._listeners):
                with contextlib.suppress(Exception):
                    listener(change_info)
        return changed

    def on_change(self, callback: Callable[[dict[str, Any]], None]) -> None:
        self._listeners.append(callback)

    def get_changes(self) -> list[dict[str, Any]]:
        return list(self._changes)


class StatsForecaster:
    """Forecasts future metric values."""

    def __init__(self, window_size: int = 10) -> None:
        self.window_size = window_size
        self.history: list[float] = []

    def add_value(self, value: float) -> None:
        self.history.append(value)

    def predict_next(self) -> float:
        if not self.history:
            return 0.0
        return sum(self.history[-self.window_size :]) / min(len(self.history), self.window_size)

    def confidence_interval(self) -> tuple[float, float]:
        prediction = self.predict_next()
        margin = prediction * 0.1
        return (prediction - margin, prediction + margin)

    def predict(self, historical: list[float], periods: int = 3) -> list[float]:
        if periods <= 0 or not historical:
            return []
        if len(historical) == 1:
            return [float(historical[0])] * periods
        last, prev = float(historical[-1]), float(historical[-2])
        delta = last - prev
        if delta == 0.0:
            window = [float(v) for v in historical[-min(len(historical), self.window_size) :]]
            delta = (window[-1] - window[0]) / max(1, (len(window) - 1))
        return [last + delta * (i + 1) for i in range(periods)]

    def predict_with_confidence(self, historical: list[float], periods: int = 2) -> dict[str, list[float]]:
        # Rust optimization
        with contextlib.suppress(ImportError, AttributeError, Exception):
            import rust_core as rc

            preds, lower, upper = rc.predict_with_confidence_rust([float(v) for v in historical], periods)
            return {
                "predictions": preds,
                "confidence_lower": lower,
                "confidence_upper": upper,
            }

        # Python fallback
        preds = self.predict(historical, periods=periods)
        if not historical:
            margin = 0.0
        else:
            values = [float(v) for v in historical]
            mean = sum(values) / len(values)
            var = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(var)
            margin = max(std, abs(mean) * 0.05)
        return {
            "predictions": preds,
            "confidence_lower": [p - margin for p in preds],
            "confidence_upper": [p + margin for p in preds],
        }
