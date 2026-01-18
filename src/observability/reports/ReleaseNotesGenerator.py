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
from src.core.base.Version import VERSION
from src.core.base.types import ChangelogEntry
from src.core.base.types import ReleaseNote

__version__ = VERSION


class ReleaseNotesGenerator:
    """Generates release notes from changelog entries.

    Creates formatted release notes suitable for publication.

    Example:
        >>> generator=ReleaseNotesGenerator()
        >>> notes=generator.generate("1.0.0", entries)
    """

    def generate(
        self, version: str, entries: list[ChangelogEntry], title: str | None = None
    ) -> ReleaseNote:
        """Generate release notes from entries.

        Args:
            version: Release version.
            entries: Changelog entries for this release.
            title: Optional release title.

        Returns:
            Generated ReleaseNote.
        """
        # Extract highlights (high priority or high severity)
        highlights = [
            e.description
            for e in entries
            if e.priority >= 2 or e.severity in ("high", "critical")
        ]

        # Extract breaking changes
        breaking = [
            e.description
            for e in entries
            if "breaking" in e.description.lower() or "breaking" in e.tags
        ]

        # Generate summary
        summary = f"Release {version} includes {len(entries)} changes"
        if breaking:
            summary += f" with {len(breaking)} breaking change(s)"

        # Format full changelog
        changelog_lines: list[str] = []
        by_category: dict[str, list[str]] = {}
        for entry in entries:
            if entry.category not in by_category:
                by_category[entry.category] = []
            by_category[entry.category].append(entry.description)

        for cat, descs in by_category.items():
            changelog_lines.append(f"### {cat}")
            for desc in descs:
                changelog_lines.append(f"- {desc}")
            changelog_lines.append("")

        return ReleaseNote(
            version=version,
            title=title or f"Release {version}",
            summary=summary,
            highlights=highlights[:5],  # Top 5 highlights
            breaking_changes=breaking,
            full_changelog="\n".join(changelog_lines),
        )
