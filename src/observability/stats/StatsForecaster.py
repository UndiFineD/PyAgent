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


"""Auto-extracted class from agent_stats.py"""



from typing import Dict, List, Tuple
import math



































class StatsForecaster:
    """Forecasts future metric values."""
    def __init__(self, window_size: int = 10) -> None:
        self.window_size = window_size
        self.history: List[float] = []

    def add_value(self, value: float) -> None:
        """Add a value to history."""
        self.history.append(value)

    def predict_next(self) -> float:
        """Predict next value using simple average."""
        if not self.history:
            return 0.0
        return sum(self.history[-self.window_size:]) / min(len(self.history), self.window_size)

    def confidence_interval(self) -> Tuple[float, float]:
        """Return confidence interval for prediction."""
        prediction = self.predict_next()
        margin = prediction * 0.1  # 10% margin
        return (prediction - margin, prediction + margin)

    def predict(self, historical: List[float], periods: int = 3) -> List[float]:
        """Predict future values from a historical series."""
        if periods <= 0:
            return []
        if not historical:
            return []
        if len(historical) == 1:
            return [float(historical[0])] * periods

        last = float(historical[-1])
        prev = float(historical[-2])
        delta = last - prev
        if delta == 0.0:
            # Fall back to average slope over the last window.
            window = [float(v) for v in historical[-min(len(historical), self.window_size):]]
            delta = (window[-1] - window[0]) / max(1, (len(window) - 1))
        return [last + delta * (i + 1) for i in range(periods)]

    def predict_with_confidence(self, historical: List[float], periods: int = 2) -> Dict[str, List[float]]:
        """Predict future values and include naive confidence intervals."""
        preds = self.predict(historical, periods=periods)
        if not historical:
            margin = 0.0
        else:
            values = [float(v) for v in historical]
            mean = sum(values) / len(values)
            var = sum((v - mean) ** 2 for v in values) / len(values)
            std = math.sqrt(var)
            margin = max(std, abs(mean) * 0.05)

        lower = [p - margin for p in preds]
        upper = [p + margin for p in preds]
        return {
            "predictions": preds,
            "confidence_lower": lower,
            "confidence_upper": upper,
        }
