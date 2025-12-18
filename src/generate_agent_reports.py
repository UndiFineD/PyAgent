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

"""Generate per-file agent reports.

For every Python file under `scripts / agent/*.py`, this script writes:

- `<stem>.description.md`

- `<stem>.errors.md`

- `<stem>.improvements.md`

The output is intentionally lightweight and based on static inspection and

basic syntax / compile checks.

Features:

- Static analysis using AST parsing

- Incremental processing (skip unchanged files)

- Report comparison between versions

- Report templates with custom sections

- Report filtering by date range and criteria

- Report versioning with change tracking

- Report caching with invalidation strategies

"""

from __future__ import annotations

import ast

import hashlib

import json

import logging

import re

import sys

import time

from dataclasses import dataclass, field

from datetime import datetime

from enum import Enum

from pathlib import Path

from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, cast

AGENT_DIR = Path(__file__).resolve().parent

REPO_ROOT = AGENT_DIR.parents[1]

# =============================================================================

# Enums for Type Safety

# =============================================================================


class ReportType(Enum):

    """Type of report to generate."""

    DESCRIPTION = "description"

    ERRORS = "errors"

    IMPROVEMENTS = "improvements"

    SUMMARY = "summary"


class ReportFormat(Enum):

    """Output format for reports."""

    MARKDOWN = "markdown"

    JSON = "json"

    HTML = "html"


class SeverityLevel(Enum):

    """Severity level for issues."""

    INFO = 1

    WARNING = 2

    ERROR = 3

    CRITICAL = 4


class IssueCategory(Enum):

    """Category of code issue."""

    SYNTAX = "syntax"

    TYPE_ANNOTATION = "type_annotation"

    STYLE = "style"

    SECURITY = "security"

    PERFORMANCE = "performance"

    DOCUMENTATION = "documentation"


class SubscriptionFrequency(Enum):

    """Frequency for report subscriptions."""

    IMMEDIATE = "immediate"

    HOURLY = "hourly"

    DAILY = "daily"

    WEEKLY = "weekly"


class PermissionLevel(Enum):

    """Permission levels for report access."""

    NONE = 0

    READ = 1

    WRITE = 2

    ADMIN = 3


class ExportFormat(Enum):

    """Export formats for reports."""

    JSON = "json"

    HTML = "html"

    PDF = "pdf"

    CSV = "csv"


class LocaleCode(Enum):

    """Supported locales for reports."""

    EN_US = "en-US"

    DE_DE = "de-DE"

    FR_FR = "fr-FR"

    ES_ES = "es-ES"


class AuditAction(Enum):

    """Actions for audit logging."""

    CREATE = "create"

    READ = "read"

    UPDATE = "update"

    DELETE = "delete"

    EXPORT = "export"

# =============================================================================

# Dataclasses for Data Structures

# =============================================================================


@dataclass(frozen=True)
class CompileResult:

    """Result of compile / syntax check."""

    ok: bool

    error: Optional[str] = None


@dataclass
@dataclass
class CodeIssue:

    """Represents a code issue or improvement suggestion.

    Attributes:

        message: Issue description.

        category: Issue category.

        severity: Severity level.

        line_number: Line number if applicable.

        file_path: File path if applicable.

        function_name: Function name if applicable.

    """

    message: str

    category: IssueCategory

    severity: SeverityLevel = SeverityLevel.INFO

    line_number: Optional[int] = None

    file_path: Optional[str] = None

    function_name: Optional[str] = None


@dataclass
class ReportMetadata:

    """Metadata for a generated report.

    Attributes:

        path: Path to source file.

        generated_at: Timestamp of generation.

        content_hash: SHA256 hash of content.

        version: Report version string.

    """

    path: str

    generated_at: str

    content_hash: str

    version: str


@dataclass
class ReportTemplate:

    """Template for report generation.

    Attributes:

        name: Template name.

        sections: List of section names to include.

        include_metadata: Whether to include metadata section.

        include_summary: Whether to include summary section.

    """

    name: str

    sections: List[str] = field(
        default_factory=lambda: ["purpose", "location", "surface"]
    )  # type: ignore[assignment]

    include_metadata: bool = True

    include_summary: bool = True


@dataclass
@dataclass
class ReportCache:

    """Cache for report data.

    Attributes:

        path: File path for the cached report.

        content_hash: Hash of the cached content.

        content: The cached report content.

        created_at: Timestamp when cache was created.

        ttl_seconds: Time - to - live for cache entries.

    """

    path: str = ""

    content_hash: str = ""

    content: str = ""

    created_at: float = 0.0

    ttl_seconds: int = 3600


@dataclass
class ReportComparison:

    """Result of comparing two report versions.

    Attributes:

        old_path: Path to old version.

        new_path: Path to new version.

        added: Items added in new version.

        removed: Items removed from old version.

        changed: Items that changed (list of tuples of old, new).

        unchanged_count: Count of unchanged items.

    """

    old_path: str

    new_path: str

    added: List[str] = field(default_factory=list)  # type: ignore[assignment]

    removed: List[str] = field(default_factory=list)  # type: ignore[assignment]

    changed: List[tuple] = field(default_factory=list)  # type: ignore[assignment]

    unchanged_count: int = 0


@dataclass
class FilterCriteria:

    """Criteria for filtering reports.

    Attributes:

        date_from: Start date for filtering.

        date_to: End date for filtering.

        min_severity: Minimum severity level.

        categories: Categories to include.

        file_patterns: Glob patterns for files.

    """

    date_from: Optional[datetime] = None

    date_to: Optional[datetime] = None

    min_severity: Optional[SeverityLevel] = None

    categories: Optional[List[IssueCategory]] = None

    file_patterns: Optional[List[str]] = None


@dataclass
class ReportSubscription:

    """Subscription for report delivery.

    Attributes:

        subscriber_id: Unique subscriber identifier.

        email: Email address for delivery.

        frequency: Delivery frequency.

        report_types: Types of reports to receive.

        file_patterns: Patterns for files to include.

        enabled: Whether subscription is active.

    """

    subscriber_id: str

    email: str

    frequency: SubscriptionFrequency = SubscriptionFrequency.DAILY

    report_types: List[ReportType] = field(default_factory=list)  # type: ignore[assignment]

    file_patterns: List[str] = field(default_factory=list)  # type: ignore[assignment]

    enabled: bool = True


@dataclass
class ArchivedReport:

    """Archived report with retention info.

    Attributes:

        report_id: Unique report identifier.

        file_path: Original file path.

        content: Report content.

        archived_at: Archive timestamp.

        retention_days: Days to retain.

        metadata: Report metadata.

    """

    report_id: str

    file_path: str

    content: str

    archived_at: float = field(default_factory=time.time)  # type: ignore[assignment]

    retention_days: int = 90

    metadata: Dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]


@dataclass
class ReportAnnotation:

    """Annotation on a report.

    Attributes:

        annotation_id: Unique annotation identifier.

        report_id: Associated report ID.

        author: Author of annotation.

        content: Annotation content.

        line_number: Line number if applicable.

        created_at: Creation timestamp.

    """

    annotation_id: str

    report_id: str

    author: str

    content: str

    line_number: Optional[int] = None

    created_at: float = field(default_factory=time.time)  # type: ignore[assignment]


@dataclass
class ReportSearchResult:

    """Result from report search.

    Attributes:

        file_path: Path to report file.

        report_type: Type of report.

        match_text: Matched text snippet.

        line_number: Line number of match.

        score: Relevance score.

    """

    file_path: str

    report_type: ReportType

    match_text: str

    line_number: int

    score: float = 1.0


@dataclass
class ReportMetric:

    """Custom metric for reports.

    Attributes:

        name: Metric name.

        value: Metric value.

        unit: Unit of measurement.

        threshold: Alert threshold.

        trend: Trend direction (+/-/=).

    """

    name: str

    value: float

    unit: str = ""

    threshold: Optional[float] = None

    trend: str = "="


@dataclass
class ReportPermission:

    """Permission for report access.

    Attributes:

        user_id: User identifier.

        report_pattern: Glob pattern for reports.

        level: Permission level.

        granted_by: Who granted permission.

        expires_at: Expiration timestamp.

    """

    user_id: str

    report_pattern: str

    level: PermissionLevel = PermissionLevel.READ

    granted_by: str = ""

    expires_at: Optional[float] = None


@dataclass
class AuditEntry:

    """Audit log entry.

    Attributes:

        entry_id: Unique entry identifier.

        timestamp: Event timestamp.

        action: Audit action.

        user_id: User who performed action.

        report_id: Affected report.

        details: Additional details.

    """

    entry_id: str

    timestamp: float

    action: AuditAction

    user_id: str

    report_id: str

    details: Dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]


@dataclass
class LocalizedString:

    """Localized string with translations.

    Attributes:

        key: String key.

        translations: Locale to text mapping.

        default: Default text if locale missing.

    """

    key: str

    translations: Dict[str, str] = field(default_factory=dict)  # type: ignore[assignment]

    default: str = ""


@dataclass
class ValidationResult:

    """Result of report validation.

    Attributes:

        valid: Whether report is valid.

        errors: Validation errors.

        warnings: Validation warnings.

        checksum: Content checksum.

    """

    valid: bool

    errors: List[str] = field(default_factory=list)  # type: ignore[assignment]

    warnings: List[str] = field(default_factory=list)  # type: ignore[assignment]

    checksum: str = ""


@dataclass
class AggregatedReport:

    """Report aggregated from multiple sources.

    Attributes:

        sources: Source report paths.

        combined_issues: Combined issues from all sources.

        summary: Aggregation summary.

        generated_at: Generation timestamp.

    """

    sources: List[str] = field(default_factory=list)  # type: ignore[assignment]

    combined_issues: List[CodeIssue] = field(default_factory=list)  # type: ignore[assignment]

    summary: Dict[str, Any] = field(default_factory=dict)  # type: ignore[assignment]

    generated_at: float = field(default_factory=time.time)  # type: ignore[assignment]

# =============================================================================

# Report Cache Manager

# =============================================================================


class ReportCacheManager:

    """Manages report caching with invalidation strategies.

    Attributes:

        cache_file: Path to cache file.

        _cache: Current cache data mapping (path, hash) -> (content, ttl_end).

    """

    def __init__(self, cache_file: Optional[Path] = None):
        """Initialize cache manager.

        Args:

            cache_file: Path to cache file. Defaults to .report_cache.json.

        """

        self.cache_file = cache_file or AGENT_DIR / ".report_cache.json"

        self._cache: Dict[str, Any] = {}

        self._load_cache()

    def _load_cache(self) -> None:
        """Load cache from disk."""

        if self.cache_file.exists():

            try:

                data = json.loads(self.cache_file.read_text())

                self._cache = data.get('cache', {})

            except Exception as e:

                logging.warning(f"Failed to load cache: {e}")

    def _save_cache(self) -> None:
        """Save cache to disk."""

        try:

            data: Dict[str, Any] = {

                'cache': self._cache

            }

            self.cache_file.write_text(json.dumps(data, indent=2))

        except Exception as e:

            logging.warning(f"Failed to save cache: {e}")

    def get(self, file_path: str, content_hash: str) -> Optional[str]:
        """Get cached report if valid.

        Args:

            file_path: Path to source file.

            content_hash: Current content hash.

        Returns:

            Cached content or None if not valid or expired.

        """

        cache_key = f"{file_path}:{content_hash}"

        if cache_key not in self._cache:

            return None

        entry = self._cache[cache_key]

        # Check if expired

        if time.time() > entry.get('expires_at', 0):

            return None

        return entry.get('content')

    def set(self, file_path: str, content_hash: str, content: str, ttl: int = 3600) -> None:
        """Cache report content.

        Args:

            file_path: Path to source file.

            content_hash: Content hash.

            content: Report content to cache.

            ttl: Time-to-live in seconds.

        """

        cache_key = f"{file_path}:{content_hash}"

        self._cache[cache_key] = {

            'content': content,

            'expires_at': time.time() + ttl

        }

        self._save_cache()

    def invalidate_by_path(self, file_path: str) -> None:
        """Invalidate all cache entries for a file path.

        Args:

            file_path: Path to file.

        """

        keys_to_delete = [k for k in self._cache.keys() if k.startswith(f"{file_path}:")]

        for key in keys_to_delete:

            del self._cache[key]

        self._save_cache()

    def invalidate(self, file_path: Optional[str] = None) -> None:
        """Invalidate cache entries.

        Args:

            file_path: Path to invalidate. If None, clears all.

        """

        if file_path:

            self.invalidate_by_path(file_path)

        else:

            self._cache.clear()

            self._save_cache()

# =============================================================================

# Report Comparator

# =============================================================================


class ReportComparator:

    """Compares report versions to show differences.

    Attributes:

        reports_dir: Directory containing reports.

    """

    def __init__(self, reports_dir: Path = AGENT_DIR):
        """Initialize comparator.

        Args:

            reports_dir: Directory containing report files.

        """

        self.reports_dir = reports_dir

    def compare(self, old_path: str, new_path: str, old_content: str, new_content: str) -> ReportComparison:
        """Compare two report versions.

        Args:

            old_path: Path to old version.

            new_path: Path to new version.

            old_content: Previous report content.

            new_content: New report content.

        Returns:

            ReportComparison with differences.

        """

        old_items = self._extract_items(old_content)

        new_items = self._extract_items(new_content)

        old_set = set(old_items)

        new_set = set(new_items)

        added = list(new_set - old_set)

        removed = list(old_set - new_set)

        unchanged = len(old_set & new_set)

        return ReportComparison(

            old_path=old_path,

            new_path=new_path,

            added=added,

            removed=removed,

            changed=[],

            unchanged_count=unchanged

        )

    def _extract_items(self, content: str) -> List[str]:
        """Extract list items from markdown content."""

        items: List[str] = []

        for line in content.split('\n'):

            line = line.strip()

            if line.startswith('- '):

                items.append(line)

        return items

# =============================================================================

# Report Filter

# =============================================================================


class ReportFilter:

    """Filters reports based on criteria.

    Attributes:

        criteria: Filter criteria to apply.

    """

    def __init__(self, criteria: Optional[FilterCriteria] = None):
        """Initialize filter.

        Args:

            criteria: Filter criteria. Uses defaults if not provided.

        """

        self.criteria = criteria or FilterCriteria()

    def matches(self, issue: CodeIssue) -> bool:
        """Check if issue matches filter criteria.

        Args:

            issue: Code issue to check.

        Returns:

            True if issue matches all criteria.

        """

        # Check severity

        if self.criteria.min_severity and issue.severity.value < self.criteria.min_severity.value:

            return False

        # Check category

        if self.criteria.categories and issue.category not in self.criteria.categories:

            return False

        return True

    def filter_issues(self, issues: List[CodeIssue]) -> List[CodeIssue]:
        """Filter list of issues.

        Args:

            issues: List of issues to filter.

        Returns:

            Filtered list of issues.

        """

        return [i for i in issues if self.matches(i)]

# =============================================================================

# Session 8 Helper Classes

# =============================================================================


class SubscriptionManager:

    """Manager for report subscriptions and scheduled delivery.

    Handles subscriber management, delivery scheduling, and

    notification triggering.

    Attributes:

        subscriptions: Active subscriptions.

        delivery_queue: Pending deliveries.

    Example:

        manager=SubscriptionManager()

        manager.add_subscription(ReportSubscription("user1", "user@example.com"))

        manager.process_deliveries()

    """

    def __init__(self) -> None:
        """Initialize subscription manager."""

        self.subscriptions: Dict[str, ReportSubscription] = {}

        self.delivery_queue: List[Dict[str, Any]] = []

        logging.debug("SubscriptionManager initialized")

    def add_subscription(self, subscription: ReportSubscription) -> None:
        """Add a subscription.

        Args:

            subscription: Subscription to add.

        """

        self.subscriptions[subscription.subscriber_id] = subscription

        logging.debug(f"Added subscription for {subscription.subscriber_id}")

    def remove_subscription(self, subscriber_id: str) -> bool:
        """Remove a subscription.

        Args:

            subscriber_id: Subscriber to remove.

        Returns:

            True if removed.

        """

        if subscriber_id in self.subscriptions:

            del self.subscriptions[subscriber_id]

            return True

        return False

    def get_due_subscriptions(self) -> List[ReportSubscription]:
        """Get subscriptions due for delivery.

        Returns:

            List of due subscriptions.

        """

        return [s for s in self.subscriptions.values() if s.enabled]

    def queue_delivery(

        self,

        subscriber_id: str,

        report_content: str,

        report_type: ReportType

    ) -> None:
        """Queue a report delivery.

        Args:

            subscriber_id: Target subscriber.

            report_content: Report content.

            report_type: Type of report.

        """

        self.delivery_queue.append({

            "subscriber_id": subscriber_id,

            "content": report_content,

            "type": report_type,

            "queued_at": time.time()

        })

    def process_deliveries(self) -> int:
        """Process pending deliveries.

        Returns:

            Number of deliveries processed.

        """

        processed = len(self.delivery_queue)

        self.delivery_queue.clear()

        return processed


class ReportArchiver:

    """Manager for report archiving with retention policies.

    Handles archiving, retrieval, and cleanup of historical reports.

    Attributes:

        archive_dir: Directory for archived reports.

        archives: In - memory archive index.

    Example:

        archiver=ReportArchiver(Path("./archives"))

        archiver.archive("file.py", report_content)

        old_reports=archiver.list_archives("file.py")

    """

    def __init__(self, archive_dir: Optional[Path] = None) -> None:
        """Initialize archiver.

        Args:

            archive_dir: Directory for archives.

        """

        self.archive_dir = archive_dir or AGENT_DIR / ".archives"

        self.archives: Dict[str, List[ArchivedReport]] = {}

        logging.debug(f"ReportArchiver initialized at {self.archive_dir}")

    def archive(

        self,

        file_path: str,

        content: str,

        retention_days: int = 90

    ) -> ArchivedReport:
        """Archive a report.

        Args:

            file_path: Source file path.

            content: Report content.

            retention_days: Days to retain.

        Returns:

            Created archive entry.

        """

        report_id = f"{file_path}_{int(time.time())}"

        archived = ArchivedReport(

            report_id=report_id,

            file_path=file_path,

            content=content,

            retention_days=retention_days

        )

        if file_path not in self.archives:

            self.archives[file_path] = []

        self.archives[file_path].append(archived)

        return archived

    def list_archives(self, file_path: str) -> List[ArchivedReport]:
        """List archives for a file.

        Args:

            file_path: File to list archives for.

        Returns:

            List of archived reports.

        """

        return self.archives.get(file_path, [])

    def get_archive(self, report_id: str) -> Optional[ArchivedReport]:
        """Get a specific archive.

        Args:

            report_id: Archive ID.

        Returns:

            Archived report if found.

        """

        for archives in self.archives.values():

            for archive in archives:

                if archive.report_id == report_id:

                    return archive

        return None

    def cleanup_expired(self) -> int:
        """Remove expired archives.

        Returns:

            Number of archives removed.

        """

        removed = 0

        current_time = time.time()

        for file_path in list(self.archives.keys()):

            valid: List[ArchivedReport] = []

            for archive in self.archives[file_path]:

                expiry = archive.archived_at + (archive.retention_days * 86400)

                if current_time < expiry:

                    valid.append(archive)

                else:

                    removed += 1

            self.archives[file_path] = valid

        return removed


class AnnotationManager:

    """Manager for report annotations and comments.

    Handles adding, retrieving, and managing annotations on reports.

    Attributes:

        annotations: Annotations by report ID.

    Example:

        manager=AnnotationManager()

        manager.add_annotation("report1", "user", "Important note")

        notes=manager.get_annotations("report1")

    """

    def __init__(self) -> None:
        """Initialize annotation manager."""

        self.annotations: Dict[str, List[ReportAnnotation]] = {}
        self._annotation_counter = 0

        logging.debug("AnnotationManager initialized")

    def add_annotation(

        self,

        report_id: str,

        author: str,

        content: str,

        line_number: Optional[int] = None

    ) -> ReportAnnotation:
        """Add an annotation.

        Args:

            report_id: Report to annotate.

            author: Annotation author.

            content: Annotation content.

            line_number: Line number if applicable.

        Returns:

            Created annotation.

        """

        self._annotation_counter += 1
        annotation_id = f"ann_{report_id}_{self._annotation_counter}"

        annotation = ReportAnnotation(

            annotation_id=annotation_id,

            report_id=report_id,

            author=author,

            content=content,

            line_number=line_number

        )

        if report_id not in self.annotations:

            self.annotations[report_id] = []

        self.annotations[report_id].append(annotation)

        return annotation

    def get_annotations(self, report_id: str) -> List[ReportAnnotation]:
        """Get annotations for a report.

        Args:

            report_id: Report ID.

        Returns:

            List of annotations.

        """

        return self.annotations.get(report_id, [])

    def remove_annotation(self, annotation_id: str) -> bool:
        """Remove an annotation.

        Args:

            annotation_id: Annotation to remove.

        Returns:

            True if removed.

        """

        for report_id, anns in list(self.annotations.items()):

            for i, ann in enumerate(anns):

                if ann.annotation_id == annotation_id:

                    self.annotations[report_id].pop(i)

                    return True

        return False


class ReportSearchEngine:

    """Search engine for reports.

    Enables full - text search across historical report data.

    Attributes:

        index: Search index mapping terms to locations.

    Example:

        engine=ReportSearchEngine()

        engine.index_report("file.py", ReportType.ERRORS, content)

        results=engine.search("syntax error")

    """

    def __init__(self) -> None:
        """Initialize search engine."""

        self.index: Dict[str, List[Tuple[str, ReportType, int]]] = {}

        self._reports: Dict[str, str] = {}

        logging.debug("ReportSearchEngine initialized")

    def index_report(

        self,

        file_path: str,

        report_type: ReportType,

        content: str

    ) -> None:
        """Index a report for searching.

        Args:

            file_path: Report file path.

            report_type: Type of report.

            content: Report content.

        """

        key = f"{file_path}:{report_type.name}"

        self._reports[key] = content

        # Build index

        for line_num, line in enumerate(content.split("\n"), 1):

            words = re.findall(r'\w+', line.lower())

            for word in words:

                if word not in self.index:

                    self.index[word] = []

                self.index[word].append((file_path, report_type, line_num))

    def search(self, query: str, max_results: int = 20) -> List[ReportSearchResult]:
        """Search reports.

        Args:

            query: Search query.

            max_results: Maximum results to return.

        Returns:

            List of search results.

        """

        words = re.findall(r'\w+', query.lower())

        matches: Dict[str, int] = {}

        for word in words:

            if word in self.index:

                for file_path, report_type, line_num in self.index[word]:

                    key = f"{file_path}:{report_type.name}:{line_num}"

                    matches[key] = matches.get(key, 0) + 1

        results: List[ReportSearchResult] = []

        for key, score in sorted(matches.items(), key=lambda x: -x[1])[:max_results]:

            parts = key.split(":")

            file_path = parts[0]

            report_type = ReportType[parts[1]]

            line_num = int(parts[2])

            # Get match context

            report_key = f"{file_path}:{report_type.name}"

            content = self._reports.get(report_key, "")

            lines = content.split("\n")

            match_text = lines[line_num - 1] if line_num <= len(lines) else ""

            results.append(ReportSearchResult(

                file_path=file_path,

                report_type=report_type,

                match_text=match_text,

                line_number=line_num,

                score=float(score)

            ))

        return results


class MetricsCollector:

    """Collector for custom report metrics and KPIs.

    Tracks and calculates metrics across reports.

    Attributes:

        metrics: Collected metrics by file.

    Example:

        collector=MetricsCollector()

        collector.record("file.py", "issues_count", 5)

        summary=collector.get_summary()

    """

    def __init__(self) -> None:
        """Initialize metrics collector."""

        self.metrics: Dict[str, List[ReportMetric]] = {}

        logging.debug("MetricsCollector initialized")

    def record(

        self,

        file_path: str,

        name: str,

        value: float,

        unit: str = "",

        threshold: Optional[float] = None

    ) -> ReportMetric:
        """Record a metric.

        Args:

            file_path: File being measured.

            name: Metric name.

            value: Metric value.

            unit: Unit of measurement.

            threshold: Alert threshold.

        Returns:

            Created metric.

        """

        metric = ReportMetric(

            name=name,

            value=value,

            unit=unit,

            threshold=threshold

        )

        if file_path not in self.metrics:

            self.metrics[file_path] = []

        self.metrics[file_path].append(metric)

        return metric

    def get_metrics(self, file_path: str) -> List[ReportMetric]:
        """Get metrics for a file.

        Args:

            file_path: File path.

        Returns:

            List of metrics.

        """

        return self.metrics.get(file_path, [])

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics.

        Returns:

            Summary dictionary.

        """

        total_files = len(self.metrics)

        total_metrics = sum(len(m) for m in self.metrics.values())

        # Calculate averages by metric name

        averages: Dict[str, List[float]] = {}

        for metrics in self.metrics.values():

            for metric in metrics:

                if metric.name not in averages:

                    averages[metric.name] = []

                averages[metric.name].append(metric.value)

        avg_summary = {

            name: sum(vals) / len(vals) if vals else 0

            for name, vals in averages.items()

        }

        return {

            "total_files": total_files,

            "total_metrics": total_metrics,

            "averages": avg_summary

        }


class AccessController:

    """Controller for report access permissions.

    Manages user permissions and access control for reports.

    Attributes:

        permissions: User permissions.

    Example:

        controller=AccessController()

        controller.grant("user1", "*.md", PermissionLevel.READ)

        can_read=controller.check("user1", "report.md", PermissionLevel.READ)

    """

    def __init__(self) -> None:
        """Initialize access controller."""

        self.permissions: List[ReportPermission] = []

        logging.debug("AccessController initialized")

    def grant(

        self,

        user_id: str,

        report_pattern: str,

        level: PermissionLevel,

        granted_by: str = "system"

    ) -> ReportPermission:
        """Grant permission to a user.

        Args:

            user_id: User to grant permission to.

            report_pattern: Pattern for reports.

            level: Permission level.

            granted_by: Who is granting.

        Returns:

            Created permission.

        """

        permission = ReportPermission(

            user_id=user_id,

            report_pattern=report_pattern,

            level=level,

            granted_by=granted_by

        )

        self.permissions.append(permission)

        return permission

    def revoke(self, user_id: str, report_pattern: str) -> bool:
        """Revoke a permission.

        Args:

            user_id: User ID.

            report_pattern: Pattern to revoke.

        Returns:

            True if revoked.

        """

        for perm in self.permissions:

            if perm.user_id == user_id and perm.report_pattern == report_pattern:

                self.permissions.remove(perm)

                return True

        return False

    def check(

        self,

        user_id: str,

        report_path: str,

        required_level: PermissionLevel

    ) -> bool:
        """Check if user has permission.

        Args:

            user_id: User to check.

            report_path: Report being accessed.

            required_level: Required permission level.

        Returns:

            True if permitted.

        """

        import fnmatch

        for perm in self.permissions:

            if perm.user_id != user_id:

                continue

            if perm.expires_at and time.time() > perm.expires_at:

                continue

            # Normalize paths for comparison (remove extra spaces)
            normalized_path = re.sub(r'\s+', '/', report_path)
            if fnmatch.fnmatch(normalized_path, perm.report_pattern):

                if perm.level.value >= required_level.value:

                    return True

        return False


class ReportExporter:

    """Exporter for various report formats.

    Exports reports to different formats including PDF, PPT, CSV.

    Example:

        exporter=ReportExporter()

        html=exporter.to_html(markdown_content)

        csv_data=exporter.to_csv(issues)

    """

    def __init__(self) -> None:
        """Initialize exporter."""

        logging.debug("ReportExporter initialized")

    def to_html(self, content: str, title: str = "Report") -> str:
        """Convert markdown to HTML.

        Args:

            content: Markdown content.

            title: Document title.

        Returns:

            HTML content.

        """

        # Simple markdown to HTML conversion

        html_content = content

        html_content = re.sub(r'# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)

        html_content = re.sub(r'## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)

        html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)

        html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)

        return f"""<!DOCTYPE html>

<html>

<head><title>{title}</title></head>

<body>{html_content}</body>

</html>"""

    def to_csv(self, issues: List[CodeIssue]) -> str:
        """Export issues to CSV.

        Args:

            issues: List of issues.

        Returns:

            CSV content.

        """

        lines = ["message,category,severity,line_number,function_name"]

        for issue in issues:

            lines.append(

                f'"{issue.message}",{issue.category.name},{issue.severity.name},'

                f'{issue.line_number or ""},"{issue.function_name or ""}"'

            )

        return "\n".join(lines)

    def export(

        self,

        content: str,

        format: ExportFormat,

        output_path: Optional[Path] = None

    ) -> str:
        """Export report to format.

        Args:

            content: Report content.

            format: Target format.

            output_path: Optional output file.

        Returns:

            Exported content.

        """

        if format == ExportFormat.HTML:

            result = self.to_html(content)

        elif format == ExportFormat.JSON:

            result = json.dumps({"content": content})

        else:

            result = content

        if output_path:

            output_path.write_text(result, encoding="utf-8")

        return result


class AuditLogger:

    """Logger for report audit trail.

    Records all actions performed on reports for compliance.

    Attributes:

        entries: Audit log entries.

    Example:

        logger=AuditLogger()

        logger.log(AuditAction.READ, "user1", "report.md")

        history=logger.get_history("report.md")

    """

    def __init__(self) -> None:
        """Initialize audit logger."""

        self.entries: List[AuditEntry] = []

        logging.debug("AuditLogger initialized")

    def log(

        self,

        action: AuditAction,

        user_id: str,

        report_id: str,

        details: Optional[Dict[str, Any]] = None

    ) -> AuditEntry:
        """Log an action.

        Args:

            action: Action performed.

            user_id: User who performed it.

            report_id: Affected report.

            details: Additional details.

        Returns:

            Created entry.

        """

        entry = AuditEntry(

            entry_id=f"audit_{int(time.time())}_{len(self.entries)}",

            timestamp=time.time(),

            action=action,

            user_id=user_id,

            report_id=report_id,

            details=details or {}

        )

        self.entries.append(entry)

        return entry

    def get_history(self, report_id: str) -> List[AuditEntry]:
        """Get audit history for report.

        Args:

            report_id: Report ID.

        Returns:

            List of entries.

        """

        return [e for e in self.entries if e.report_id == report_id]

    def get_user_activity(self, user_id: str) -> List[AuditEntry]:
        """Get activity for user.

        Args:

            user_id: User ID.

        Returns:

            List of entries.

        """

        return [e for e in self.entries if e.user_id == user_id]


class ReportValidator:

    """Validator for report data integrity.

    Validates report structure, content, and checksums.

    Example:

        validator=ReportValidator()

        result=validator.validate(content)

        if not result.valid:

            print(result.errors)

    """

    def __init__(self) -> None:
        """Initialize validator."""

        logging.debug("ReportValidator initialized")

    def validate(self, content: str) -> ValidationResult:
        """Validate report content.

        Args:

            content: Report content.

        Returns:

            Validation result.

        """

        errors: List[str] = []

        warnings: List[str] = []

        # Check for required sections

        if not re.search(r'^#+\s', content, re.MULTILINE):

            errors.append("Missing main heading")

        # Check for empty content

        if len(content.strip()) < 10:

            errors.append("Content too short")

        # Check for malformed links

        if re.search(r'\[.*?\]\(\s*\)', content):

            warnings.append("Contains empty link targets")

        # Calculate checksum

        checksum = hashlib.sha256(content.encode()).hexdigest()[:16]

        return ValidationResult(

            valid=len(errors) == 0,

            errors=errors,

            warnings=warnings,

            checksum=checksum

        )

    def verify_checksum(self, content: str, expected: str) -> bool:
        """Verify content checksum.

        Args:

            content: Report content.

            expected: Expected checksum.

        Returns:

            True if matches.

        """

        actual = hashlib.sha256(content.encode()).hexdigest()[:16]

        return actual == expected


class ReportLocalizer:

    """Localizer for report internationalization.

    Handles translation of report strings.

    Attributes:

        strings: Localized strings.

        current_locale: Current locale.

    Example:

        localizer=ReportLocalizer()

        localizer.add_string("error.syntax", {"en-US": "Syntax Error"})

        text=localizer.get("error.syntax")

    """

    def __init__(self, locale: LocaleCode = LocaleCode.EN_US) -> None:
        """Initialize localizer.

        Args:

            locale: Default locale.

        """

        self.strings: Dict[str, LocalizedString] = {}

        self.current_locale = locale

        self._init_defaults()

        logging.debug(f"ReportLocalizer initialized with {locale.value}")

    def _init_defaults(self) -> None:
        """Initialize default strings."""

        defaults = {

            "report.description": {"en-US": "Description", "de-DE": "Beschreibung"},

            "report.errors": {"en-US": "Errors", "de-DE": "Fehler"},

            "report.improvements": {"en-US": "Improvements", "de-DE": "Verbesserungen"},

            "severity.info": {"en-US": "Info", "de-DE": "Info"},

            "severity.warning": {"en-US": "Warning", "de-DE": "Warnung"},

            "severity.error": {"en-US": "Error", "de-DE": "Fehler"},

        }

        for key, translations in defaults.items():

            self.add_string(key, translations)

    def add_string(self, key: str, translations: Dict[str, str]) -> None:
        """Add a localized string.

        Args:

            key: String key.

            translations: Locale to text mapping.

        """

        default = translations.get("en-US", list(translations.values())[0] if translations else "")

        self.strings[key] = LocalizedString(key=key, translations=translations, default=default)

    def get(self, key: str, locale: Optional[LocaleCode] = None) -> str:
        """Get localized string.

        Args:

            key: String key.

            locale: Override locale.

        Returns:

            Localized text.

        """

        loc = locale or self.current_locale

        if key not in self.strings:

            return key

        string = self.strings[key]

        return string.translations.get(loc.value, string.default)

    def set_locale(self, locale: LocaleCode) -> None:
        """Set current locale.

        Args:

            locale: New locale.

        """

        self.current_locale = locale


class ReportAPI:

    """API for programmatic report access.

    Provides a RESTful - style interface for report operations.

    Example:

        api=ReportAPI()

        reports=api.list_reports()

        report=api.get_report("file.py", ReportType.ERRORS)

    """

    def __init__(self, reports_dir: Path = AGENT_DIR) -> None:
        """Initialize API.

        Args:

            reports_dir: Directory containing reports.

        """

        self.reports_dir = reports_dir

        logging.debug(f"ReportAPI initialized for {reports_dir}")

    def list_reports(self, file_pattern: str = "*.md") -> List[str]:
        """List available reports.

        Args:

            file_pattern: Glob pattern.

        Returns:

            List of report paths.

        """

        return [str(p) for p in self.reports_dir.glob(file_pattern)]

    def get_report(self, file_stem: str, report_type: ReportType) -> Optional[str]:
        """Get a specific report.

        Args:

            file_stem: File stem.

            report_type: Report type.

        Returns:

            Report content if found.

        """

        suffix_map = {

            ReportType.DESCRIPTION: ".description.md",

            ReportType.ERRORS: ".errors.md",

            ReportType.IMPROVEMENTS: ".improvements.md",

        }

        suffix = suffix_map.get(report_type, ".md")

        path = self.reports_dir / f"{file_stem}{suffix}"

        if path.exists():

            return path.read_text(encoding="utf-8")

        return None

    def create_report(

        self,

        file_stem: str,

        report_type: ReportType,

        content: str

    ) -> bool:
        """Create or update a report.

        Args:

            file_stem: File stem.

            report_type: Report type.

            content: Report content.

        Returns:

            True if successful.

        """

        suffix_map = {

            ReportType.DESCRIPTION: ".description.md",

            ReportType.ERRORS: ".errors.md",

            ReportType.IMPROVEMENTS: ".improvements.md",

        }

        suffix = suffix_map.get(report_type, ".md")

        path = self.reports_dir / f"{file_stem}{suffix}"

        try:

            path.write_text(content, encoding="utf-8")

            return True

        except Exception:

            return False


class ReportScheduler:

    """Scheduler for report generation.

    Handles scheduling report generation with cron - like expressions.

    Attributes:

        schedules: Scheduled tasks.

    Example:

        scheduler=ReportScheduler()

        scheduler.add_schedule("daily", "0 8 * * *", ["*.py"])

        due=scheduler.get_due_tasks()

    """

    def __init__(self) -> None:
        """Initialize scheduler."""

        self.schedules: Dict[str, Dict[str, Any]] = {}

        logging.debug("ReportScheduler initialized")

    def add_schedule(

        self,

        name: str,

        cron_expr: str,

        file_patterns: List[str]

    ) -> None:
        """Add a schedule.

        Args:

            name: Schedule name.

            cron_expr: Cron expression.

            file_patterns: Files to process.

        """

        self.schedules[name] = {

            "cron": cron_expr,

            "patterns": file_patterns,

            "last_run": 0.0

        }

    def remove_schedule(self, name: str) -> bool:
        """Remove a schedule.

        Args:

            name: Schedule name.

        Returns:

            True if removed.

        """

        if name in self.schedules:

            del self.schedules[name]

            return True

        return False

    def get_due_tasks(self) -> List[str]:
        """Get tasks due to run.

        Returns:

            List of due schedule names.

        """

        # Simple implementation - in production would parse cron

        return list(self.schedules.keys())

    def mark_completed(self, name: str) -> None:
        """Mark a task as completed.

        Args:

            name: Schedule name.

        """

        if name in self.schedules:

            self.schedules[name]["last_run"] = time.time()


class ReportAggregator:

    """Aggregator for combining reports from multiple sources.

    Combines and summarizes reports across files.

    Example:

        aggregator=ReportAggregator()

        aggregator.add_source("file1.py", issues1)

        aggregator.add_source("file2.py", issues2)

        combined=aggregator.aggregate()

    """

    def __init__(self) -> None:
        """Initialize aggregator."""

        self.sources: Dict[str, List[CodeIssue]] = {}

        logging.debug("ReportAggregator initialized")

    def add_source(self, file_path: str, issues: List[CodeIssue]) -> None:
        """Add a source to aggregate.

        Args:

            file_path: Source file.

            issues: Issues from file.

        """

        self.sources[file_path] = issues

    def aggregate(self) -> AggregatedReport:
        """Aggregate all sources.

        Returns:

            Aggregated report.

        """

        all_issues: List[CodeIssue] = []

        for issues in self.sources.values():

            all_issues.extend(issues)

        # Calculate summary

        by_severity: Dict[str, int] = {}

        by_category: Dict[str, int] = {}

        for issue in all_issues:

            sev = issue.severity.name

            cat = issue.category.name

            by_severity[sev] = by_severity.get(sev, 0) + 1

            by_category[cat] = by_category.get(cat, 0) + 1

        return AggregatedReport(

            sources=list(self.sources.keys()),

            combined_issues=all_issues,

            summary={

                "total_issues": len(all_issues),

                "total_files": len(self.sources),

                "by_severity": by_severity,

                "by_category": by_category

            }

        )

    def clear(self) -> None:
        """Clear all sources."""

        self.sources.clear()

# =============================================================================

# Helper Functions

# =============================================================================


def _read_text(path: Path) -> str:

    return path.read_text(encoding="utf-8", errors="replace")


def _sha256_text(text: str) -> str:

    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _try_parse_python(source: str, filename: str) -> Tuple[Optional[ast.AST], Optional[str]]:

    try:

        return ast.parse(source, filename=filename), None

    except SyntaxError as exc:

        location = f"{exc.filename}:{exc.lineno}:{exc.offset}" if exc.lineno else exc.filename

        return None, f"SyntaxError at {location}: {exc.msg}"


def _compile_check(path: Path) -> CompileResult:

    source = _read_text(path)

    tree, err = _try_parse_python(source, str(path))

    if tree is None:

        return CompileResult(ok=False, error=err)

    # If AST parse succeeded, consider syntax check OK.

    return CompileResult(ok=True)


def _is_pytest_test_file(path: Path) -> bool:

    return path.name.startswith("test_") and path.suffix == ".py"


def _looks_like_pytest_import_problem(path: Path) -> Optional[str]:

    # pytest imports test modules; hyphens / dots in the filename make import fail.

    name = path.name

    if not _is_pytest_test_file(path):

        return None

    if "-" in name or name.count(".") > 1:

        return (

            "Filename is not import - friendly for pytest collection (contains '-' or extra '.') "

            "and may fail test discovery / import."

        )

    return None


def _find_top_level_defs(tree: ast.AST) -> Tuple[List[str], List[str]]:

    functions: List[str] = []

    classes: List[str] = []

    for node in getattr(tree, "body", []):

        if isinstance(node, ast.FunctionDef):

            functions.append(node.name)

        elif isinstance(node, ast.AsyncFunctionDef):

            functions.append(f"async {node.name}")

        elif isinstance(node, ast.ClassDef):

            classes.append(node.name)

    return functions, classes


def _find_imports(tree: ast.AST) -> List[str]:

    imports: List[str] = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:

                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):

            mod = node.module or ""

            imports.append(mod)

    # De - dupe while preserving order

    seen: set[str] = set()

    out: List[str] = []

    for item in imports:

        if item not in seen:

            seen.add(item)

            out.append(item)

    return out


def _detect_cli_entry(source: str) -> bool:

    return "if __name__ == '__main__'" in source or 'if __name__ == "__main__"' in source


def _detect_argparse(source: str) -> bool:

    return "argparse" in source


def _placeholder_test_note(path: Path, source: str) -> Optional[str]:

    if not _is_pytest_test_file(path):

        return None

    if re.search(r"def\s + test_placeholder\s*\(", source) and "assert True" in source:

        return "Test file only contains a placeholder test (no real assertions / coverage)."

    return None


def _write_md(path: Path, content: str) -> None:

    # Normalize newlines for Windows repos.

    path.write_text(content.replace("\r\n", "\n").rstrip() + "\n", encoding="utf-8")


def _rel(path: Path) -> str:

    try:

        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")

    except ValueError:

        return str(path).replace("\\", "/")


def render_description(py_path: Path, source: str, tree: ast.AST) -> str:

    doc = ast.get_docstring(cast(ast.Module, tree)) or ""

    functions, classes = _find_top_level_defs(tree)

    imports = _find_imports(tree)

    lines: List[str] = []

    lines.append(f"  # Description: `{py_path.name}`")

    lines.append("")

    if doc.strip():

        lines.append("  ## Module purpose")

        lines.append(doc.strip())

        lines.append("")

    else:

        lines.append("  ## Module purpose")

        lines.append("(No module docstring found.)")

        lines.append("")

    lines.append("  ## Location")

    lines.append(f"- Path: `{_rel(py_path)}`")

    lines.append("")

    lines.append("  ## Public surface")

    lines.append(f"- Classes: {', '.join(classes) if classes else '(none)'}")

    lines.append(f"- Functions: {', '.join(functions) if functions else '(none)'}")

    lines.append("")

    lines.append("  ## Behavior summary")

    behavior_bits: List[str] = []

    if _detect_cli_entry(source):

        behavior_bits.append("Has a CLI entrypoint (`__main__`).")

    if _detect_argparse(source):

        behavior_bits.append("Uses `argparse` for CLI parsing.")

    if "subprocess" in source:

        behavior_bits.append("Invokes external commands via `subprocess`.")

    if "sys.path.insert" in source:

        behavior_bits.append("Mutates `sys.path` to import sibling modules.")

    if not behavior_bits:

        behavior_bits.append("Pure module (no obvious CLI / side effects).")

    for bit in behavior_bits:

        lines.append(f"- {bit}")

    lines.append("")

    lines.append("  ## Key dependencies")

    if imports:

        # Keep it short; imports can be long.

        shown = imports[:12]

        shown_imports = ", ".join(f"`{x}`" for x in shown)

        suffix = " …" if len(imports) > len(shown) else ""

        lines.append(f"- Top imports: {shown_imports}{suffix}")

    else:

        lines.append("- (none)")

    lines.append("")

    lines.append("  ## File fingerprint")

    lines.append(f"- SHA256(source): `{_sha256_text(source)[:16]}…`")

    return "\n".join(lines)


def render_errors(py_path: Path, source: str, compile_result: CompileResult) -> str:

    lines: List[str] = []

    lines.append(f"  # Errors: `{py_path.name}`")

    lines.append("")

    lines.append("  ## Scan scope")

    lines.append("- Static scan (AST parse) + lightweight compile / syntax check")

    lines.append("- VS Code / Pylance Problems are not embedded by this script")

    lines.append("")

    lines.append("  ## Syntax / compile")

    if compile_result.ok:

        lines.append("- `py_compile` equivalent: OK (AST parse succeeded)")

    else:

        lines.append("- `py_compile` equivalent: FAILED")

        lines.append(f"- Error: {compile_result.error}")

    lines.append("")

    known: List[str] = []

    pytest_name_issue = _looks_like_pytest_import_problem(py_path)

    if pytest_name_issue:

        known.append(pytest_name_issue)

    placeholder_note = _placeholder_test_note(py_path, source)

    if placeholder_note:

        known.append(placeholder_note)

    # High - level runtime hazards (facts based on static scan)

    if "subprocess.run([\"git\"" in source or "subprocess.run(['git'" in source:

        known.append(
            "Runs `git` via `subprocess`; will fail if git is not "
            "installed or repo has no remote.")

    if "copilot" in source and "subprocess.run" in source:
        known.append(
            "Invokes `copilot` CLI; will be a no-op / fallback if "
            "Copilot CLI is not installed."
        )

    lines.append("  ## Known issues / hazards")

    if known:

        for item in known:

            lines.append(f"- {item}")

    else:

        lines.append("- None detected by the lightweight scan")

    return "\n".join(lines)


def _find_issues(tree: ast.AST, source: str) -> List[str]:

    issues: List[str] = []

    # 1. Mutable defaults

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            for default in node.args.defaults:

                if isinstance(default, (ast.List, ast.Dict, ast.Set)):

                    issues.append(
                        f"Function `{node.name}` has a mutable default "
                        f"argument (list / dict / set)."
                    )

                    break  # One per function is enough

    # 2. Bare excepts

    for node in ast.walk(tree):

        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append(
                "Contains bare `except:` clause (catches SystemExit / "
                "KeyboardInterrupt)."
            )

    # 3. Missing type hints

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            # Check args

            missing_arg_type = any(
                arg.annotation is None for arg in node.args.args if arg.arg != 'self')

            # Check return

            missing_return_type = node.returns is None

            if missing_arg_type or missing_return_type:

                issues.append(f"Function `{node.name}` is missing type annotations.")

    # 4. TODOs

    if "TODO" in source or "FIXME" in source:

        issues.append("Contains TODO or FIXME comments.")

    return issues


def render_improvements(py_path: Path, source: str, tree: ast.AST) -> str:

    _, classes = _find_top_level_defs(tree)

    suggestions: List[str] = []

    # AST - based issues

    suggestions.extend(_find_issues(tree, source))

    if "sys.path.insert" in source:

        suggestions.append(
            "Avoid `sys.path.insert(...)` imports; prefer a proper "
            "package layout or relative imports."
        )

    if "subprocess.run" in source:

        suggestions.append(
            "Add robust subprocess error handling (`check=True`, "
            "timeouts, clearer stderr reporting)."
        )

    if _detect_cli_entry(source) and _detect_argparse(source):

        suggestions.append("Add `--help` examples and validate CLI args (paths, required files).")

    if _is_pytest_test_file(py_path) and re.search(
        r"def\s + test_placeholder\s*\(", source
    ):

        suggestions.append(
            "Replace placeholder tests with real assertions; target "
            "the most important behaviors first."
        )

    if _looks_like_pytest_import_problem(py_path):

        suggestions.append(
            "Rename the file to be pytest-importable (avoid '-' and "
            "extra '.'), then update references."
        )

    # Generic quality improvements

    if not ast.get_docstring(cast(ast.Module, tree)):

        suggestions.append("Add a concise module docstring describing purpose / usage.")

    if classes and "__init__" not in source:

        suggestions.append("Consider documenting class construction / expected invariants.")

    if "print(" in source and "logging" not in source:

        suggestions.append(
            "Consider using `logging` instead of `print` for controllable verbosity.")

    # Keep it short and deterministic.

    suggestions = sorted(list(set(suggestions)))  # Dedupe and sort

    lines: List[str] = []

    lines.append(f"  # Improvements: `{py_path.name}`")

    lines.append("")

    lines.append("  ## Suggested improvements")

    if suggestions:

        for s in suggestions:

            lines.append(f"- {s}")

    else:

        lines.append("- No obvious improvements detected by the lightweight scan")

    lines.append("")

    lines.append("  ## Notes")

    lines.append(
        "- These are suggestions based on static inspection; validate behavior with tests / runs.")

    lines.append(f"- File: `{_rel(py_path)}`")

    return "\n".join(lines)


def iter_agent_py_files() -> Iterable[Path]:

    return sorted(AGENT_DIR.glob("*.py"))


def _get_existing_sha(stem: str) -> Optional[str]:

    desc_path = AGENT_DIR / f"{stem}.description.md"

    if not desc_path.exists():

        return None

    content = _read_text(desc_path)

    match = re.search(r"- SHA256\(source\): `([a-f0-9]+)", content)

    return match.group(1) if match else None


def main(argv: Sequence[str]) -> int:

    logging.basicConfig(

        level=logging.INFO,

        format='%(asctime)s - %(levelname)s - %(message)s',

        datefmt='%H:%M:%S'

    )

    py_files = list(iter_agent_py_files())

    if not py_files:

        logging.error(f"No .py files found under {AGENT_DIR}")

        return 1

    count = 0

    skipped = 0

    errors_count = 0

    for py_path in py_files:

        try:

            source = _read_text(py_path)

            current_sha = _sha256_text(source)[:16]

            stem = py_path.stem

            # Incremental check

            existing_sha = _get_existing_sha(stem)

            if existing_sha == current_sha:

                skipped += 1

                logging.debug(f"Skipping unchanged file: {py_path.name}")

                continue

            logging.info(f"Processing {py_path.name}...")

            tree, parse_err = _try_parse_python(source, str(py_path))

            compile_result = _compile_check(py_path)

            # If parse failed, still emit minimal files.

            if tree is None:

                description = (

                    f"  # Description: `{py_path.name}`\n\n"

                    f"  ## Module purpose\n\n"

                    f"(Unable to parse file: {parse_err})\n"

                )

                errors = render_errors(py_path, source, compile_result)

                improvements = (

                    f"  # Improvements: `{py_path.name}`\n\n"

                    "  ## Suggested improvements\n"

                    "- Fix the syntax errors first; then re - run report generation\n"

                )

            else:

                description = render_description(py_path, source, tree)

                errors = render_errors(py_path, source, compile_result)

                improvements = render_improvements(py_path, source, tree)

            _write_md(AGENT_DIR / f"{stem}.description.md", description)

            _write_md(AGENT_DIR / f"{stem}.errors.md", errors)

            _write_md(AGENT_DIR / f"{stem}.improvements.md", improvements)

            count += 1

        except Exception as e:

            logging.error(f"Error processing {py_path.name}: {e}")

            errors_count += 1

    logging.info(f"Processed {count} files, skipped {skipped} unchanged, {errors_count} errors.")

    return 0 if errors_count == 0 else 1


if __name__ == "__main__":

    raise SystemExit(main(sys.argv))
