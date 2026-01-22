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
Centralized Telemetry and Metrics Core.
Provides high-performance aggregation, alerting, and cross-tier observability.
"""

from __future__ import annotations
<<<<<<< HEAD

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
=======
import time
import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from .base_core import BaseCore
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

try:
    import rust_core as rc
except ImportError:
    rc = None

<<<<<<< HEAD
from .base_core import BaseCore

logger = logging.getLogger("pyagent.telemetry")


class MetricType(Enum):
    """Enumeration of supported metric types."""

=======
logger = logging.getLogger("pyagent.telemetry")

class MetricType(Enum):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

<<<<<<< HEAD

@dataclass
class Metric:
    """Representation of a single metric data point."""

=======
@dataclass
class Metric:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    name: str
    value: float
    metric_type: MetricType = MetricType.GAUGE
    timestamp: float = field(default_factory=time.time)
    tags: Dict[str, str] = field(default_factory=dict)
<<<<<<< HEAD
    namespace: str = "default"
    unit: str = ""
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    # Compatibility: some tests treat history entries as (timestamp, value) tuples.
    def __iter__(self) -> Any:
        yield self.timestamp
        yield self.value

    def __getitem__(self, index: int) -> Any:
        return (self.timestamp, self.value)[index]

<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class TelemetryCore(BaseCore):
    """
    Authoritative engine for system metrics and event tracking.
    Standardizes how agents and infrastructure report health and performance.
    """
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def __init__(self) -> None:
        super().__init__()
        self._metrics_buffer: List[Metric] = []
        self._alerts: List[Dict[str, Any]] = []

<<<<<<< HEAD
    def record_metric(
        self, name: str, value: float, mtype: MetricType = MetricType.GAUGE, tags: Optional[Dict[str, str]] = None
    ) -> None:
        """Records a single metric point."""
        metric = Metric(name=name, value=value, metric_type=mtype, tags=tags or {})
        self._metrics_buffer.append(metric)

=======
    def record_metric(self, name: str, value: float, mtype: MetricType = MetricType.GAUGE, tags: Optional[Dict[str, str]] = None) -> None:
        """Records a single metric point."""
        metric = Metric(name=name, value=value, metric_type=mtype, tags=tags or {})
        self._metrics_buffer.append(metric)
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Trim buffer if too large (10k points)
        if len(self._metrics_buffer) > 10000:
            self._metrics_buffer = self._metrics_buffer[-5000:]

    def get_rollups(self, metric_name: str, window_seconds: int = 3600) -> Dict[str, float]:
        """
        Calculates basic stats for a metric.
        Hot path for Rust acceleration in docs/RUST_MAPPING.md.
        """
        if rc and hasattr(rc, "calculate_rollups"):
            try:
                # Optimized Rust rollup calculation
<<<<<<< HEAD
                return rc.calculate_rollups(  # pylint: disable=no-member
                    [(m.name, m.timestamp, m.value) for m in self._metrics_buffer],
                    metric_name,
                    window_seconds,
                    time.time(),
                )
            except Exception as err:  # pylint: disable=broad-exception-caught, unused-variable
                logger.debug("Rust calculate_rollups failed, falling back: %s", err)

        now = time.time()
        relevant = [
            m.value for m in self._metrics_buffer if m.name == metric_name and (now - m.timestamp) < window_seconds
        ]

        if not relevant:
            return {"avg": 0.0, "max": 0.0, "count": 0}

        return {"avg": sum(relevant) / len(relevant), "max": max(relevant), "count": len(relevant)}

    def clear(self) -> None:
        """Clears all buffered metrics and alerts."""
=======
                return rc.calculate_rollups(
                    [(m.name, m.timestamp, m.value) for m in self._metrics_buffer],
                    metric_name,
                    window_seconds,
                    time.time()
                )
            except Exception as e:
                logger.debug("Rust calculate_rollups failed, falling back: %s", e)
        
        now = time.time()
        relevant = [m.value for m in self._metrics_buffer if m.name == metric_name and (now - m.timestamp) < window_seconds]
        
        if not relevant:
            return {"avg": 0.0, "max": 0.0, "count": 0}
            
        return {
            "avg": sum(relevant) / len(relevant),
            "max": max(relevant),
            "count": len(relevant)
        }

    def clear(self) -> None:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self._metrics_buffer.clear()
        self._alerts.clear()
