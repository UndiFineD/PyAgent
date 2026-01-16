#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Metric namespace management engine.

from __future__ import annotations
from typing import Any
from .Metrics import MetricNamespace


class MetricNamespaceManager:
    """Manage metric namespaces for organizing large metric sets."""

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
        ns = MetricNamespace(
            name=name, description=description, parent=parent, tags=tags or {}
        )
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
        current = namespace
        while current:
            hierarchy.insert(0, current)
            ns = self.namespaces.get(current)
            current = ns.parent if ns else None
        return " / ".join(hierarchy)
