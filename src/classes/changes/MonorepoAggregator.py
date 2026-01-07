#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from .ChangelogEntry import ChangelogEntry
from .MonorepoEntry import MonorepoEntry

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

class MonorepoAggregator:
    """Aggregates changelogs for monorepo setups.

    Combines changelogs from multiple packages into a single
    unified changelog.

    Attributes:
        packages: Dictionary of package entries.

    Example:
        >>> aggregator=MonorepoAggregator()
        >>> aggregator.add_package("pkg-a", "1.0.0", entries)
        >>> unified=aggregator.generate_unified_changelog()
    """

    def __init__(self) -> None:
        """Initialize the monorepo aggregator."""
        self.packages: Dict[str, MonorepoEntry] = {}

    def add_package(
        self,
        package_name: str,
        version: str,
        entries: List[ChangelogEntry],
        path: str = ""
    ) -> MonorepoEntry:
        """Add a package to the aggregator.

        Args:
            package_name: Name of the package.
            version: Package version.
            entries: Changelog entries for the package.
            path: Path to the package.

        Returns:
            The created MonorepoEntry.
        """
        entry = MonorepoEntry(
            package_name=package_name,
            version=version,
            entries=entries,
            path=path
        )
        self.packages[package_name] = entry
        return entry

    def generate_unified_changelog(self) -> str:
        """Generate a unified changelog from all packages.

        Returns:
            Unified changelog as markdown.
        """
        result = ["# Monorepo Changelog\n"]

        for name, pkg in sorted(self.packages.items()):
            result.append(f"## {name} v{pkg.version}\n")
            for entry in pkg.entries:
                result.append(f"- [{entry.category}] {entry.description}")
            result.append("")

        return '\n'.join(result)
