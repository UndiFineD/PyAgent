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


"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from src.core.base.common.types import changelog_entry
from src.core.base.common.types import monorepo_entry

__version__ = VERSION


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
        self.packages: dict[str, MonorepoEntry] = {}

    def add_package(
        self,
        package_name: str,
        version: str,
        entries: list[ChangelogEntry],
        path: str = "",
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
            package_name=package_name, version=version, entries=entries, path=path
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

        return "\n".join(result)
