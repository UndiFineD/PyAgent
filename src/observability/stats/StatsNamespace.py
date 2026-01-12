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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_stats.py"""



from .Metric import Metric

from typing import Dict, List, Optional



































class StatsNamespace:
    """Represents a namespace for metric isolation."""
    def __init__(self, name: str) -> None:
        self.name = name
        self.metrics: Dict[str, List[Metric]] = {}
        self.metric_values: Dict[str, float] = {}  # Direct metric values for set_metric/get_metric

    def add_metric(self, metric: Metric) -> None:
        """Add a metric to namespace."""
        if metric.name not in self.metrics:
            self.metrics[metric.name] = []
        self.metrics[metric.name].append(metric)

    def set_metric(self, name: str, value: float) -> None:
        """Set a metric value."""
        self.metric_values[name] = value

    def get_metric(self, name: str) -> Optional[float]:
        """Get a metric value."""
        return self.metric_values.get(name)

    def get_metrics(self) -> Dict[str, List[Metric]]:
        """Get all metrics in namespace."""
        return self.metrics
