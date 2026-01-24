#!/usr/bin/env python3

"""
Monitoring.py module.
"""
# Copyright 2026 PyAgent Authors
# System resource monitoring engine.

from __future__ import annotations

import logging
import platform
from pathlib import Path
from typing import Any

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

logger = logging.getLogger(__name__)


class ResourceMonitor:
    """Monitors local system load to inform agent execution strategies."""

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.stats_file = self.workspace_root / ".system_stats.json"

    def get_current_stats(self) -> dict[str, Any]:
        stats = {
            "platform": platform.platform(),
            "cpu_usage_pct": 0,
            "memory_usage_pct": 0,
            "disk_free_gb": 0,
            "status": "UNAVAILABLE",
            "gpu": {"available": False, "type": "NONE"},
        }
        if not HAS_PSUTIL:
            return stats
        try:
            stats["cpu_usage_pct"] = psutil.cpu_percent(interval=None)
            stats["memory_usage_pct"] = psutil.virtual_memory().percent
            disk = psutil.disk_usage(str(self.workspace_root))
            stats["disk_free_gb"] = round(disk.free / (1024**3), 2)
            if stats["cpu_usage_pct"] > 90 or stats["memory_usage_pct"] > 90:
                stats["status"] = "CRITICAL"
            elif stats["cpu_usage_pct"] > 70 or stats["memory_usage_pct"] > 70:
                stats["status"] = "WARNING"
            else:
                stats["status"] = "HEALTHY"
        except Exception as e:
            logger.error(f"Failed to gather resource stats: {e}")
            stats["status"] = "ERROR"
        return stats

    def get_market_multiplier(self) -> float:
        stats = self.get_current_stats()
        mult = 1.0
        if stats["status"] == "CRITICAL":
            mult = 3.0
        elif stats["status"] == "WARNING":
            mult = 1.5
        return mult
