#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from .RetentionPolicy import RetentionPolicy

from typing import Any, Dict, List


































from src.core.base.version import VERSION
__version__ = VERSION

class RetentionEnforcer:
    """Enforces retention policies on metrics."""
    def __init__(self) -> None:
        self.policies: Dict[str, RetentionPolicy] = {}
        self.data: Dict[str, List[Dict[str, Any]]] = {}

    def set_policy(self, metric_pattern: str, policy: RetentionPolicy) -> None:
        """Set a retention policy for metrics matching pattern."""
        self.policies[metric_pattern] = policy

    def add_policy(self, metric: str, max_age_days: int, max_points: int) -> None:
        """Add a retention policy (backward compat)."""
        policy = RetentionPolicy(name=metric, retention_days=max_age_days, max_points=max_points)
        self.policies[metric] = policy

    def add_data(self, metric_name: str, timestamp: float, value: Any) -> None:
        """Add data point to a metric."""
        if metric_name not in self.data:
            self.data[metric_name] = []
        self.data[metric_name].append({"timestamp": timestamp, "value": value})

    def enforce(self) -> int:
        """Enforce retention policies, return count of removed items."""
        from datetime import datetime
        removed_count = 0
        now = datetime.now().timestamp()
        for metric_pattern, policy in self.policies.items():
            # Find matching metrics
            matching_metrics = [m for m in self.data.keys() if metric_pattern.replace("*", "") in m]
            for metric in matching_metrics:
                if metric in self.data:
                    original_count = len(self.data[metric])
                    # Apply retention days policy
                    if policy.retention_days > 0:
                        cutoff_time = now - (policy.retention_days * 86400)  # days to seconds
                        self.data[metric] = [
                            d for d in self.data[metric]
                            if d["timestamp"] > cutoff_time
                        ]
                    removed_count += original_count - len(self.data[metric])
        return removed_count

    def apply_policies(self, metrics: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
        """Apply retention policies to metrics."""
        result: Dict[str, List[Any]] = {}
        for metric, values in metrics.items():
            policy = self.policies.get(metric)
            if policy:
                if hasattr(policy, 'max_points') and policy.max_points > 0:
                    result[metric] = values[-policy.max_points:]
                else:
                    result[metric] = values
            else:
                result[metric] = values
        return result
