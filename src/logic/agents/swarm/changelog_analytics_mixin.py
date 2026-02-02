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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Changelog analytics mixin.py module.
"""

from __future__ import annotations

import re
from typing import Any


class ChangelogAnalyticsMixin:
    """Mixin for calculating statistics and analytics for changelogs."""

    def calculate_statistics(self) -> dict[str, Any]:
        """Calculate statistics for the changelog."""
        content = getattr(self, "current_content", "") or getattr(self, "previous_content", "")
        if not content:
            return {}

        # Count versions
        version_pattern = r"##\s*\[?(\d+\.\d+\.\d+|\d{4}\.\d{2}\.\d{2})\]?"
        versions = re.findall(version_pattern, content)

        # Count entries per category
        categories: dict[str, int] = {}
        for section in ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]:
            pattern = rf"###\s*{section}\s*\n(.*?)(?=###|\Z)"
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                entries = [line for line in matches[0].split("\n") if line.strip().startswith("-")]
                categories[section] = len(entries)

        # Count contributors
        contributor_pattern = r"@(\w+)"
        contributors = set(re.findall(contributor_pattern, content))

        stats = {
            "version_count": len(versions),
            "latest_version": versions[0] if versions else None,
            "entries_by_category": categories,
            "total_entries": sum(categories.values()) if categories else 0,
            "contributor_count": len(contributors),
            "contributors": list(contributors),
            "line_count": len(content.split("\n")),
            "character_count": len(content),
        }
        setattr(self, "_statistics", stats)
        return stats
