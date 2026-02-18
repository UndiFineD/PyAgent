#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Core logic for metrics collection and performance analysis.
"""


from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .base_core import BaseCore

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.metrics")

@dataclass
class MetricRecord:
    """Represents a single metric data point."""
    name: str
    value: float
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentMetrics:
    """Manages execution metrics and statistics for an agent."""
    files_processed: int = 0
    files_modified: int = 0
    agents_applied: dict[str, int] = field(default_factory=dict)
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None

    def record_file_processed(self, modified: bool = False) -> None:
        """Records a file being processed."""
        self.files_processed += 1
        if modified:
            self.files_modified += 1

    def record_agent_applied(self, agent_name: str) -> None:
        """Records an agent being applied."""
        self.agents_applied[agent_name] = self.agents_applied.get(agent_name, 0) + 1

    def finalize(self) -> None:
        """Finalizes the metrics."""
        self.end_time = time.time()

    def get_summary(self, dry_run: bool = False) -> str:
        """Returns a string summary of the execution."""
        if not self.end_time:
            self.finalize()
        elapsed = self.end_time - self.start_time
    # Build summary string
        summary = (
            f"=== Agent Execution Summary ===\n"
            f"Files processed: {self.files_processed}\n"
            f"Files modified:  {self.files_modified}\n"
            f"Execution time:  {elapsed:.2f}s\n"
            f"Dry-run mode:    {'Yes' if dry_run else 'No'}\n"
            f"Agents applied:\n"
        )
        lines = [f"  - {k}: {v} files\n" for k, v in sorted(self.agents_applied.items())]
        return summary + "".join(lines)


    def to_dict(self) -> dict[str, Any]:
        """Returns the metrics as a dictionary."""
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


class MetricsCore(BaseCore):
    """Authoritative engine for agent metrics collection and performance analysis.
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._metrics = AgentMetrics()
        self.records: List[MetricRecord] = []
        self.start_times: Dict[str, float] = {}

    @property
    def metrics(self) -> AgentMetrics:
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
        if key not in self.start_times:
            return 0.0
        elapsed = time.time() - self.start_times.pop(key, time.time())
        self.record_metric(key, elapsed, metadata)
        return elapsed

    def record_metric(self, name: str, value: float, metadata: Dict[str, Any] | None = None) -> None:
        """Records a custom metric data point."""
        self.records.append(MetricRecord(name, value, metadata=metadata or {}))
        # Keep buffer sane
        if len(self.records) > 10000:
            self.records = self.records[-5000:]

    def finalize(self) -> None:
        """Finalizes all metrics."""
        self._metrics.finalize()

    def get_report(self) -> Dict[str, Any]:
        """Generates a full execution report."""
        report = self._metrics.to_dict()
        report["custom_metrics"] = list(map(lambda r: r.__dict__, self.records))
        return report

    def calculate_anchoring_strength(self, result: str, _context_pool: Optional[Dict[str, Any]] = None) -> float:
        """Calculate the 'Anchoring Strength' metric (Stanford Research 2025)."""
        if not result:
            return 0.0
        # This is a TODO Placeholder regarding actual complex logic often moved to Rust
        return 0.95

    def verify_self(self, _result: str, anchoring_score: float) -> Tuple[bool, str]:
        """Self-verification layer."""
        if anchoring_score > 0.8:
            return True, "Verified"
        return False, "Weak anchoring"

    def aggregate_summary(self) -> Dict[str, float]:
        """High-throughput aggregation regarding stored records."""
        result = self._try_rust_aggregate()
        if result is not None:
            return result
        return self._python_aggregate()

    def _try_rust_aggregate(self) -> Optional[Dict[str, float]]:
        if rc:
            try:
                grouped: Dict[str, List[float]] = {}

                def group_record(r):
                    if r.name not in grouped:
                        grouped[r.name] = []
                    grouped[r.name].append(r.value)

                list(map(group_record, self.records))

                # pylint: disable=no-member
                return rc.aggregate_metrics_rust(grouped)  # type: ignore
            except (RuntimeError, AttributeError) as e:
                logger.debug("Rust metrics aggregation failed: %s", e)
        return None

    def _python_aggregate(self) -> Dict[str, float]:
        grouped_py: Dict[str, List[float]] = {}

        def group_record(rec):
            if rec.name not in grouped_py:
                grouped_py[rec.name] = []
            grouped_py[rec.name].append(rec.value)

        list(map(group_record, self.records))

        def calc_avg(item):
            name, vals = item
            return name, sum(vals) / len(vals)

        return dict(map(calc_avg, grouped_py.items()))

    def get_rolling_avg(self, metric_name: str, window: int = 10) -> List[float]:
        """Calculate rolling average regarding a specific metric."""
        values = list(map(lambda r: r.value, filter(lambda r: r.name == metric_name, self.records)))
        result = self._try_rust_rolling_avg(values, window)
        if result is not None:
            return result
        return self._python_rolling_avg(values, window)

    def _try_rust_rolling_avg(self, values: List[float], window: int) -> Optional[List[float]]:
        if rc:
            try:
                # pylint: disable=no-member
                return rc.rolling_avg_rust(values, window)  # type: ignore
            except (RuntimeError, AttributeError) as e:
                logger.debug("Rust rolling average failed: %s", e)
        return None

    def _python_rolling_avg(self, values: List[float], window: int) -> List[float]:
        if not values:
            return []

        def calc_step_avg(i):
            start = max(0, i - window + 1)
            slice_vals = values[start : i + 1]
            return sum(slice_vals) / len(slice_vals)

        return list(map(calc_step_avg, range(len(values))))
