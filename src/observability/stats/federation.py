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
Federation.py module.
"""
# Stats federation engine.

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from src.core.base.logic.connectivity_manager import ConnectivityManager

from .metrics import AggregationResult
from .observability_core import (AggregationType, FederatedSource,
                                 FederationMode)

logger = logging.getLogger(__name__)


class StatsFederation:
    """Aggregate stats from multiple repositories."""

    def __init__(self, mode: FederationMode = FederationMode.PULL) -> None:
        self.mode = mode
        self.sources: dict[str, FederatedSource] = {}
        self.aggregated: dict[str, list[float]] = {}
        self._last_sync: dict[str, datetime] = {}
        self.connectivity = ConnectivityManager()

    def add_source(
        self,
        name: str,
        endpoint: str | None = None,
        data: dict[str, float] | None = None,
        healthy: bool = True,
    ) -> None:
        source = FederatedSource(repo_url=name, api_endpoint=endpoint or "", enabled=healthy)
        self.sources[name] = source
        self._last_sync[name] = datetime.min
        if data:
            source.metrics.update({k: float(v) for k, v in data.items()})

    def remove_source(self, name: str) -> bool:
        if name in self.sources:
            del self.sources[name]
            return True
        return False

    def sync_source(self, name: str) -> dict[str, float]:
        if name not in self.sources or not self.sources[name].enabled:
            return {}
        source = self.sources[name]
        if source.api_endpoint.startswith(("http", "https")):
            try:
                data = self.connectivity.get_json(source.api_endpoint)
                if isinstance(data, dict):
                    source.metrics.update({k: float(v) for k, v in data.items() if isinstance(v, (int, float))})
                    return source.metrics
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.error(f"Sync failed for {name}: {e}")
        return {}

    def sync_all(self) -> dict[str, dict[str, float]]:
        return {name: self.sync_source(name) for name in self.sources}

    def aggregate(self, metric_name: str, aggregation: AggregationType = AggregationType.SUM) -> AggregationResult:
        values = []
        failed = 0
        for name, src in self.sources.items():
            if src.enabled and metric_name in src.metrics:
                values.append(src.metrics[metric_name])
            else:
                failed += 1

        # Add local aggregated data
        if metric_name in self.aggregated:
            values.extend(self.aggregated[metric_name])

        total = 0.0
        if values:
            if aggregation == AggregationType.SUM:
                total = float(sum(values))
            elif aggregation == AggregationType.AVG:
                total = float(sum(values) / len(values))
            elif aggregation == AggregationType.MIN:
                total = float(min(values))
            elif aggregation == AggregationType.MAX:
                total = float(max(values))
            elif aggregation == AggregationType.COUNT:
                total = float(len(values))

        return AggregationResult(
            total,
            total=total,
            failed_sources=failed,
            source_count=len(values),
            metric_name=metric_name,
        )

    def get_federation_status(self) -> dict[str, Any]:
        """Get status of federation."""
        # Include source names as keys for test compatibility
        status = {
            "sources": len(self.sources),
            "healthy": sum(1 for s in self.sources.values() if s.enabled),
            "last_sync": self._last_sync,
        }
        for name in self.sources:
            status[name] = "healthy" if self.sources[name].enabled else "unhealthy"
        return status
