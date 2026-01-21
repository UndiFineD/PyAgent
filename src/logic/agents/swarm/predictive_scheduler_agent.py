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
from src.core.base.lifecycle.version import VERSION
import time
import logging
from typing import Any
from src.core.base.lifecycle.base_agent import BaseAgent

__version__ = VERSION


class PredictiveSchedulerAgent(BaseAgent):
    """
    Phase 53: Predictive Resource Forecasting.
    Uses historical telemetry to forecast future token usage and compute needs.
    Phase 130: Neural Feedback Loop integration for adaptive weight balancing.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.usage_history: list[dict[str, Any]] = []
        self.prediction_window = 10  # Number of steps to look ahead
        self.weights: dict[str, float] = {
            "avg": 0.5,
            "trend": 0.5,
        }  # Initial neural weights
        self.learning_rate = 0.05

    def ingest_metrics(
        self, metrics: list[Any], actual_outcome: float | None = None
    ) -> None:
        """
        Ingests recent agent metrics for analysis.
        Phase 130: Adjusts weights using simple backpropagation logic if actual outcome is provided.
        """
        for m in metrics:
            self.usage_history.append(
                {
                    "timestamp": getattr(m, "timestamp", time.time()),
                    "tokens": getattr(m, "token_count", 0),
                    "agent": getattr(m, "agent_name", "unknown"),
                }
            )

        if actual_outcome is not None and len(self.usage_history) > 1:
            # Neural Feedback Loop: Adjust weights based on last prediction error
            error = actual_outcome - self.forecast_usage()["forecasted_tokens"]
            logging.info(f"Neural Feedback: Adjusting weights (error: {error:.2f})")

            # Simple gradient descent on weights
            self.weights["trend"] += self.learning_rate * (
                error / 1000.0
            )  # Normalized update
            self.weights["avg"] = 1.0 - self.weights["trend"]

            # Clamp weights
            self.weights["trend"] = max(0.1, min(0.9, self.weights["trend"]))
            self.weights["avg"] = max(0.1, min(0.9, self.weights["avg"]))

        # Keep history manageable
        if len(self.usage_history) > 1000:
            self.usage_history = self.usage_history[-1000:]

    def forecast_usage(self) -> dict[str, Any]:
        """
        Forecasts usage for the next cycle.
        Phase 130: Weighted combination of average and trend based on neural feedback.
        """
        if len(self.usage_history) < 5:
            return {
                "forecasted_tokens": 0,
                "confidence": 0.1,
                "action": "collect_more_data",
            }

        recent_usage = [h["tokens"] for h in self.usage_history[-5:]]
        avg_usage = sum(recent_usage) / len(recent_usage)

        # Trend analysis
        trend_val = recent_usage[-1] - recent_usage[0]

        # Weighted forecast
        forecast = (avg_usage * self.weights["avg"]) + (
            max(0, avg_usage + trend_val) * self.weights["trend"]
        )

        return {
            "forecasted_tokens": forecast,
            "confidence": 0.8 if len(self.usage_history) > 20 else 0.4,
            "provisioning_recommendation": "scale_up" if forecast > 1000 else "stable",
            "weights": self.weights,
        }

    def evaluate_scaling_needs(self, current_nodes: int) -> dict[str, Any]:
        """Recommends scaling actions based on predicted load."""
        forecast = self.forecast_usage()
        needed_nodes = current_nodes

        if forecast["forecasted_tokens"] > 5000:
            needed_nodes += 2
        elif forecast["forecasted_tokens"] > 2000:
            needed_nodes += 1

        return {
            "current_nodes": current_nodes,
            "recommended_nodes": needed_nodes,
            "trigger_scaling": needed_nodes > current_nodes,
        }
