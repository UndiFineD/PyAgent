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
namespaces.py - Metric Namespace Management"""
"""
[Brief Summary]
A small manager class to create, delete, and organize MetricNamespace objects and to assign metrics to namespaces for hierarchical metric organization.
# DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
from src.core.metrics.namespaces import MetricNamespaceManager
mgr = MetricNamespaceManager()
mgr.create_namespace("infrastructure", "Infra metrics")
mgr.create_namespace("database", "DB metrics", parent="infrastructure")
mgr.assign_metric("db.connections", "database")
print(mgr.get_full_path("database"))  # "infrastructure / database"

WHAT IT DOES:
- Provides an in-memory registry for MetricNamespace instances keyed by name.
- Supports creating namespaces (with optional parent, description, tags), deleting namespaces, assigning metric names to namespaces, and resolving a namespace's full hierarchical path.
- Keeps a simple mapping of metrics per namespace for lightweight lookups.

WHAT IT SHOULD DO BETTER:
- Validate and normalize namespace names; prevent cycles in parent links and provide clearer error messages.
- Handle deletion safely (reassign or cascade metrics and child namespaces) and raise informative exceptions rather than boolean flags.
- Add persistence (disk/DB), concurrency/thread-safety, richer query APIs, and unit tests for edge cases (missing parents, duplicate assignments).
- Improve typing (use TypedDict for tags), and document expected MetricNamespace contract (required attributes used: name, parent).

FILE CONTENT SUMMARY:
Namespaces.py module.
"""
# Metric namespace management engi""""""ne.

from __future__ import annotations

from typing import Any

from .metrics import MetricNamespace


class MetricNamespaceManager:
    """Manage metric namespaces for organizing large metric set""""""s."""

    def __init__(self) -> None:
        self.namespaces: dict[str, MetricNamespace] = {}
        self.metrics_by_namespace: dict[str, list[str]] = {}

    def create_namespace(
        self,
        name: str,
        description: str = "",
        parent: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> MetricNamespace:
        if parent and parent not in self.namespaces:
            raise ValueError("Parent missing")
        ns = MetricNamespace(name=name, description=description, parent=parent, tags=tags or {})
        self.namespaces[name] = ns
        self.metrics_by_namespace[name] = []
        return ns

    def delete_namespace(self, name: str) -> bool:
        if name in self.namespaces:
            del self.namespaces[name]
            del self.metrics_by_namespace[name]
            return True
        return False

    def assign_metric(self, metric_name: str, namespace: str) -> bool:
        if namespace not in self.namespaces:
            return False
        if metric_name not in self.metrics_by_namespace[namespace]:
            self.metrics_by_namespace[namespace].append(metric_name)
        return True

    def get_full_path(self, namespace: str) -> str:
        hierarchy: list[Any] = []
        current: str | None = namespace
        while current:
            hierarchy.insert(0, current)
            ns: MetricNamespace | None = self.namespaces.get(current)
            current = ns.parent if ns else None
        return " / ".join(hierarchy)
"""
# Metric namespace managemen""""""t engine.

from __future__ import annotations

from typing import Any

from .metrics import MetricNamespace


class MetricNamespaceManager:
    """Manage metric namespaces for organizing large metr""""""ic sets."""

    def __init__(self) -> None:
        self.namespaces: dict[str, MetricNamespace] = {}
        self.metrics_by_namespace: dict[str, list[str]] = {}

    def create_namespace(
        self,
        name: str,
        description: str = "",
        parent: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> MetricNamespace:
        if parent and parent not in self.namespaces:
            raise ValueError("Parent missing")
        ns = MetricNamespace(name=name, description=description, parent=parent, tags=tags or {})
        self.namespaces[name] = ns
        self.metrics_by_namespace[name] = []
        return ns

    def delete_namespace(self, name: str) -> bool:
        if name in self.namespaces:
            del self.namespaces[name]
            del self.metrics_by_namespace[name]
            return True
        return False

    def assign_metric(self, metric_name: str, namespace: str) -> bool:
        if namespace not in self.namespaces:
            return False
        if metric_name not in self.metrics_by_namespace[namespace]:
            self.metrics_by_namespace[namespace].append(metric_name)
        return True

    def get_full_path(self, namespace: str) -> str:
        hierarchy: list[Any] = []
        current: str | None = namespace
        while current:
            hierarchy.insert(0, current)
            ns: MetricNamespace | None = self.namespaces.get(current)
            current = ns.parent if ns else None
        return " / ".join(hierarchy)
