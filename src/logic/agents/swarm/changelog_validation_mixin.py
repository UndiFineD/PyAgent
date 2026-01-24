#!/usr/bin/env python3

"""
Changelog validation mixin.py module.
"""
# Copyright 2026 PyAgent Authors

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .changelog_entry import ChangelogEntry


class ChangelogValidationMixin:
    """Mixin for validating changelog entries and content."""

    def validate_entry(self, entry: ChangelogEntry) -> list[dict[str, str]]:
        """Validate a changelog entry against all rules."""
        issues: list[dict[str, str]] = []
        if not hasattr(self, "_validation_rules"):
            return issues

        # Validate version format
        if entry.version:
            v_rule = next((r for r in self._validation_rules if r.name == "version_format"), None)
            if v_rule and not re.match(v_rule.pattern, entry.version):
                issues.append({"rule": v_rule.name, "message": v_rule.message, "severity": v_rule.severity})

        # Validate date format
        if entry.date:
            d_rule = next((r for r in self._validation_rules if r.name == "date_format"), None)
            if d_rule and not re.match(d_rule.pattern, entry.date):
                issues.append({"rule": d_rule.name, "message": d_rule.message, "severity": d_rule.severity})

        # Validate entry description
        e_rule = next((r for r in self._validation_rules if r.name == "entry_not_empty"), None)
        if e_rule and not re.match(e_rule.pattern, entry.description):
            issues.append({"rule": e_rule.name, "message": e_rule.message, "severity": e_rule.severity})

        return issues

    def validate_changelog(self, content: str) -> list[dict[str, Any]]:
        """Validate the entire changelog content."""
        all_issues: list[dict[str, Any]] = []
        # Check for merge conflicts
        conflicts = self.detect_merge_conflicts(content)
        if conflicts:
            all_issues.append(
                {
                    "type": "merge_conflict",
                    "count": len(conflicts),
                    "severity": "error",
                    "message": f"Found {len(conflicts)} unresolved merge conflict(s)",
                }
            )

        # Check for required sections
        if hasattr(self, "_template") and self._template:
            for section in self._template.sections:
                if f"### {section}" not in content and f"## {section}" not in content:
                    all_issues.append(
                        {
                            "type": "missing_section",
                            "section": section,
                            "severity": "warning",
                            "message": f"Missing recommended section: {section}",
                        }
                    )
        return all_issues
