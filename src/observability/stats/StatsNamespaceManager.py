#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from .StatsNamespace import StatsNamespace

from typing import Dict, Optional


































from src.core.base.version import VERSION
__version__ = VERSION

class StatsNamespaceManager:
    """Manages multiple namespaces."""
    def __init__(self) -> None:
        self.namespaces: Dict[str, StatsNamespace] = {}

    def create(self, name: str) -> StatsNamespace:
        """Create a new namespace."""
        ns = StatsNamespace(name)
        self.namespaces[name] = ns
        return ns

    def create_namespace(self, name: str) -> StatsNamespace:
        """Create a new namespace (backward compat)."""
        return self.create(name)

    def get_namespace(self, name: str) -> Optional[StatsNamespace]:
        """Get a namespace."""
        return self.namespaces.get(name)
