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
Entry management logic for ChangesAgent.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Optional

from ..changelog_entry import ChangelogEntry
from ..validation_rule import ValidationRule


class ChangesEntryMixin:
    """Mixin for managing changelog entries."""

    # Default validation rules
    DEFAULT_VALIDATION_RULES: list[ValidationRule] = [
        ValidationRule(
            name="version_format",
            pattern=r"^\d+\.\d+\.\d+$",
            message="Version should follow semantic versioning (X.Y.Z)",
            severity="warning",
        ),
        ValidationRule(
            name="date_format",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            message="Date should be in ISO format (YYYY-MM-DD)",
            severity="warning",
        ),
        ValidationRule(
            name="entry_not_empty",
            pattern=r".{3,}",
            message="Entry description should not be empty or too short",
            severity="error",
        ),
    ]

    def add_validation_rule(self, rule: ValidationRule) -> None:
        """Add a custom validation rule."""
        if not hasattr(self, "_validation_rules"):
            self._validation_rules = self.DEFAULT_VALIDATION_RULES.copy()
        self._validation_rules.append(rule)

    def add_entry(
        self,
        category: str,
        description: str,
        priority: int = 0,
        severity: str = "normal",
        tags: Optional[List[str]] = None,
        linked_issues: Optional[List[str]] = None,
    ) -> ChangelogEntry:
        """Add a new changelog entry."""
        entry = ChangelogEntry(
            category=category,
            description=description,
            version=self.generate_next_version(),
            date=datetime.now().strftime("%Y-%m-%d"),
            priority=priority,
            severity=severity,
            tags=tags or [],
            linked_issues=linked_issues or [],
        )
        # Validate before adding
        issues = self.validate_entry(entry)
        if any(i["severity"] == "error" for i in issues):
            logging.error(f"Entry validation failed: {issues}")
            raise ValueError(f"Entry validation failed: {issues}")
        if not hasattr(self, "_entries"):
            self._entries = []
        self._entries.append(entry)
        return entry

    def get_entries_by_category(self, category: str) -> List[ChangelogEntry]:
        """Get all entries for a specific category."""
        return [e for e in getattr(self, "_entries", []) if e.category == category]

    def get_entries_by_priority(self, min_priority: int = 0) -> List[ChangelogEntry]:
        """Get entries with priority >= min_priority, sorted by priority."""
        filtered = [e for e in getattr(self, "_entries", []) if e.priority >= min_priority]
        return sorted(filtered, key=lambda e: e.priority, reverse=True)

    def deduplicate_entries(self) -> int:
        """Remove duplicate entries, returns count of removed."""
        if not hasattr(self, "_entries"):
            return 0
        seen: set[str] = set()
        unique_entries = []
        removed_count = 0
        for entry in self._entries:
            key = f"{entry.category}:{entry.description}"
            if key not in seen:
                seen.add(key)
                unique_entries.append(entry)
            else:
                removed_count += 1
        self._entries = unique_entries
        return removed_count

    def format_entries_as_markdown(self) -> str:
        """Format all entries as markdown changelog."""
        if not hasattr(self, "_entries") or not self._entries:
            return ""
        # Group by version
        by_version: dict[str, list[ChangelogEntry]] = {}
        for entry in self._entries:
            version = entry.version or "Unreleased"
            if version not in by_version:
                by_version[version] = []
            by_version[version].append(entry)
        result: list[str] = []
        for version, entries in by_version.items():
            date = entries[0].date if entries else datetime.now().strftime("%Y-%m-%d")
            result.append(f"## [{version}] - {date}\n")
            # Group by category
            by_category: dict[str, list[ChangelogEntry]] = {}
            for entry in entries:
                if entry.category not in by_category:
                    by_category[entry.category] = []
                by_category[entry.category].append(entry)
            sections = self.get_template_sections()
            for category in sections:
                if category in by_category:
                    result.append(f"### {category}\n")
                    for entry in by_category[category]:
                        line = f"- {entry.description}"
                        if entry.tags:
                            line += f" [{', '.join(entry.tags)}]"
                        if entry.linked_issues:
                            line += f" ({', '.join(entry.linked_issues)})"
                        result.append(line)
                    result.append("")
        return "\n".join(result)
