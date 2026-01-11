#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from .TestTimer import TestTimer

from typing import Callable, Dict, List

class Benchmarker:
    """Runs benchmarks and collects statistics."""

    def __init__(self) -> None:
        """Initialize benchmarker."""
        self.timings: List[float] = []

    def run(self, fn: Callable[[], None], iterations: int = 5) -> Dict[str, float]:
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
            "iterations": iterations
        }
