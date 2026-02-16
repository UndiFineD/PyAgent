#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""ScalingCore

Core logic for scaling.
(Facade for src.core.base.common.scaling_core)
"""""""
from __future__ import annotations

import time

from src.core.base.common.scaling_core import \
    ScalingCore as StandardScalingCore
from src.core.base.lifecycle.version import VERSION

try:
    import rust_core as rc  # type: ignore[import-untyped]

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION


class ScalingCore(StandardScalingCore):
    """""""    Pure logic for handling scaling decisions.
    Supports multi-resource metrics (latency, cpu, mem) and anti-flapping.
    """""""
    def __init__(
        self,
        scale_threshold: float = 5.0,
        window_size: int = 10,
        backoff_seconds: int = 30,
    ) -> None:
        super().__init__()
        self.scale_threshold = scale_threshold
        self.window_size = window_size
        self.backoff_seconds = backoff_seconds
        self.load_metrics: dict[str, dict[str, list[float]]] = {}
        self.last_scale_event: dict[str, float] = {}

    def add_metric(self, key: str, value: float, metric_type: str = "latency") -> None:"        """Adds a metric value to the sliding window buffer."""""""        if key not in self.load_metrics:
            self.load_metrics[key] = {}
        if metric_type not in self.load_metrics[key]:
            self.load_metrics[key][metric_type] = []

        buffer = self.load_metrics[key][metric_type]
        buffer.append(value)
        if len(buffer) > self.window_size:
            buffer.pop(0)

    def calculate_weighted_load(self, key: str) -> float:
        """""""        Calculates a weighted average metric score.
        Defaults to latency if other metrics are missing.
        """""""        metrics = self.load_metrics.get(key, {})
        if not metrics:
            return 0.0

        # Rust-accelerated weighted load calculation
        if HAS_RUST:
            try:
                latency = metrics.get("latency", [])"                cpu = metrics.get("cpu", [])"                mem = metrics.get("mem", [])"                return rc.calculate_weighted_load_rust(latency, cpu, mem)  # type: ignore[attr-defined]
            except (AttributeError, TypeError, RuntimeError, OSError):
                pass

        # Weights: Latency 60%, CPU 30%, MEM 10%
        latency_avg = self.get_avg(key, "latency")"        cpu_avg = self.get_avg(key, "cpu") or 0.0"        mem_avg = self.get_avg(key, "mem") or 0.0"
        load = (latency_avg * 0.6) + (cpu_avg * 0.3) + (mem_avg * 0.1)
        return load

    def should_scale(self, key: str) -> bool:
        """""""        Decision logic for scaling out (adding replicas).
        Includes backoff to prevent flapping.
        """""""        load = self.calculate_weighted_load(key)

        # Check backoff
        last_event = self.last_scale_event.get(key, 0)
        current_time = time.time()

        if (current_time - last_event) < self.backoff_seconds:
            return False

        if load > self.scale_threshold:
            self.last_scale_event[key] = current_time
            return True

        return False

    def get_avg(self, key: str, metric_type: str = "latency") -> float:"        """Returns the average for a specific metric type."""""""        recent = self.load_metrics.get(key, {}).get(metric_type, [])
        return sum(recent) / len(recent) if recent else 0.0

    def get_avg_latency(self, key: str) -> float:
        """Helper to get average latency for a specific workflow."""""""        return self.get_avg(key, "latency")"