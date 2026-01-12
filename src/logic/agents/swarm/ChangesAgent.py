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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_changes.py"""




from .ChangelogEntry import ChangelogEntry
from .ChangelogTemplate import ChangelogTemplate
from .ValidationRule import ValidationRule
from .VersioningStrategy import VersioningStrategy

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

class ChangesAgent(BaseAgent):
    """Updates code file changelogs using AI assistance.

    Features:
    - Changelog templates for different project types
    - Preview mode before committing changes
    - Multiple versioning strategies (SemVer, CalVer)
    - Merge conflict detection and resolution
    - Entry validation with customizable rules
    - Statistics and analytics
    """

    # Default templates for different project types
    DEFAULT_TEMPLATES: Dict[str, ChangelogTemplate] = {
        "python": ChangelogTemplate(
            name="Python",
            project_type="python",
            sections=["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"],
            include_contributors=True
        ),
        "javascript": ChangelogTemplate(
            name="JavaScript",
            project_type="javascript",
            sections=["Features", "Bug Fixes", "Breaking Changes", "Documentation"],
        ),
        "generic": ChangelogTemplate(
            name="Generic",
            project_type="generic",
            sections=["Added", "Changed", "Fixed", "Removed"],
        ),
    }

    # Default validation rules
    DEFAULT_VALIDATION_RULES: List[ValidationRule] = [
        ValidationRule(
            name="version_format",
            pattern=r"^\d+\.\d+\.\d+$",
            message="Version should follow semantic versioning (X.Y.Z)",
            severity="warning"
        ),
        ValidationRule(
            name="date_format",
            pattern=r"^\d{4}-\d{2}-\d{2}$",
            message="Date should be in ISO format (YYYY-MM-DD)",
            severity="warning"
        ),
        ValidationRule(
            name="entry_not_empty",
            pattern=r".{3,}",
            message="Entry description should not be empty or too short",
            severity="error"
        ),
    ]

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_file_extension()
        self._check_associated_file()
        self._template: Optional[ChangelogTemplate] = None
        self._versioning_strategy: VersioningStrategy = VersioningStrategy.SEMVER
        self._validation_rules: List[ValidationRule] = self.DEFAULT_VALIDATION_RULES.copy()
        self._preview_mode: bool = False
        self._preview_content: str = ""
        self._entries: List[ChangelogEntry] = []
        self._statistics: Dict[str, Any] = {}

    def _validate_file_extension(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith('.changes.md'):
            logging.warning(f"File {self.file_path.name} does not end with .changes.md")

    def _check_associated_file(self) -> None:
        """Check if the associated code file exists."""
        name = self.file_path.name
        if name.endswith('.changes.md'):
            base_name = name[:-11]  # len('.changes.md')
            # Try to find the file with common extensions or exact match
            candidate = self.file_path.parent / base_name
            if candidate.exists():
                return
            # Try adding extensions
            for ext in ['.py', '.sh', '.js', '.ts', '.md']:
                candidate = self.file_path.parent / (base_name + ext)
                if candidate.exists() and candidate != self.file_path:
                    return
            logging.warning(f"Could not find associated code file for {self.file_path.name}")

    # ========== Template Management ==========

    def set_template(self, template_name: str) -> None:
        """Set the changelog template by name."""
        if template_name in self.DEFAULT_TEMPLATES:
            self._template = self.DEFAULT_TEMPLATES[template_name]
            logging.info(f"Using template: {self._template.name}")
        else:
            logging.warning(f"Unknown template '{template_name}', using generic")
            self._template = self.DEFAULT_TEMPLATES["generic"]

    def create_custom_template(
        self,
        name: str,
        project_type: str,
        sections: List[str],
        header_format: str = "## [{version}] - {date}",
        include_links: bool = True,
        include_contributors: bool = False
    ) -> ChangelogTemplate:
        """Create a custom changelog template."""
        template = ChangelogTemplate(
            name=name,
            project_type=project_type,
            sections=sections,
            header_format=header_format,
            include_links=include_links,
            include_contributors=include_contributors
        )
        self._template = template
        return template

    def get_template_sections(self) -> List[str]:
        """Get the sections for the current template."""
        if self._template:
            return self._template.sections
        return ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]

    # ========== Versioning Strategies ==========

    def set_versioning_strategy(self, strategy: VersioningStrategy) -> None:
        """Set the versioning strategy."""
        self._versioning_strategy = strategy
        logging.info(f"Using versioning strategy: {strategy.value}")

    def generate_next_version(self, bump_type: str = "patch") -> str:
        """Generate the next version based on the current strategy.

        Args:
            bump_type: For SemVer: 'major', 'minor', 'patch'. For CalVer: ignored.
        """
        if self._versioning_strategy == VersioningStrategy.CALVER:
            return datetime.now().strftime("%Y.%m.%d")

        # SemVer: Try to extract current version and bump it
        current_version = self._extract_latest_version()
        if current_version:
            parts = current_version.split(".")
            if len(parts) >= 3:
                major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
                if bump_type == "major":
                    return f"{major + 1}.0.0"
                elif bump_type == "minor":
                    return f"{major}.{minor + 1}.0"
                else:  # patch
                    return f"{major}.{minor}.{patch + 1}"
        return "0.1.0"  # Default starting version

    def _extract_latest_version(self) -> Optional[str]:
        """Extract the latest version from the changelog."""
        pattern = r"##\s*\[?(\d+\.\d+\.\d+)\]?"
        matches = re.findall(pattern, self.previous_content)
        if matches:
            return matches[0]
        return None

    # ========== Preview Mode ==========

    def enable_preview_mode(self) -> None:
        """Enable preview mode - changes won't be written to file."""
        self._preview_mode = True
        logging.info("Preview mode enabled")

    def disable_preview_mode(self) -> None:
        """Disable preview mode."""
        self._preview_mode = False
        logging.info("Preview mode disabled")

    def get_preview(self) -> str:
        """Get the preview of changes without applying them."""
        return self._preview_content if self._preview_content else self.current_content

    def preview_changes(self, content: str) -> Dict[str, Any]:
        """Preview changes and return a summary."""
        self._preview_content = content

        # Calculate diff statistics
        original_lines = self.previous_content.split('\n')
        new_lines = content.split('\n')

        added = len([line for line in new_lines if line and line not in original_lines])
        removed = len([line for line in original_lines if line and line not in new_lines])

        return {
            "original_lines": len(original_lines),
            "new_lines": len(new_lines),
            "lines_added": added,
            "lines_removed": removed,
            "preview": content[:500] + "..." if len(content) > 500 else content
        }

    def update_file(self) -> bool:
        """Override update_file to support preview mode."""
        if self._preview_mode:
            logging.info("Preview mode: changes not written to file")
            return True

        return bool(super().update_file())

    # ========== Merge Detection ==========
    def detect_merge_conflicts(self, content: str) -> List[Dict[str, Any]]:
        """Detect merge conflict markers in the content."""
        conflicts: List[Dict[str, Any]] = []
        lines = content.split('\n')
        in_conflict = False
        conflict_start = 0
        ours: List[str] = []
        theirs: List[str] = []
        for i, line in enumerate(lines):
            if line.startswith('<<<<<<<'):
                in_conflict = True
                conflict_start = i
                ours = []
            elif line.startswith('=======') and in_conflict:
                pass  # Separator
            elif line.startswith('>>>>>>>') and in_conflict:
                conflicts.append({
                    "start_line": conflict_start,
                    "end_line": i,
                    "ours": '\n'.join(ours),
                    "theirs": '\n'.join(theirs)
                })
                in_conflict = False
                ours = []
                theirs = []
            elif in_conflict:
                if '=======' not in content[content.find('<<<<<<<'):content.find(line)]:
                    ours.append(line)
                else:
                    theirs.append(line)
        return conflicts

    def resolve_merge_conflict(
        self,
        content: str,
        resolution: str = "ours"
    ) -> str:
        """Resolve merge conflicts in the content.

        Args:
            content: Content with merge conflicts
            resolution: 'ours', 'theirs', or 'both'
        """
        result: List[str] = []
        lines = content.split('\n')
        in_conflict = False
        ours_section = True
        ours: List[str] = []
        theirs: List[str] = []

        for line in lines:
            if line.startswith('<<<<<<<'):
                in_conflict = True
                ours_section = True
                ours = []
                theirs = []
            elif line.startswith('=======') and in_conflict:
                ours_section = False
            elif line.startswith('>>>>>>>') and in_conflict:
                # Apply resolution
                if resolution == "ours":
                    result.extend(ours)
                elif resolution == "theirs":
                    result.extend(theirs)
                else:  # both
                    result.extend(ours)
                    result.extend(theirs)
                in_conflict = False
            elif in_conflict:
                if ours_section:
                    ours.append(line)
                else:
                    theirs.append(line)
            else:
                result.append(line)
        return '\n'.join(result)

    # ========== Entry Validation ==========
    def add_validation_rule(self, rule: ValidationRule) -> None:
        """Add a custom validation rule."""
        self._validation_rules.append(rule)

    def validate_entry(self, entry: ChangelogEntry) -> List[Dict[str, str]]:
        """Validate a changelog entry against all rules."""
        issues: List[Dict[str, str]] = []
        # Validate version format
        if entry.version:
            version_rule = next(
                (r for r in self._validation_rules if r.name == "version_format"),
                None
            )
            if version_rule and not re.match(version_rule.pattern, entry.version):
                issues.append({
                    "rule": version_rule.name,
                    "message": version_rule.message,
                    "severity": version_rule.severity
                })
        # Validate date format
        if entry.date:
            date_rule = next(
                (r for r in self._validation_rules if r.name == "date_format"),
                None
            )
            if date_rule and not re.match(date_rule.pattern, entry.date):
                issues.append({
                    "rule": date_rule.name,
                    "message": date_rule.message,
                    "severity": date_rule.severity
                })
        # Validate entry description
        entry_rule = next(
            (r for r in self._validation_rules if r.name == "entry_not_empty"),
            None
        )
        if entry_rule and not re.match(entry_rule.pattern, entry.description):
            issues.append({
                "rule": entry_rule.name,
                "message": entry_rule.message,
                "severity": entry_rule.severity
            })
        return issues

    def validate_changelog(self, content: str) -> List[Dict[str, Any]]:
        """Validate the entire changelog content."""
        all_issues: List[Dict[str, Any]] = []
        # Check for merge conflicts
        conflicts = self.detect_merge_conflicts(content)
        if conflicts:
            all_issues.append({
                "type": "merge_conflict",
                "count": len(conflicts),
                "severity": "error",
                "message": f"Found {len(conflicts)} unresolved merge conflict(s)"
            })
        # Check for required sections
        if self._template:
            for section in self._template.sections:
                if f"### {section}" not in content and f"## {section}" not in content:
                    all_issues.append({
                        "type": "missing_section",
                        "section": section,
                        "severity": "warning",
                        "message": f"Missing recommended section: {section}"
                    })
        return all_issues

    # ========== Statistics ==========
    def calculate_statistics(self) -> Dict[str, Any]:
        """Calculate statistics for the changelog."""
        content = self.current_content or self.previous_content
        # Count versions
        version_pattern = r"##\s*\[?(\d+\.\d+\.\d+|\d{4}\.\d{2}\.\d{2})\]?"
        versions = re.findall(version_pattern, content)
        # Count entries per category
        categories: Dict[str, int] = {}
        for section in ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]:
            pattern = rf"###\s*{section}\s*\n(.*?)(?=###|\Z)"
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                entries = [line for line in matches[0].split('\n') if line.strip().startswith('-')]
                categories[section] = len(entries)
        # Count contributors (if mentioned)
        contributor_pattern = r"@(\w+)"
        contributors = set(re.findall(contributor_pattern, content))
        self._statistics = {
            "version_count": len(versions),
            "latest_version": versions[0] if versions else None,
            "entries_by_category": categories,
            "total_entries": sum(categories.values()) if categories else 0,
            "contributor_count": len(contributors),
            "contributors": list(contributors),
            "line_count": len(content.split('\n')),
            "character_count": len(content)
        }
        return self._statistics

    # ========== Entry Management ==========
    def add_entry(
        self,
        category: str,
        description: str,
        priority: int = 0,
        severity: str = "normal",
        tags: Optional[List[str]] = None,
        linked_issues: Optional[List[str]] = None
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
            linked_issues=linked_issues or []
        )
        # Validate before adding
        issues = self.validate_entry(entry)
        if any(i["severity"] == "error" for i in issues):
            logging.error(f"Entry validation failed: {issues}")
            raise ValueError(f"Entry validation failed: {issues}")
        self._entries.append(entry)
        return entry

    def get_entries_by_category(self, category: str) -> List[ChangelogEntry]:
        """Get all entries for a specific category."""
        return [e for e in self._entries if e.category == category]

    def get_entries_by_priority(self, min_priority: int = 0) -> List[ChangelogEntry]:
        """Get entries with priority >= min_priority, sorted by priority."""
        filtered = [e for e in self._entries if e.priority >= min_priority]
        return sorted(filtered, key=lambda e: e.priority, reverse=True)

    def deduplicate_entries(self) -> int:
        """Remove duplicate entries, returns count of removed."""
        seen: set[str] = set()
        unique: list[ChangelogEntry] = []
        removed = 0
        for entry in self._entries:
            key = hashlib.md5(
                f"{entry.category}:{entry.description}".encode()
            ).hexdigest()
            if key not in seen:
                seen.add(key)
                unique.append(entry)
            else:
                removed += 1
        self._entries = unique
        return removed

    def format_entries_as_markdown(self) -> str:
        """Format all entries as markdown changelog."""
        if not self._entries:
            return ""
        # Group by version
        by_version: Dict[str, List[ChangelogEntry]] = {}
        for entry in self._entries:
            version = entry.version or "Unreleased"
            if version not in by_version:
                by_version[version] = []
            by_version[version].append(entry)
        result: List[str] = []
        for version, entries in by_version.items():
            date = entries[0].date if entries else datetime.now().strftime("%Y-%m-%d")
            result.append(f"## [{version}] - {date}\n")
            # Group by category
            by_category: Dict[str, List[ChangelogEntry]] = {}
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
        return '\n'.join(result)

    def _get_default_content(self) -> str:
        """Return default content for new changelog files."""
        return "# Changes\n\nNo changes recorded.\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original changelog preserved below:\n\n")

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the changelogs with specific change tracking suggestions."""
        logging.info(f"Improving changelog for {self.file_path}")
        # Add guidance for structured output
        enhanced_prompt = (
            f"{prompt}\n\n"
            "Please format the changelog using 'Keep a Changelog' conventions:\n"
            "## [Version] - YYYY - MM - DD\n"
            "### Added\n"
            "### Changed\n"
            "### Deprecated\n"
            "### Removed\n"
            "### Fixed\n"
            "### Security\n"
        )
        description = f"Improve the changelog for {self.file_path.stem.replace('.changes', '')}"
        # For changelog improvement, provide specific change tracking suggestions
        if any(keyword in prompt.lower() for keyword in ["improve", "change", "log"]):
            fallback_suggestions = f"""# AI Changelog Improvement Suggestions
# Description: {description}
#
# Suggestions:
# 1. Follow 'Keep a Changelog' format
# 2. Group changes by type (Added, Changed, Deprecated, Removed, Fixed, Security)
# 3. Include dates for versions
# 4. Be specific about changes
#
# Original changelog preserved below:
#
{self.previous_content}"""
            self.current_content = fallback_suggestions
            return self.current_content
        # For other prompts, call the BaseAgent's subagent path directly.
        #
        # This intentionally bypasses BaseAgent.improve_content() caching so
        # tests that monkeypatch base_agent.BaseAgent.run_subagent remain
        # deterministic even when earlier test runs have populated caches.
        from src.core.base.BaseAgent import entrypoint as _base_agent

        try:
            full_prompt = self._build_prompt_with_history(enhanced_prompt)
        except Exception:
            full_prompt = enhanced_prompt

        improvement = _base_agent.BaseAgent.run_subagent(self, description, full_prompt, self.previous_content)

        for processor in self._post_processors:
            improvement = processor(improvement)

        self.current_content = improvement
        return self.current_content
