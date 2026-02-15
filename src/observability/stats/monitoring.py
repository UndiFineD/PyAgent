#!/usr/bin/env python3


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Monitoring.py - System resource monitoring engine

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Instantiate ResourceMonitor with the workspace root path and call get_current_stats() to retrieve a snapshot dict of system metrics or get_market_multiplier() to obtain a simple multiplier for agent scheduling decisions. Example: monitor = ResourceMonitor("C:\\path\\to\\workspace"); stats = monitor.get_current_stats(); mult = monitor.get_market_multiplier().

WHAT IT DOES:
Reports platform string, CPU and memory usage percentages, free disk space (GB), a simple health status (HEALTHY/WARNING/CRITICAL/ERROR/UNAVAILABLE), and a placeholder GPU field; uses psutil when available and logs failures. Provides a coarse "market multiplier" (1.0, 1.5, 3.0) derived from status to influence agent throttling or task costing.

WHAT IT SHOULD DO BETTER:
- Add configurable thresholds and expose them via constructor or config rather than hard-coded 70/90 values.
- Implement GPU detection (CUDA/ROCk) and accurate GPU load/VRAM metrics when applicable.
- Persist historical stats to the stats_file and rotate/aggregate them for trend-based decisions.
- Make sampling non-blocking/async and allow cpu_percent interval control to avoid sudden spikes or blocking calls.
- Improve error handling granularity (avoid broad except), avoid using private psutil internals import, add unit tests, and ensure cross-platform disk-path handling.

FILE CONTENT SUMMARY:
Monitoring.py module.
"""
# System resource monitoring engine.

from __future__ import annotations

import logging
import platform
from pathlib import Path
from typing import Any

from psutil._common import sdiskusage

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

logger: logging.Logger = logging.getLogger(__name__)


class ResourceMonitor:
    """Monitors local system load to inform agent execution strategies."""

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.stats_file: Path = self.workspace_root / ".system_stats.json"

    def get_current_stats(self) -> dict[str, Any]:
        stats: dict[str, Any] = {
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
            disk: sdiskusage = psutil.disk_usage(str(self.workspace_root))
            stats["disk_free_gb"] = round(disk.free / (1024**3), 2)
            if stats["cpu_usage_pct"] > 90 or stats["memory_usage_pct"] > 90:
                stats["status"] = "CRITICAL"
            elif stats["cpu_usage_pct"] > 70 or stats["memory_usage_pct"] > 70:
                stats["status"] = "WARNING"
            else:
                stats["status"] = "HEALTHY"
        except (psutil.Error, OSError) as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Failed to gather resource stats: {e}")
            stats["status"] = "ERROR"
        return stats

    def get_market_multiplier(self) -> float:
        stats: dict[str, Any] = self.get_current_stats()
        mult = 1.0
        if stats["status"] == "CRITICAL":
            mult = 3.0
        elif stats["status"] == "WARNING":
            mult = 1.5
        return mult
"""
# System resource monitoring engine.

from __future__ import annotations

import logging
import platform
from pathlib import Path
from typing import Any

from psutil._common import sdiskusage

try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

logger: logging.Logger = logging.getLogger(__name__)


class ResourceMonitor:
    """Monitors local system load to inform agent execution strategies."""

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.stats_file: Path = self.workspace_root / ".system_stats.json"

    def get_current_stats(self) -> dict[str, Any]:
        stats: dict[str, Any] = {
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
            disk: sdiskusage = psutil.disk_usage(str(self.workspace_root))
            stats["disk_free_gb"] = round(disk.free / (1024**3), 2)
            if stats["cpu_usage_pct"] > 90 or stats["memory_usage_pct"] > 90:
                stats["status"] = "CRITICAL"
            elif stats["cpu_usage_pct"] > 70 or stats["memory_usage_pct"] > 70:
                stats["status"] = "WARNING"
            else:
                stats["status"] = "HEALTHY"
        except (psutil.Error, OSError) as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Failed to gather resource stats: {e}")
            stats["status"] = "ERROR"
        return stats

    def get_market_multiplier(self) -> float:
        stats: dict[str, Any] = self.get_current_stats()
        mult = 1.0
        if stats["status"] == "CRITICAL":
            mult = 3.0
        elif stats["status"] == "WARNING":
            mult = 1.5
        return mult
