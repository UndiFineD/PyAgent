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


"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from .TestTimer import TestTimer
from collections.abc import Callable

__version__ = VERSION


class Benchmarker:
    """Runs benchmarks and collects statistics."""

    def __init__(self) -> None:
        """Initialize benchmarker."""
        self.timings: list[float] = []

    def run(self, fn: Callable[[], None], iterations: int = 5) -> dict[str, float]:
        """Run a function multiple times and collect timing statistics.

        Args:
            fn: Function to benchmark.
            iterations: Number of iterations.

        Returns:
            Statistics dictionary with min/max/mean in both seconds and milliseconds, plus iterations.
        """
        self.timings = []
        for _ in range(iterations):
            timer = TestTimer()
            timer.start()
            fn()
            elapsed = timer.stop()
            self.timings.append(elapsed)

        mean_seconds = sum(self.timings) / len(self.timings)
        return {
            "min": min(self.timings),
            "max": max(self.timings),
            "mean": mean_seconds,
            "median": sorted(self.timings)[len(self.timings) // 2],
            "min_ms": min(self.timings) * 1000,
            "max_ms": max(self.timings) * 1000,
            "average_ms": mean_seconds * 1000,
            "iterations": iterations,
        }
