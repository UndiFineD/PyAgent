#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
"""
System Health Monitor.
(Facade for src.core.base.common.health_core)
"""

from src.core.base.common.health_core import HealthCore as StandardHealthCore


class SystemHealthMonitor(StandardHealthCore):
    """Monitors backend health and manages failover.
    Integrated with StabilityCore for advanced fleet-wide stasis detection.
    """

    def __init__(
        self,
        health_threshold: float = 0.8,
        window_size: int = 100,
    ) -> None:
        super().__init__()
        from src.observability.stats.core.stability_core import StabilityCore

        self.health_threshold = health_threshold
        self.window_size = window_size
        self.core = StabilityCore()
