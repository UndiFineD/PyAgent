#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Logic for thresholds, alerting, and retention enforcement.

from __future__ import annotations
import logging
from datetime import datetime
from typing import Any, Dict, List
from .metrics import Alert, AlertSeverity, RetentionPolicy, Threshold

logger = logging.getLogger(__name__)

class ThresholdAlertManager:
    """Manages threshold checking and alert emission."""
    def __init__(self) -> None:
        self.thresholds: Dict[str, List[Threshold]] = {}
        self.alerts: List[Alert] = []

    def set_threshold(self, name:
        str, threshold: Threshold) -> None:
        if name not in self.thresholds:
            self.thresholds[name] = []
        self.thresholds[name].append(threshold)

    def check(self, metric_name:
        str, value: float) -> List[Alert]:
        triggered = []
        for t in self.thresholds.get(metric_name, []):
            is_breach = False
            if t.max_value is not None and value > t.max_value:
                is_breach = True
            if t.min_value is not None and value < t.min_value:
                is_breach = True
            
            if is_breach:
                alert = Alert(
                    id=f"{metric_name}_{datetime.now().timestamp()}",
                    metric_name=metric_name,
                    current_value=value,
                    threshold_value=t.max_value if t.max_value is not None else t.min_value, # type: ignore
                    severity=t.severity or AlertSeverity.MEDIUM,
                    message=t.message or f"Threshold breach for {metric_name}",
                    timestamp=datetime.now().isoformat()
                )
                self.alerts.append(alert)
                triggered.append(alert)
        return triggered

class RetentionEnforcer:
    """Enforces retention policies on metrics."""
    def __init__(self) -> None:
        self.policies: Dict[str, RetentionPolicy] = {}
        self.data: Dict[str, List[Dict[str, Any]]] = {}

    def set_policy(self, pattern:
        str, policy: RetentionPolicy) -> None:
        self.policies[pattern] = policy

    def add_data(self, name:
        str, ts: float, val: Any) -> None:
        if name not in self.data:
            self.data[name] = []
        self.data[name].append({"timestamp": ts, "value": val})

    def enforce(self) -> int:
        removed = 0
        now = datetime.now().timestamp()
        for pat, pol in self.policies.items():
            matching = [m for m in self.data if pat.replace("*", "") in m]
            for m in matching:
                orig = len(self.data[m])
                if pol.retention_days > 0:
                    cutoff = now - (pol.retention_days * 86400)
                    self.data[m] = [d for d in self.data[m] if d["timestamp"] > cutoff]
                removed += orig - len(self.data[m])
        return removed