#!/usr/bin/env python3
"""PerformanceTracker shim for pytest collection.

Provides a minimal `PerformanceTracker` to satisfy imports during iterative fixes.
"""


class PerformanceTracker:
    def __init__(self, *_, **__):
        self.metrics = {}

    def record(self, name, value):
        self.metrics.setdefault(name, []).append(value)

    def summary(self):
        return {k: (sum(v) / len(v) if v else 0) for k, v in self.metrics.items()}


__all__ = ["PerformanceTracker"]
