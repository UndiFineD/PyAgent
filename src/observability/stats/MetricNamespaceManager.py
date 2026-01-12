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



from .MetricNamespace import MetricNamespace

from typing import Dict, List, Optional



































class MetricNamespaceManager:
    """Manage metric namespaces for organizing large metric sets.

    Provides namespace management for organizing and hierarchically
    structuring large collections of metrics.

    Attributes:
        namespaces: Registered namespaces.
        metrics_by_namespace: Metrics organized by namespace.
    """

    def __init__(self) -> None:
        """Initialize namespace manager."""
        self.namespaces: Dict[str, MetricNamespace] = {}
        self.metrics_by_namespace: Dict[str, List[str]] = {}

    def create_namespace(
        self,
        name: str,
        description: str = "",
        parent: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> MetricNamespace:
        """Create a new namespace.

        Args:
            name: Namespace name.
            description: Description of the namespace.
            parent: Parent namespace name.
            tags: Tags for the namespace.

        Returns:
            The created namespace.
        """
        if parent and parent not in self.namespaces:
            raise ValueError(f"Parent namespace '{parent}' does not exist")

        namespace = MetricNamespace(
            name=name,
            description=description,
            parent=parent,
            tags=tags or {}
        )
        self.namespaces[name] = namespace
        self.metrics_by_namespace[name] = []
        return namespace

    def delete_namespace(self, name: str) -> bool:
        """Delete a namespace.

        Args:
            name: Name of namespace to delete.

        Returns:
            True if namespace was deleted.
        """
        # Check for child namespaces
        for ns in self.namespaces.values():
            if ns.parent == name:
                raise ValueError("Cannot delete: namespace has children")

        if name in self.namespaces:
            del self.namespaces[name]
            if name in self.metrics_by_namespace:
                del self.metrics_by_namespace[name]
            return True
        return False

    def assign_metric(self, metric_name: str, namespace: str) -> bool:
        """Assign a metric to a namespace.

        Args:
            metric_name: The metric name.
            namespace: The target namespace.

        Returns:
            True if assigned successfully.
        """
        if namespace not in self.namespaces:
            return False

        if metric_name not in self.metrics_by_namespace[namespace]:
            self.metrics_by_namespace[namespace].append(metric_name)
        return True

    def get_namespace_hierarchy(self, name: str) -> List[str]:
        """Get the namespace hierarchy from root to given namespace.

        Args:
            name: The namespace name.

        Returns:
            List of namespace names from root to given namespace.
        """
        hierarchy: list[str] = []
        current: str | None = name
        while current:
            hierarchy.insert(0, current)
            ns = self.namespaces.get(current)
            current = ns.parent if ns else None
        return hierarchy

    def get_full_path(self, namespace: str) -> str:
        """Get full path string for a namespace.

        Args:
            namespace: The namespace name.

        Returns:
            Full path string like "root / parent / child".
        """
        return " / ".join(self.get_namespace_hierarchy(namespace))
