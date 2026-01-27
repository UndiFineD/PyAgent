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
Real-time memory profiling for Phase 52.
Tracks DBO allocation patterns and fragmentation in the synchronized workspace.
"""

import logging
import time
from typing import Any, Dict, List

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger(__name__)


class MemoryProfiler:
    """
    Profiles workspace memory usage with sub-millisecond precision.
    Integrates with Rust for high-throughput allocation tracking.
    """

    def __init__(self) -> None:
        self.snapshots: List[Dict[str, Any]] = []
        self.peak_memory = 0
        self.start_time = time.time()

    def take_snapshot(self, label: str = "auto") -> Dict[str, Any]:
        """Captures current memory state and fragmentation metrics."""
        usage = 0
        frag = 0.0

        if rc and hasattr(rc, "memory_profile_rust"):
            try:
                stats = rc.memory_profile_rust()
                usage = stats.get("current_usage", 0)
                frag = stats.get("fragmentation", 0.0)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.debug(f"Rust profiling failed: {e}")

        self.peak_memory = max(self.peak_memory, usage)

        snapshot = {
            "timestamp": time.time() - self.start_time,
            "label": label,
            "usage_bytes": usage,
            "fragmentation": frag,
        }
        self.snapshots.append(snapshot)
        return snapshot

    def analyze_patterns(self) -> Dict[str, Any]:
        """Analyzes allocation patterns to detect leaks or inefficiencies."""
        if not self.snapshots:
            return {}

        return {
            "duration": time.time() - self.start_time,
            "peak_mb": self.peak_memory / (1024 * 1024),
            "avg_fragmentation": sum(s["fragmentation"] for s in self.snapshots) / len(self.snapshots),
            "snapshot_count": len(self.snapshots),
        }

    def reset(self) -> None:
        """Clears profiler history."""
        self.snapshots.clear()
        self.peak_memory = 0
        self.start_time = time.time()
