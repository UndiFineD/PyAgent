#!/usr/bin/env python3

"""
ScalingCore logic for fleet expansion.
Pure logic for computing moving averages, resource mapping, and anti-flapping scaling decisions.
"""

from __future__ import annotations

import time
from typing import Dict, List, Optional, Tuple

class ScalingCore:
    """
    Pure logic for handling scaling decisions.
    Supports multi-resource metrics (latency, cpu, mem) and anti-flapping.
    """
    def __init__(self, scale_threshold: float = 5.0, window_size: int = 10, backoff_seconds: int = 30) -> None:
        self.scale_threshold = scale_threshold
        self.window_size = window_size
        self.backoff_seconds = backoff_seconds
        self.load_metrics: Dict[str, Dict[str, List[float]]] = {}
        self.last_scale_event: Dict[str, float] = {}

    def add_metric(self, key: str, value: float, metric_type: str = "latency") -> None:
        """Adds a metric value to the sliding window buffer."""
        if key not in self.load_metrics:
            self.load_metrics[key] = {}
        if metric_type not in self.load_metrics[key]:
            self.load_metrics[key][metric_type] = []
            
        buffer = self.load_metrics[key][metric_type]
        buffer.append(value)
        if len(buffer) > self.window_size:
            buffer.pop(0)

    def calculate_weighted_load(self, key: str) -> float:
        """
        Calculates a weighted average metric score.
        Defaults to latency if other metrics are missing.
        """
        metrics = self.load_metrics.get(key, {})
        if not metrics:
            return 0.0
            
        # Weights: Latency 60%, CPU 30%, MEM 10%
        latency_avg = self.get_avg(key, "latency")
        cpu_avg = self.get_avg(key, "cpu") or 0.0
        mem_avg = self.get_avg(key, "mem") or 0.0
        
        load = (latency_avg * 0.6) + (cpu_avg * 0.3) + (mem_avg * 0.1)
        return load

    def should_scale(self, key: str) -> bool:
        """
        Decision logic for scaling out (adding replicas).
        Includes backoff to prevent flapping.
        """
        load = self.calculate_weighted_load(key)
        
        # Check backoff
        last_event = self.last_scale_event.get(key, 0)
        current_time = time.time()
        
        if (current_time - last_event) < self.backoff_seconds:
            return False
            
        if load > self.scale_threshold:
            self.last_scale_event[key] = current_time
            return True
            
        return False

    def get_avg(self, key: str, metric_type: str = "latency") -> float:
        """Returns the average for a specific metric type."""
        recent = self.load_metrics.get(key, {}).get(metric_type, [])
        return sum(recent) / len(recent) if recent else 0.0

    def get_avg_latency(self, key: str) -> float:
        return self.get_avg(key, "latency")
