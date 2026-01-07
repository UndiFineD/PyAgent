#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from .ChangelogEntry import ChangelogEntry
from .ReleaseNote import ReleaseNote

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

class ReleaseNotesGenerator:
    """Generates release notes from changelog entries.

    Creates formatted release notes suitable for publication.

    Example:
        >>> generator=ReleaseNotesGenerator()
        >>> notes=generator.generate("1.0.0", entries)
    """

    def generate(
        self,
        version: str,
        entries: List[ChangelogEntry],
        title: Optional[str] = None
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
            e.description for e in entries
            if e.priority >= 2 or e.severity in ("high", "critical")
        ]

        # Extract breaking changes
        breaking = [
            e.description for e in entries
            if "breaking" in e.description.lower() or "breaking" in e.tags
        ]

        # Generate summary
        summary = f"Release {version} includes {len(entries)} changes"
        if breaking:
            summary += f" with {len(breaking)} breaking change(s)"

        # Format full changelog
        changelog_lines: List[str] = []
        by_category: Dict[str, List[str]] = {}
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
            full_changelog='\n'.join(changelog_lines)
        )
