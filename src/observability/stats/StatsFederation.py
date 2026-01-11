#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from .AggregationType import AggregationType
from .FederatedSource import FederatedSource
from .FederationMode import FederationMode

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import logging
from src.core.base.ConnectivityManager import ConnectivityManager


































from src.core.base.version import VERSION
__version__ = VERSION

class AggregationResult(Dict[str, Any]):
    """Compatibility class that behaves like both a dict and a float."""
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, (int, float)):
            return float(self.get("total", 0.0)) == float(other)
        return super().__eq__(other)

    def __float__(self) -> float:
        return float(self.get("total", 0.0))

class StatsFederation:
    """Aggregate stats from multiple repositories.

    Provides federation capabilities to collect and aggregate
    metrics from multiple source repositories.

    Attributes:
        sources: Federated data sources.
        mode: Federation mode (pull, push, hybrid).
        aggregated: Aggregated metrics from all sources.
    """

    def __init__(self, mode: FederationMode = FederationMode.PULL) -> None:
        """Initialize stats federation.

        Args:
            mode: The federation mode to use.
        """
        self.mode = mode
        self.sources: Dict[str, FederatedSource] = {}
        self.aggregated: Dict[str, List[float]] = {}
        self._last_sync: Dict[str, datetime] = {}
        self.connectivity = ConnectivityManager()

    def add_source(
        self,
        name: str,
        endpoint: Optional[str] = None,
        data: Optional[Dict[str, float]] = None,
        healthy: bool = True
    ) -> None:
        """Add a federated source.

        Args:
            name: Name for the source.
            endpoint: Optional API endpoint for the source.
            data: Optional data dictionary from the source.
            healthy: Whether the source is healthy.
        """
        source = FederatedSource(
            repo_url=name,
            api_endpoint=endpoint or "",
            enabled=healthy
        )
        self.sources[name] = source
        self._last_sync[name] = datetime.min

        # Store data if provided
        if data:
            source.metrics.update({k: float(v) for k, v in data.items()})

    def remove_source(self, name: str) -> bool:
        """Remove a federated source.

        Args:
            name: Name of the source to remove.

        Returns:
            True if source was removed.
        """
        if name in self.sources:
            del self.sources[name]
            if name in self._last_sync:
                del self._last_sync[name]
            return True
        return False

    def sync_source(self, name: str) -> Dict[str, float]:
        """Sync metrics from a specific source.

        Args:
            name: Name of the source to sync.

        Returns:
            Dictionary of synced metrics.
        """
        if name not in self.sources:
            return {}

        source = self.sources[name]
        if not source.enabled:
            return {}

        # Phase 120 enhancement: Real endpoint synchronization
        endpoint = source.api_endpoint
        if endpoint and endpoint.startswith(("http://", "https://")):
            try:
                headers = {}
                if source.auth_token:
                    headers["Authorization"] = f"Bearer {source.auth_token}"
                
                # Use ConnectivityManager
                data = self.connectivity.get_json(endpoint, headers=headers)
                
                if isinstance(data, dict):
                    # update metrics on source object
                    for k, v in data.items():
                        if isinstance(v, (int, float)):
                             source.metrics[k] = float(v)
                    
                    # Maintain compatibility with current aggregate() logic
                    self.aggregated[name] = [float(v) for v in data.values() if isinstance(v, (int, float))]
                    
                    self._last_sync[name] = datetime.now()
                    return {k: float(v) for k, v in data.items() if isinstance(v, (int, float))}
            except Exception as e:
                logging.error(f"StatsFederation: Sync failed for {name} ({endpoint}): {e}")
        
        self._last_sync[name] = datetime.now()
        return {}

    def sync_all(self) -> Dict[str, Dict[str, float]]:
        """Sync metrics from all sources.

        Returns:
            Dictionary of metrics per source.
        """
        results: Dict[str, Dict[str, float]] = {}
        for name in self.sources:
            results[name] = self.sync_source(name)
        return results

    def aggregate(
        self,
        metric_name: str,
        aggregation: AggregationType = AggregationType.SUM
    ) -> AggregationResult:
        """Aggregate a metric across all sources.

        Args:
            metric_name: The metric to aggregate.
            aggregation: The aggregation type.

        Returns:
            AggregationResult behaving as both dict and float.
        """
        values: List[float] = list(self.aggregated.get(metric_name, []))
        failed_sources = 0
        
        # Collect values from all sources
        for source_name, source in self.sources.items():
            if not source.enabled:
                failed_sources += 1
                continue
                
            # Check for the specific metric in the source's metrics dictionary
            if metric_name in source.metrics:
                value = source.metrics[metric_name]
                if isinstance(value, (int, float)):
                    values.append(float(value))

        total = 0.0
        if values:
            if aggregation == AggregationType.SUM:
                total = sum(values)
            elif aggregation == AggregationType.AVG:
                total = sum(values) / len(values)
            elif aggregation == AggregationType.MIN:
                total = min(values)
            elif aggregation == AggregationType.MAX:
                total = max(values)
            elif aggregation == AggregationType.COUNT:
                total = float(len(values))
        
        return AggregationResult({
            "total": total,
            "failed_sources": failed_sources,
            "source_count": len(values),
            "metric_name": metric_name
        })

    def get_federation_status(self) -> Dict[str, Dict[str, Union[bool, str]]]:
        """Get status of all federated sources.

        Returns:
            Status information per source.
        """
        status: Dict[str, Dict[str, Union[bool, str]]] = {}
        for name, source in self.sources.items():
            status[name] = {
                "enabled": source.enabled,
                "last_sync": self._last_sync.get(name, datetime.min).isoformat(),
                "endpoint": source.api_endpoint
            }
        return status
