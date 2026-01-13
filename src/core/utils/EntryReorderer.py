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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .ChangelogEntry import ChangelogEntry
from .GroupingStrategy import GroupingStrategy
from typing import Dict, List

__version__ = VERSION

class EntryReorderer:
    """Reorders and groups changelog entries.

    Provides functionality to reorder entries by various criteria.

    Example:
        >>> reorderer=EntryReorderer()
        >>> sorted_entries=reorderer.reorder(entries, GroupingStrategy.BY_PRIORITY)
    """

    def reorder(
        self,
        entries: list[ChangelogEntry],
        strategy: GroupingStrategy
    ) -> list[ChangelogEntry]:
        """Reorder entries based on strategy.

        Args:
            entries: Entries to reorder.
            strategy: Grouping / sorting strategy.

        Returns:
            Reordered list of entries.
        """
        if strategy == GroupingStrategy.BY_DATE:
            return sorted(entries, key=lambda e: e.date, reverse=True)
        elif strategy == GroupingStrategy.BY_VERSION:
            return sorted(entries, key=lambda e: e.version, reverse=True)
        elif strategy == GroupingStrategy.BY_CATEGORY:
            return sorted(entries, key=lambda e: e.category)
        elif strategy == GroupingStrategy.BY_AUTHOR:
            return entries  # Would need author field
        return entries

    def group_by_category(self, entries: list[ChangelogEntry]) -> dict[str, list[ChangelogEntry]]:
        """Group entries by category.

        Args:
            entries: Entries to group.

        Returns:
            Dictionary mapping category to entries.
        """
        result: dict[str, list[ChangelogEntry]] = {}
        for entry in entries:
            if entry.category not in result:
                result[entry.category] = []
            result[entry.category].append(entry)
        return result