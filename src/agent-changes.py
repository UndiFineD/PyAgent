#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE - 2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Changes Agent: Improves and updates code file changelogs.

Reads a changes file (Codefile.changes.md), uses Copilot to enhance the changelog,
and updates the changes file with improvements.

## Description
This module provides a Changes Agent that reads existing code file changelogs,
uses AI assistance to improve and complete them, and updates the changes files
with enhanced documentation.

## Changelog
- 1.0.0: Initial implementation
- 1.1.0: Added changelog templates, preview mode, versioning strategies
- 1.2.0: Added merge detection, validation rules, statistics

## Suggested Fixes
- Add validation for changes file format
"""

from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import logging
import re
import json
import hashlib
from base_agent import BaseAgent, create_main_function


class VersioningStrategy(Enum):
    """Supported versioning strategies."""
    SEMVER = "semver"  # Semantic Versioning (MAJOR.MINOR.PATCH)
    CALVER = "calver"  # Calendar Versioning (YYYY.MM.DD)
    CUSTOM = "custom"  # Custom versioning pattern


@dataclass
class ChangelogTemplate:
    """Template for changelog entries."""
    name: str
    project_type: str
    sections: List[str] = field(default_factory=lambda: [
        "Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"
    ])
    header_format: str = "## [{version}] - {date}"
    include_links: bool = True
    include_contributors: bool = False


@dataclass
class ChangelogEntry:
    """A single changelog entry."""
    category: str
    description: str
    version: str = ""
    date: str = ""
    priority: int = 0  # Higher=more important
    severity: str = "normal"  # low, normal, high, critical
    tags: List[str] = field(default_factory=list)
    linked_issues: List[str] = field(default_factory=list)
    linked_commits: List[str] = field(default_factory=list)


@dataclass
class ValidationRule:
    """Rule for validating changelog entries."""
    name: str
    pattern: str
    message: str
    severity: str = "warning"  # warning, error


# ========== Session 6 Enums ==========


class LocalizationLanguage(Enum):
    """Supported languages for changelog localization."""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    JAPANESE = "ja"
    CHINESE = "zh"
    PORTUGUESE = "pt"


class DiffViewMode(Enum):
    """Modes for changelog diff visualization."""
    UNIFIED = "unified"
    SIDE_BY_SIDE = "side_by_side"
    INLINE = "inline"


class ImportSource(Enum):
    """External sources for changelog import."""
    GITHUB_RELEASES = "github_releases"
    JIRA = "jira"
    GITLAB = "gitlab"
    MANUAL = "manual"


class ComplianceCategory(Enum):
    """Categories for compliance checking."""
    SECURITY = "security"
    LEGAL = "legal"
    PRIVACY = "privacy"
    ACCESSIBILITY = "accessibility"


class FeedFormat(Enum):
    """Feed format types for RSS / Atom generation."""
    RSS_20 = "rss_20"
    ATOM_10 = "atom_10"
    JSON_FEED = "json_feed"


class GroupingStrategy(Enum):
    """Strategies for entry grouping."""
    BY_DATE = "by_date"
    BY_VERSION = "by_version"
    BY_CATEGORY = "by_category"
    BY_AUTHOR = "by_author"


# ========== Session 6 Dataclasses ==========


@dataclass
class LocalizedEntry:
    """A changelog entry with localization support.

    Attributes:
        original_text: Original entry text.
        language: Source language of the entry.
        translations: Dictionary of translations by language code.
        auto_translated: Whether translations were auto - generated.
    """
    original_text: str
    language: LocalizationLanguage = LocalizationLanguage.ENGLISH
    translations: Dict[str, str] = field(default_factory=dict)
    auto_translated: bool = False


@dataclass
class DiffResult:
    """Result of a changelog diff comparison.

    Attributes:
        additions: Lines added.
        deletions: Lines removed.
        modifications: Lines changed.
        unchanged: Lines unchanged.
        similarity_score: Percentage of similarity (0 - 100).
    """
    additions: List[str] = field(default_factory=list)
    deletions: List[str] = field(default_factory=list)
    modifications: List[Tuple[str, str]] = field(default_factory=list)
    unchanged: int = 0
    similarity_score: float = 0.0


@dataclass
class ImportedEntry:
    """An entry imported from external source.

    Attributes:
        source: Where the entry was imported from.
        external_id: ID in the external system.
        title: Entry title.
        description: Entry description.
        author: Author of the entry.
        created_at: When the entry was created.
        labels: Labels / tags from the source.
    """
    source: ImportSource
    external_id: str
    title: str
    description: str
    author: str = ""
    created_at: str = ""
    labels: List[str] = field(default_factory=list)


@dataclass
class SearchResult:
    """Result from changelog search.

    Attributes:
        version: Version where match was found.
        line_number: Line number of the match.
        context: Surrounding text context.
        match_score: Relevance score (0 - 1).
    """
    version: str
    line_number: int
    context: str
    match_score: float = 1.0


@dataclass
class LinkedReference:
    """A linked reference to commit or issue.

    Attributes:
        ref_type: Type of reference ('commit' or 'issue').
        ref_id: ID of the reference.
        url: URL to the reference.
        title: Title / description of the reference.
    """
    ref_type: str
    ref_id: str
    url: str = ""
    title: str = ""


@dataclass
class MonorepoEntry:
    """Changelog entry for monorepo aggregation.

    Attributes:
        package_name: Name of the package.
        version: Package version.
        entries: List of changelog entries for this package.
        path: Path to the package in the repo.
    """
    package_name: str
    version: str
    entries: List[ChangelogEntry] = field(default_factory=list)
    path: str = ""


@dataclass
class ReleaseNote:
    """Generated release notes.

    Attributes:
        version: Release version.
        title: Release title.
        summary: Brief summary.
        highlights: Key highlights.
        breaking_changes: List of breaking changes.
        full_changelog: Complete changelog text.
    """
    version: str
    title: str
    summary: str
    highlights: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    full_changelog: str = ""


@dataclass
class ComplianceResult:
    """Result of compliance checking.

    Attributes:
        category: Compliance category checked.
        passed: Whether the check passed.
        issues: List of compliance issues found.
        recommendations: Recommendations for fixing issues.
    """
    category: ComplianceCategory
    passed: bool
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class EntryTemplate:
    """Template for changelog entries with placeholders.

    Attributes:
        name: Template name.
        template_text: Template with placeholders.
        placeholders: List of placeholder names.
        description: Description of the template.
    """
    name: str
    template_text: str
    placeholders: List[str] = field(default_factory=list)
    description: str = ""


# ========== Session 6 Helper Classes ==========


class ChangelogLocalizer:
    """Handles changelog localization to multiple languages.

    Provides functionality to translate changelog entries to different
    languages for international users.

    Attributes:
        entries: List of localized entries.
        default_language: Default language for entries.

    Example:
        >>> localizer=ChangelogLocalizer()
        >>> entry=localizer.create_entry("Added new feature")
        >>> localizer.add_translation(entry, LocalizationLanguage.SPANISH, "Nueva característica")
    """

    def __init__(
            self,
            default_language: LocalizationLanguage = LocalizationLanguage.ENGLISH) -> None:
        """Initialize the changelog localizer.

        Args:
            default_language: Default language for entries.
        """
        self.entries: List[LocalizedEntry] = []
        self.default_language = default_language

    def create_entry(self, text: str) -> LocalizedEntry:
        """Create a new localized entry.

        Args:
            text: Original entry text.

        Returns:
            A new LocalizedEntry instance.
        """
        entry = LocalizedEntry(
            original_text=text,
            language=self.default_language
        )
        self.entries.append(entry)
        return entry

    def add_translation(
        self,
        entry: LocalizedEntry,
        language: LocalizationLanguage,
        translation: str
    ) -> None:
        """Add a translation to an entry.

        Args:
            entry: The entry to translate.
            language: Target language.
            translation: Translated text.
        """
        entry.translations[language.value] = translation

    def get_localized_changelog(self, language: LocalizationLanguage) -> str:
        """Get the changelog in a specific language.

        Args:
            language: Target language.

        Returns:
            Changelog text in the specified language.
        """
        result = []
        for entry in self.entries:
            if language.value in entry.translations:
                result.append(entry.translations[language.value])
            else:
                result.append(entry.original_text)
        return '\n'.join(result)


class DiffVisualizer:
    """Visualizes changelog differences with multiple view modes.

    Provides side - by - side and unified diff views for changelog
    comparison.

    Example:
        >>> visualizer=DiffVisualizer()
        >>> result=visualizer.compare("old content", "new content")
        >>> html=visualizer.render_html(result, DiffViewMode.SIDE_BY_SIDE)
    """

    def compare(self, old_content: str, new_content: str) -> DiffResult:
        """Compare two changelog versions.

        Args:
            old_content: Original changelog content.
            new_content: New changelog content.

        Returns:
            DiffResult with comparison details.
        """
        old_lines = set(old_content.split('\n'))
        new_lines = set(new_content.split('\n'))

        additions = list(new_lines - old_lines)
        deletions = list(old_lines - new_lines)
        unchanged = len(old_lines & new_lines)

        total = len(old_lines | new_lines)
        similarity = (unchanged / total * 100) if total > 0 else 100.0

        return DiffResult(
            additions=additions,
            deletions=deletions,
            unchanged=unchanged,
            similarity_score=similarity
        )

    def render_html(self, result: DiffResult, mode: DiffViewMode) -> str:
        """Render diff result as HTML.

        Args:
            result: DiffResult to render.
            mode: Visualization mode.

        Returns:
            HTML string representation of the diff.
        """
        if mode == DiffViewMode.SIDE_BY_SIDE:
            return self._render_side_by_side(result)
        elif mode == DiffViewMode.INLINE:
            return self._render_inline(result)
        return self._render_unified(result)

    def _render_unified(self, result: DiffResult) -> str:
        """Render unified diff view."""
        lines = []
        lines.append("<div class='diff-unified'>")
        for line in result.deletions:
            lines.append(f"<span class='deletion'>- {line}</span>")
        for line in result.additions:
            lines.append(f"<span class='addition'>+ {line}</span>")
        lines.append("</div>")
        return '\n'.join(lines)

    def _render_side_by_side(self, result: DiffResult) -> str:
        """Render side-by-side diff view."""
        return f"<div class='diff - side - by - side'>Deletions: {
            len(
                result.deletions)}, Additions: {
            len(
                result.additions)}</div>"

    def _render_inline(self, result: DiffResult) -> str:
        """Render inline diff view."""
        return f"<div class='diff - inline'>Changes: {len(result.deletions) +
                                                      len(result.additions)}</div>"


class ExternalImporter:
    """Imports changelog entries from external sources.

    Supports importing from GitHub releases, JIRA, and other sources.

    Attributes:
        imported_entries: List of imported entries.

    Example:
        >>> importer=ExternalImporter()
        >>> entries=importer.import_github_releases("owner", "repo")
    """

    def __init__(self) -> None:
        """Initialize the external importer."""
        self.imported_entries: List[ImportedEntry] = []

    def import_github_releases(self, owner: str, repo: str) -> List[ImportedEntry]:
        """Import entries from GitHub releases.

        Args:
            owner: Repository owner.
            repo: Repository name.

        Returns:
            List of imported entries.
        """
        # Placeholder for actual GitHub API integration
        entry = ImportedEntry(
            source=ImportSource.GITHUB_RELEASES,
            external_id=f"{owner}/{repo}",
            title="GitHub Release",
            description=f"Releases from {owner}/{repo}"
        )
        self.imported_entries.append(entry)
        return [entry]

    def import_jira(self, project_key: str) -> List[ImportedEntry]:
        """Import entries from JIRA.

        Args:
            project_key: JIRA project key.

        Returns:
            List of imported entries.
        """
        # Placeholder for actual JIRA API integration
        entry = ImportedEntry(
            source=ImportSource.JIRA,
            external_id=project_key,
            title="JIRA Import",
            description=f"Issues from {project_key}"
        )
        self.imported_entries.append(entry)
        return [entry]

    def convert_to_changelog_entries(self) -> List[ChangelogEntry]:
        """Convert imported entries to changelog entries.

        Returns:
            List of ChangelogEntry instances.
        """
        result = []
        for imported in self.imported_entries:
            result.append(ChangelogEntry(
                category="Added",
                description=imported.description,
                tags=imported.labels
            ))
        return result


class ChangelogSearcher:
    """Searches changelog content across project history.

    Provides search functionality for finding specific entries
    in changelog history.

    Example:
        >>> searcher=ChangelogSearcher()
        >>> results=searcher.search("bug fix", changelog_content)
    """

    def search(self, query: str, content: str) -> List[SearchResult]:
        """Search for query in changelog content.

        Args:
            query: Search query string.
            content: Changelog content to search.

        Returns:
            List of search results.
        """
        results = []
        lines = content.split('\n')
        current_version = "Unknown"

        for i, line in enumerate(lines, 1):
            # Track current version
            version_match = re.match(r"##\s*\[?(\d+\.\d+\.\d+|\d{4}\.\d{2}\.\d{2})\]?", line)
            if version_match:
                current_version = version_match.group(1)

            # Search for query
            if query.lower() in line.lower():
                results.append(SearchResult(
                    version=current_version,
                    line_number=i,
                    context=line.strip(),
                    match_score=self._calculate_score(query, line)
                ))

        return sorted(results, key=lambda r: r.match_score, reverse=True)

    def _calculate_score(self, query: str, text: str) -> float:
        """Calculate relevance score for a match.

        Args:
            query: Search query.
            text: Text containing the match.

        Returns:
            Score between 0 and 1.
        """
        query_lower = query.lower()
        text_lower = text.lower()

        # Exact match gets highest score
        if query_lower == text_lower:
            return 1.0

        # Word boundary match
        if re.search(rf'\b{re.escape(query_lower)}\b', text_lower):
            return 0.8

        # Substring match
        return 0.5


class ReferenceLinkManager:
    """Manages links to commits and issues in changelog entries.

    Provides functionality to add, validate, and format references
    to commits and issues.

    Attributes:
        references: Dictionary of references by entry ID.

    Example:
        >>> manager=ReferenceLinkManager()
        >>> manager.add_commit_reference("entry1", "abc123", "https://github.com/...")
    """

    def __init__(self) -> None:
        """Initialize the reference link manager."""
        self.references: Dict[str, List[LinkedReference]] = {}

    def add_commit_reference(
        self,
        entry_id: str,
        commit_sha: str,
        url: str = "",
        title: str = ""
    ) -> LinkedReference:
        """Add a commit reference to an entry.

        Args:
            entry_id: ID of the changelog entry.
            commit_sha: Git commit SHA.
            url: URL to the commit.
            title: Commit message / title.

        Returns:
            The created LinkedReference.
        """
        ref = LinkedReference(
            ref_type="commit",
            ref_id=commit_sha[:7],
            url=url,
            title=title
        )
        if entry_id not in self.references:
            self.references[entry_id] = []
        self.references[entry_id].append(ref)
        return ref

    def add_issue_reference(
        self,
        entry_id: str,
        issue_number: str,
        url: str = "",
        title: str = ""
    ) -> LinkedReference:
        """Add an issue reference to an entry.

        Args:
            entry_id: ID of the changelog entry.
            issue_number: Issue number.
            url: URL to the issue.
            title: Issue title.

        Returns:
            The created LinkedReference.
        """
        ref = LinkedReference(
            ref_type="issue",
            ref_id=f"#{issue_number}",
            url=url,
            title=title
        )
        if entry_id not in self.references:
            self.references[entry_id] = []
        self.references[entry_id].append(ref)
        return ref

    def format_references(self, entry_id: str) -> str:
        """Format references for display.

        Args:
            entry_id: ID of the changelog entry.

        Returns:
            Formatted string of references.
        """
        refs = self.references.get(entry_id, [])
        if not refs:
            return ""
        return " (" + ", ".join(f"[{r.ref_id}]({r.url})" if r.url else r.ref_id for r in refs) + ")"


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
        changelog_lines = []
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


class FeedGenerator:
    """Generates RSS / Atom feeds from changelog.

    Creates syndication feeds for changelog updates.

    Attributes:
        format: Feed format to generate.

    Example:
        >>> generator=FeedGenerator(FeedFormat.ATOM_10)
        >>> feed=generator.generate(entries, "My Project")
    """

    def __init__(self, format: FeedFormat = FeedFormat.ATOM_10) -> None:
        """Initialize the feed generator.

        Args:
            format: Feed format to use.
        """
        self.format = format

    def generate(self, entries: List[ChangelogEntry], project_name: str) -> str:
        """Generate feed from changelog entries.

        Args:
            entries: Changelog entries.
            project_name: Name of the project.

        Returns:
            Feed content as string.
        """
        if self.format == FeedFormat.RSS_20:
            return self._generate_rss(entries, project_name)
        elif self.format == FeedFormat.JSON_FEED:
            return self._generate_json(entries, project_name)
        return self._generate_atom(entries, project_name)

    def _generate_atom(self, entries: List[ChangelogEntry], project_name: str) -> str:
        """Generate Atom 1.0 feed."""
        lines = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<feed xmlns="http://www.w3.org / 2005 / Atom">',
            f'  <title>{project_name} Changelog</title>',
        ]
        for entry in entries[:20]:  # Limit to 20 entries
            lines.extend([
                '  <entry>',
                f'    <title>[{entry.category}] {entry.description[:50]}</title>',
                f'    <content>{entry.description}</content>',
                '  </entry>'
            ])
        lines.append('</feed>')
        return '\n'.join(lines)

    def _generate_rss(self, entries: List[ChangelogEntry], project_name: str) -> str:
        """Generate RSS 2.0 feed."""
        lines = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<rss version="2.0">',
            '  <channel>',
            f'    <title>{project_name} Changelog</title>',
        ]
        for entry in entries[:20]:
            lines.extend([
                '    <item>',
                f'      <title>{entry.description[:50]}</title>',
                f'      <description>{entry.description}</description>',
                '    </item>'
            ])
        lines.extend(['  </channel>', '</rss>'])
        return '\n'.join(lines)

    def _generate_json(self, entries: List[ChangelogEntry], project_name: str) -> str:
        """Generate JSON Feed."""
        items = [
            {"title": f"[{e.category}] {e.description[:50]}", "content_text": e.description}
            for e in entries[:20]
        ]
        feed = {
            "version": "https://jsonfeed.org / version / 1.1",
            "title": f"{project_name} Changelog",
            "items": items
        }
        return json.dumps(feed, indent=2)


class ComplianceChecker:
    """Checks changelog compliance with various requirements.

    Verifies changelog entries meet security, legal, and
    other compliance requirements.

    Example:
        >>> checker=ComplianceChecker()
        >>> results=checker.check_all(entries)
    """

    SECURITY_KEYWORDS = ["vulnerability", "cve", "security", "patch", "exploit"]
    LEGAL_KEYWORDS = ["license", "copyright", "trademark", "patent"]

    def check_security_compliance(self, entries: List[ChangelogEntry]) -> ComplianceResult:
        """Check security compliance.

        Args:
            entries: Changelog entries to check.

        Returns:
            ComplianceResult for security category.
        """
        issues = []
        recommendations = []

        # Check for security entries without proper categorization
        for entry in entries:
            if any(kw in entry.description.lower() for kw in self.SECURITY_KEYWORDS):
                if entry.category != "Security":
                    issues.append(
                        f"Security-related entry not in Security category: {entry.description[:50]}")
                    recommendations.append("Move security-related entries to the Security section")

        return ComplianceResult(
            category=ComplianceCategory.SECURITY,
            passed=len(issues) == 0,
            issues=issues,
            recommendations=recommendations
        )

    def check_legal_compliance(self, entries: List[ChangelogEntry]) -> ComplianceResult:
        """Check legal compliance.

        Args:
            entries: Changelog entries to check.

        Returns:
            ComplianceResult for legal category.
        """
        issues = []
        recommendations = []

        # Check for entries that may need legal review
        for entry in entries:
            if any(kw in entry.description.lower() for kw in self.LEGAL_KEYWORDS):
                issues.append(f"Entry may need legal review: {entry.description[:50]}")
                recommendations.append("Have legal team review license / copyright changes")

        return ComplianceResult(
            category=ComplianceCategory.LEGAL,
            passed=len(issues) == 0,
            issues=issues,
            recommendations=recommendations
        )

    def check_all(self, entries: List[ChangelogEntry]) -> List[ComplianceResult]:
        """Run all compliance checks.

        Args:
            entries: Changelog entries to check.

        Returns:
            List of ComplianceResult for all categories.
        """
        return [
            self.check_security_compliance(entries),
            self.check_legal_compliance(entries)
        ]


class EntryReorderer:
    """Reorders and groups changelog entries.

    Provides functionality to reorder entries by various criteria.

    Example:
        >>> reorderer=EntryReorderer()
        >>> sorted_entries=reorderer.reorder(entries, GroupingStrategy.BY_PRIORITY)
    """

    def reorder(
        self,
        entries: List[ChangelogEntry],
        strategy: GroupingStrategy
    ) -> List[ChangelogEntry]:
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

    def group_by_category(self, entries: List[ChangelogEntry]) -> Dict[str, List[ChangelogEntry]]:
        """Group entries by category.

        Args:
            entries: Entries to group.

        Returns:
            Dictionary mapping category to entries.
        """
        result: Dict[str, List[ChangelogEntry]] = {}
        for entry in entries:
            if entry.category not in result:
                result[entry.category] = []
            result[entry.category].append(entry)
        return result


class TemplateManager:
    """Manages entry templates with placeholders.

    Provides template storage and application functionality.

    Attributes:
        templates: Dictionary of templates by name.

    Example:
        >>> manager=TemplateManager()
        >>> manager.add_template("bug_fix", "Fixed {issue} in {component}")
        >>> text=manager.apply_template("bug_fix", {"issue": "#123", "component": "auth"})
    """

    def __init__(self) -> None:
        """Initialize the template manager."""
        self.templates: Dict[str, EntryTemplate] = {}

    def add_template(
        self,
        name: str,
        template_text: str,
        description: str = ""
    ) -> EntryTemplate:
        """Add a new template.

        Args:
            name: Template name.
            template_text: Template with placeholders.
            description: Template description.

        Returns:
            The created EntryTemplate.
        """
        # Extract placeholders
        placeholders = re.findall(r'\{(\w+)\}', template_text)

        template = EntryTemplate(
            name=name,
            template_text=template_text,
            placeholders=placeholders,
            description=description
        )
        self.templates[name] = template
        return template

    def apply_template(self, name: str, values: Dict[str, str]) -> str:
        """Apply a template with values.

        Args:
            name: Template name.
            values: Dictionary of placeholder values.

        Returns:
            Filled - in template text.
        """
        template = self.templates.get(name)
        if not template:
            return ""

        result = template.template_text
        for placeholder, value in values.items():
            result = result.replace(f"{{{placeholder}}}", value)
        return result

    def get_template_placeholders(self, name: str) -> List[str]:
        """Get placeholders for a template.

        Args:
            name: Template name.

        Returns:
            List of placeholder names.
        """
        template = self.templates.get(name)
        return template.placeholders if template else []


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
            name="Python Project",
            project_type="python",
            sections=["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"],
            include_contributors=True
        ),
        "javascript": ChangelogTemplate(
            name="JavaScript / Node.js Project",
            project_type="javascript",
            sections=["Features", "Bug Fixes", "Breaking Changes", "Documentation"],
        ),
        "generic": ChangelogTemplate(
            name="Generic Project",
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
        return super().update_file()

    # ========== Merge Detection ==========

    def detect_merge_conflicts(self, content: str) -> List[Dict[str, str]]:
        """Detect merge conflict markers in the content."""
        conflicts = []
        lines = content.split('\n')
        in_conflict = False
        conflict_start = 0
        ours = []
        theirs = []

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
        result = []
        lines = content.split('\n')
        in_conflict = False
        ours_section = True
        ours = []
        theirs = []

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
        issues = []

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
        all_issues = []

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
        categories = {}
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
            "total_entries": sum(categories.values()),
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
        seen = set()
        unique = []
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

        result = []
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
        # For other prompts, use the base implementation with enhanced prompt
        return super().improve_content(enhanced_prompt)


# Create main function using the helper
main = create_main_function(
    ChangesAgent,
    'Changes Agent: Updates code file changelogs',
    'Path to the changes file (e.g., file.changes.md)'
)


if __name__ == '__main__':
    main()
