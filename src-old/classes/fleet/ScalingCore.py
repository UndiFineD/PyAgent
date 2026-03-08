#!/usr/bin/env python3

"""
ScalingCore logic for fleet expansion.
Pure logic for computing moving averages and scaling decisions.
"""

from typing import Dict, List, Optional

class ScalingCore:
    def __init__(self, scale_threshold: float = 5.0, window_size: int = 10) -> None:
        self.scale_threshold = scale_threshold
        self.window_size = window_size
        self.load_metrics: Dict[str, List[float]] = {}

    def add_metric(self, key: str, value: float) -> None:
        if key not in self.load_metrics:
            self.load_metrics[key] = []
        self.load_metrics[key].append(value)
        if len(self.load_metrics[key]) > self.window_size:
            self.load_metrics[key].pop(0)

    def should_scale(self, key: str) -> bool:
        recent = self.load_metrics.get(key, [])
        if not recent:
            return False
        avg = sum(recent) / len(recent)
        return avg > self.scale_threshold

    def get_avg_latency(self, key: str) -> float:
        recent = self.load_metrics.get(key, [])
        return sum(recent) / len(recent) if recent else 0.0
