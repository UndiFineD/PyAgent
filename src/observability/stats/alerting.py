#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Logic for thresholds, alerting, and retention enforcement.

from __future__ import annotations
import logging
from datetime import datetime
from typing import Any
from .observability_core import Alert, AlertSeverity, RetentionPolicy, Threshold

try:
    from rust_core import match_policies_rust
    _RUST_ACCEL = True
except ImportError:
    _RUST_ACCEL = False

logger = logging.getLogger(__name__)


class ThresholdAlertManager:
    """Manages threshold checking and alert emission."""

    def __init__(self) -> None:
        self.thresholds: dict[str, list[Threshold]] = {}
        self.alerts: list[Alert] = []

    def set_threshold(
        self,
        name: str,
        threshold: Threshold | None = None,
        warning: float | None = None,
        critical: float | None = None,
    ) -> None:
        if threshold is None:
            if warning is not None:
                # Warning threshold
                self.set_threshold(
                    name,
                    Threshold(
                        metric_name=name,
                        max_value=warning,
                        severity=AlertSeverity.MEDIUM,
                    ),
                )
            if critical is not None:
                # Critical threshold
                self.set_threshold(
                    name,
                    Threshold(
                        metric_name=name,
                        max_value=critical,
                        severity=AlertSeverity.CRITICAL,
                    ),
                )
            return
        if name not in self.thresholds:
            self.thresholds[name] = []
        self.thresholds[name].append(threshold)

    def check(self, metric_name: str, value: float) -> list[Alert]:
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
                    threshold_value=t.max_value
                    if t.max_value is not None
                    else t.min_value,  # type: ignore
                    severity=t.severity or AlertSeverity.MEDIUM,
                    message=t.message or f"Threshold breach for {metric_name}",
                    timestamp=datetime.now().isoformat(),
                )
                self.alerts.append(alert)
                triggered.append(alert)
        return triggered


class RetentionEnforcer:
    """Enforces retention policies on metrics."""

    def __init__(self) -> None:
        self.policies: dict[str, RetentionPolicy] = {}
        self.data: dict[str, list[dict[str, Any]]] = {}

    def set_policy(self, pattern: str, policy: RetentionPolicy) -> None:
        self.policies[pattern] = policy

    def add_data(
        self,
        name: str,
        ts: float | None = None,
        val: Any = None,
        timestamp: float | None = None,
        value: Any = None,
    ) -> None:
        actual_ts = timestamp if timestamp is not None else ts
        actual_val = value if value is not None else val
        if actual_ts is None:
            actual_ts = datetime.now().timestamp()

        if name not in self.data:
            self.data[name] = []
        self.data[name].append({"timestamp": actual_ts, "value": actual_val})

    def enforce(self) -> int:
        removed = 0
        now = datetime.now().timestamp()
        if _RUST_ACCEL and self.policies:
            # Use Rust for pattern matching
            patterns = list(self.policies.keys())
            data_keys = list(self.data.keys())
            policy_matches = match_policies_rust(patterns, data_keys)
            for pat, matching in policy_matches:
                pol = self.policies[pat]
                for m in matching:
                    orig = len(self.data[m])
                    if pol.retention_days > 0:
                        cutoff = now - (pol.retention_days * 86400)
                        self.data[m] = [d for d in self.data[m] if d["timestamp"] > cutoff]
                    removed += orig - len(self.data[m])
        else:
            # Python fallback
            for pat, pol in self.policies.items():
                matching = [m for m in self.data if pat.replace("*", "") in m]
                for m in matching:
                    orig = len(self.data[m])
                    if pol.retention_days > 0:
                        cutoff = now - (pol.retention_days * 86400)
                        self.data[m] = [d for d in self.data[m] if d["timestamp"] > cutoff]
                    removed += orig - len(self.data[m])
        return removed
