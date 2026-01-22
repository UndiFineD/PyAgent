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

<<<<<<< HEAD
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Core logic for metrics collection and performance analysis.
"""

from __future__ import annotations
<<<<<<< HEAD

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

=======
import time
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.metrics")

<<<<<<< HEAD

@dataclass
class MetricRecord:
    """Represents a single metric data point."""

=======
@dataclass
class MetricRecord:
    """Represents a single metric data point."""
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    name: str
    value: float
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

<<<<<<< HEAD

@dataclass
class AgentMetrics:
    """Manages execution metrics and statistics for an agent."""

=======
@dataclass
class AgentMetrics:
    """Manages execution metrics and statistics for an agent."""
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    files_processed: int = 0
    files_modified: int = 0
    agents_applied: dict[str, int] = field(default_factory=dict)
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None

    def record_file_processed(self, modified: bool = False) -> None:
<<<<<<< HEAD
        """Records a file being processed."""
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.files_processed += 1
        if modified:
            self.files_modified += 1

    def record_agent_applied(self, agent_name: str) -> None:
<<<<<<< HEAD
        """Records an agent being applied."""
        self.agents_applied[agent_name] = self.agents_applied.get(agent_name, 0) + 1

    def finalize(self) -> None:
        """Finalizes the metrics."""
        self.end_time = time.time()

    def get_summary(self, dry_run: bool = False) -> str:
        """Returns a string summary of the execution."""
=======
        self.agents_applied[agent_name] = self.agents_applied.get(agent_name, 0) + 1

    def finalize(self) -> None:
        self.end_time = time.time()

    def get_summary(self, dry_run: bool = False) -> str:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if not self.end_time:
            self.finalize()
        elapsed = self.end_time - self.start_time

        summary = f"""
=== Agent Execution Summary ===
Files processed: {self.files_processed}
Files modified:  {self.files_modified}
Execution time:  {elapsed:.2f}s
Dry-run mode:    {"Yes" if dry_run else "No"}

Agents applied:
"""
        for agent, count in sorted(self.agents_applied.items()):
            summary += f"  - {agent}: {count} files\n"
        return summary

    def to_dict(self) -> dict[str, Any]:
<<<<<<< HEAD
        """Returns the metrics as a dictionary."""
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if not self.end_time:
            self.finalize()
        elapsed = self.end_time - self.start_time
        return {
            "timestamp": time.time(),
            "start_time": self.start_time,
            "end_time": self.end_time,
            "summary": {
                "files_processed": self.files_processed,
                "files_modified": self.files_modified,
                "total_time_seconds": elapsed,
                "average_time_per_file": elapsed / max(self.files_processed, 1),
            },
            "agents_applied": self.agents_applied,
        }

<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class MetricsCore(BaseCore):
    """
    Authoritative engine for agent metrics collection and performance analysis.
    """
<<<<<<< HEAD

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
=======
    def __init__(self) -> None:
        super().__init__()
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self._metrics = AgentMetrics()
        self.records: List[MetricRecord] = []
        self.start_times: Dict[str, float] = {}

    @property
    def metrics(self) -> AgentMetrics:
<<<<<<< HEAD
        """Returns the internal AgentMetrics instance."""
        return self._metrics

    def record_file(self, modified: bool = False) -> None:
        """Wrapper for record_file_processed."""
        self._metrics.record_file_processed(modified)

    def record_agent(self, agent_name: str) -> None:
        """Wrapper for record_agent_applied."""
        self._metrics.record_agent_applied(agent_name)

    def start_timer(self, key: str) -> None:
        """Starts a timer for a given key."""
        self.start_times[key] = time.time()

    def stop_timer(self, key: str, metadata: Dict[str, Any] | None = None) -> float:
        """Stops a timer and records the elapsed time."""
=======
        return self._metrics

    def record_file(self, modified: bool = False) -> None:
        self._metrics.record_file_processed(modified)

    def record_agent(self, agent_name: str) -> None:
        self._metrics.record_agent_applied(agent_name)

    def start_timer(self, key: str) -> None:
        self.start_times[key] = time.time()

    def stop_timer(self, key: str, metadata: Dict[str, Any] | None = None) -> float:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if key not in self.start_times:
            return 0.0
        elapsed = time.time() - self.start_times.pop(key, time.time())
        self.record_metric(key, elapsed, metadata)
        return elapsed

    def record_metric(self, name: str, value: float, metadata: Dict[str, Any] | None = None) -> None:
<<<<<<< HEAD
        """Records a custom metric data point."""
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.records.append(MetricRecord(name, value, metadata=metadata or {}))
        # Keep buffer sane
        if len(self.records) > 10000:
            self.records = self.records[-5000:]

    def finalize(self) -> None:
<<<<<<< HEAD
        """Finalizes all metrics."""
        self._metrics.finalize()

    def get_report(self) -> Dict[str, Any]:
        """Generates a full execution report."""
=======
        self._metrics.finalize()

    def get_report(self) -> Dict[str, Any]:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        report = self._metrics.to_dict()
        report["custom_metrics"] = [r.__dict__ for r in self.records]
        return report

<<<<<<< HEAD
    def calculate_anchoring_strength(self, result: str, _context_pool: Optional[Dict[str, Any]] = None) -> float:
        """Calculate the 'Anchoring Strength' metric (Stanford Research 2025)."""
        if not result:
            return 0.0
        # This is a placeholder for actual complex logic often moved to Rust
        return 0.95

    def verify_self(self, _result: str, anchoring_score: float) -> Tuple[bool, str]:
=======
    def calculate_anchoring_strength(self, result: str, context_pool: Optional[Dict[str, Any]] = None) -> float:
        """Calculate the 'Anchoring Strength' metric (Stanford Research 2025)."""
        if not result: return 0.0
        # This is a placeholder for actual complex logic often moved to Rust
        return 0.95 

    def verify_self(self, result: str, anchoring_score: float) -> Tuple[bool, str]:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """Self-verification layer."""
        if anchoring_score > 0.8:
            return True, "Verified"
        return False, "Weak anchoring"

    def aggregate_summary(self) -> Dict[str, float]:
        """High-throughput aggregation of stored records."""
        if rc:
            try:
                # Group records by name
                grouped: Dict[str, List[float]] = {}
                for r in self.records:
<<<<<<< HEAD
                    if r.name not in grouped:
                        grouped[r.name] = []
                    grouped[r.name].append(r.value)
                # pylint: disable=no-member
                return rc.aggregate_metrics_rust(grouped)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.debug("Rust metrics aggregation failed: %s", e)

        # Python fallback
        results = {}
        grouped_py: Dict[str, List[float]] = {}
        for rec in self.records:
            if rec.name not in grouped_py:
                grouped_py[rec.name] = []
            grouped_py[rec.name].append(rec.value)

        for name, vals in grouped_py.items():
=======
                    if r.name not in grouped: grouped[r.name] = []
                    grouped[r.name].append(r.value)
                return rc.aggregate_metrics_rust(grouped)
            except Exception as e:
                logger.debug(f"Rust metrics aggregation failed: {e}")
        
        # Python fallback
        results = {}
        grouped: Dict[str, List[float]] = {}
        for r in self.records:
            if r.name not in grouped: grouped[r.name] = []
            grouped[r.name].append(r.value)
        
        for name, vals in grouped.items():
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            results[name] = sum(vals) / len(vals)
        return results

    def get_rolling_avg(self, metric_name: str, window: int = 10) -> List[float]:
        """Calculate rolling average for a specific metric."""
        values = [r.value for r in self.records if r.name == metric_name]
        if rc:
            try:
<<<<<<< HEAD
                # pylint: disable=no-member
                return rc.rolling_avg_rust(values, window)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.debug("Rust rolling average failed: %s", e)

        # Python fallback
        if not values:
            return []
        res = []
        for i in range(len(values)):
            start = max(0, i - window + 1)
            slice_vals = values[start : i + 1]
=======
                return rc.rolling_avg_rust(values, window)
            except Exception as e:
                logger.debug(f"Rust rolling average failed: {e}")
        
        # Python fallback
        if not values: return []
        res = []
        for i in range(len(values)):
            start = max(0, i - window + 1)
            slice_vals = values[start:i+1]
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            res.append(sum(slice_vals) / len(slice_vals))
        return res
