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

# Phase 320: Autonomous Cluster Balancing (Resource Monitoring)

import asyncio
import psutil
from typing import Dict, Any
from src.observability.structured_logger import StructuredLogger

logger = StructuredLogger(__name__)


class ResourceMonitor:
    """
    Monitors local CPU, RAM, and Disk usage using psutil.
    Triggers 'compute borrow' requests when thresholds are exceeded.
    """

    def __init__(self, fleet=None, high_threshold: float = 70.0, critical_threshold: float = 90.0):
        self.fleet = fleet
        self.high_threshold = high_threshold
        self.critical_threshold = critical_threshold
        self.last_stats: Dict[str, float] = {}
        self.running = False
        self.is_borrowing = False

    @property
    def is_stressed(self) -> bool:
        """Returns True if any core metric exceeds the high threshold."""
        stats = self.get_latest_stats()
        core_metrics = [
            stats.get("cpu_usage", 0.0),
            stats.get("memory_usage", 0.0),
            stats.get("gpu", {}).get("usage", 0.0)
        ]
        return any(val > self.high_threshold for val in core_metrics)

    async def start(self, interval: int = 10):
        """Starts the background monitoring loop."""
        self.running = True
        logger.info(f"ResourceMonitor: Starting with thresholds H:{self.high_threshold}% C:{self.critical_threshold}%")
        while self.running:
            try:
                stats = self.collect_stats()
                self.last_stats = stats

                await self._evaluate_stress(stats)
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"ResourceMonitor: Error in loop: {e}")
                await asyncio.sleep(interval)

    def collect_stats(self) -> Dict[str, Any]:
        """Collects current hardware metrics including processing, memory, disk, network, and sensors."""
        stats = {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent,
            "network_io": psutil.net_io_counters()._asdict(),
            "temp": self._get_temperature(),
            "gpu": self._get_gpu_stats()
        }
        # Backward compatibility aliases
        stats["cpu_usage"] = stats["cpu_percent"]
        stats["memory_usage"] = stats["memory_percent"]
        stats["disk_usage"] = stats["disk_percent"]
        return stats

    def _get_temperature(self) -> float:
        """Attempts to retrieve the primary system temperature."""
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return 0.0
            # Try to find a 'coretemp' or 'cpu-thermal' or similar
            for name, entries in temps.items():
                if name in ["coretemp", "cpu-thermal", "cpu_thermal"]:
                    return entries[0].current
            # Fallback to the first available temperature
            return next(iter(temps.values()))[0].current
        except (AttributeError, Exception):
            return 0.0

    def _get_gpu_stats(self) -> Dict[str, Any]:
        """Attempts to retrieve GPU utilization using GPUtil if available."""
        gpu_data = {"usage": 0.0, "mem": 0.0}
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_data["usage"] = gpus[0].load * 100
                gpu_data["mem"] = gpus[0].memoryUtil * 100
        except (ImportError, Exception):
            pass
        return gpu_data

    def get_latest_stats(self) -> Dict[str, Any]:
        """Returns the most recently collected hardware metrics."""
        return self.last_stats or self.collect_stats()

    async def _evaluate_stress(self, stats: Dict[str, Any]):
        """Checks if local node is under heavy load and needs to delegate."""
        # Only check core metrics for stress evaluation
        core_metrics = [
            stats.get("cpu_usage", 0.0),
            stats.get("memory_usage", 0.0),
            stats.get("gpu", {}).get("usage", 0.0)
        ]

        is_stressed = any(val > self.high_threshold for val in core_metrics)
        is_critical = any(val > self.critical_threshold for val in core_metrics)

        if is_critical:
            logger.warning(f"ResourceMonitor: CRITICAL LOAD DETECTED. Stats: {stats}")

        if is_stressed and self.fleet and not self.is_borrowing:
            logger.info("ResourceMonitor: Threshold exceeded (>70%). Requesting compute borrow from swarm...")
            self.is_borrowing = True
            success = await self.fleet.request_compute_borrow(stats)
            if success:
                logger.info("ResourceMonitor: Successfully delegated extra load to neighbors.")
            else:
                logger.warning("ResourceMonitor: No neighbor available to take load.")

            # Reset borrowing flag after a cooldown (e.g., 60s) to avoid spamming
            await asyncio.sleep(60)
            self.is_borrowing = False
            # Potentially trigger emergency measures
        elif is_stressed:
            logger.info(f"ResourceMonitor: High load detected. Suggesting task delegation. Stats: {stats}")

    def stop(self):
        self.running = False
        logger.info("ResourceMonitor: Stopped.")
