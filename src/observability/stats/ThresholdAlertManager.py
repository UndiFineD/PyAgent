#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from .ThresholdAlert import ThresholdAlert

from typing import Dict, List, Optional


































from src.core.base.version import VERSION
__version__ = VERSION

class ThresholdAlertManager:
    """Manages threshold-based alerting."""
    def __init__(self) -> None:
        self.alerts: List[ThresholdAlert] = []
        # Each metric can have warning/critical thresholds and/or min/max thresholds.
        self.thresholds: Dict[str, Dict[str, Optional[float]]] = {}

    def set_threshold(
        self,
        metric: str,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
        warning: Optional[float] = None,
        critical: Optional[float] = None,
    ) -> None:
        """Set thresholds for a metric.

        Compatibility:
        - Some callers use `warning=` and `critical=`.
        - Older callers use `min_val=`/`max_val=`.
        """
        self.thresholds[metric] = {
            "min": min_val,
            "max": max_val,
            "warning": warning,
            "critical": critical,
        }

    def check(self, metric: str, value: float) -> List["ThresholdAlert"]:
        """Check a value against thresholds and return any alerts."""
        if metric not in self.thresholds:
            return []

        thresh = self.thresholds[metric]
        alerts: List[ThresholdAlert] = []

        # Warning/critical are treated as "value >= threshold".
        critical_threshold = thresh.get("critical")
        warning_threshold = thresh.get("warning")
        if critical_threshold is not None and value >= critical_threshold:
            alerts.append(
                ThresholdAlert(metric=metric, value=value, severity="critical", threshold=critical_threshold)
            )
        elif warning_threshold is not None and value >= warning_threshold:
            alerts.append(
                ThresholdAlert(metric=metric, value=value, severity="warning", threshold=warning_threshold)
            )

        # Min/max thresholds are treated as bounds checks.
        min_threshold = thresh.get("min")
        max_threshold = thresh.get("max")
        if min_threshold is not None and value < min_threshold:
            alerts.append(
                ThresholdAlert(metric=metric, value=value, severity="below_min", threshold=min_threshold)
            )
        if max_threshold is not None and value > max_threshold:
            alerts.append(
                ThresholdAlert(metric=metric, value=value, severity="above_max", threshold=max_threshold)
            )

        self.alerts.extend(alerts)
        return alerts

    def check_value(self, metric: str, value: float) -> bool:
        """Compatibility wrapper: return True if any alert triggered."""
        return len(self.check(metric, value)) > 0
