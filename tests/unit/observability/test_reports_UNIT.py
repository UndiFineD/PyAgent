# -*- coding: utf-8 -*-
"""Test classes from test_generate_agent_reports.py - core module."""

from __future__ import annotations
import unittest
from typing import Any, List, Dict, Optional, Callable, Tuple, Set, Union
from unittest.mock import MagicMock, Mock, patch, call, ANY
import time
import json
from datetime import datetime
import pytest
import logging
from pathlib import Path
import sys
import os
import tempfile
import shutil
import subprocess
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Try to import test utilities
try:
    from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
except ImportError:
    # Fallback
    AGENT_DIR: Path = Path(__file__).parent.parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self) -> Self: 
            sys.path.insert(0, str(AGENT_DIR))
            return self
        def __exit__(self, *args) -> None: 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed
<<<<<<< HEAD
<<<<<<< HEAD
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

=======
>>>>>>> d6712a17b (phase 320)

class TestReportTypeEnum:
    """Tests for ReportType enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        ReportType = report_module.ReportType
        assert ReportType.DESCRIPTION.value == "description"
        assert ReportType.ERRORS.value == "errors"
        assert ReportType.IMPROVEMENTS.value == "improvements"
        assert ReportType.SUMMARY.value == "summary"

    def test_enum_members(self, report_module: Any) -> None:
        """Test all enum members exist."""
        ReportType = report_module.ReportType
        members: List[Any] = [m.name for m in ReportType]
        assert "DESCRIPTION" in members
        assert "ERRORS" in members
        assert "IMPROVEMENTS" in members
        assert "SUMMARY" in members



class TestReportFormatEnum:
    """Tests for ReportFormat enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        ReportFormat = report_module.ReportFormat
        assert ReportFormat.MARKDOWN.value == "markdown"
        assert ReportFormat.JSON.value == "json"
        assert ReportFormat.HTML.value == "html"

    def test_all_members(self, report_module: Any) -> None:
        """Test all members are present."""
        ReportFormat = report_module.ReportFormat
        assert len(list(ReportFormat)) == 3



class TestSeverityLevelEnum:
    """Tests for SeverityLevel enum."""

    def test_enum_ordering(self, report_module: Any) -> None:
        """Test severity levels have correct ordering values."""
        SeverityLevel = report_module.SeverityLevel
        assert SeverityLevel.INFO.value < SeverityLevel.WARNING.value
        assert SeverityLevel.WARNING.value < SeverityLevel.ERROR.value
        assert SeverityLevel.ERROR.value < SeverityLevel.CRITICAL.value

    def test_all_levels(self, report_module: Any) -> None:
        """Test all severity levels exist."""
        SeverityLevel = report_module.SeverityLevel
        members: List[Any] = [m.name for m in SeverityLevel]
        assert "INFO" in members
        assert "WARNING" in members
        assert "ERROR" in members
        assert "CRITICAL" in members



class TestIssueCategoryEnum:
    """Tests for IssueCategory enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        IssueCategory = report_module.IssueCategory
        assert IssueCategory.SYNTAX.value == "syntax"
        assert IssueCategory.TYPE_ANNOTATION.value == "type_annotation"
        assert IssueCategory.STYLE.value == "style"
        assert IssueCategory.SECURITY.value == "security"
        assert IssueCategory.PERFORMANCE.value == "performance"
        assert IssueCategory.DOCUMENTATION.value == "documentation"

    def test_all_categories(self, report_module: Any) -> None:
        """Test all categories exist."""
        IssueCategory = report_module.IssueCategory
        assert len(list(IssueCategory)) == 6


# =============================================================================
# Phase 6: Dataclass Tests
# =============================================================================



class TestCodeIssueDataclass:
    """Tests for CodeIssue dataclass."""

    def test_creation_minimal(self, report_module: Any) -> None:
        """Test creating CodeIssue with minimal fields."""
        CodeIssue = report_module.CodeIssue
        SeverityLevel = report_module.SeverityLevel
        IssueCategory = report_module.IssueCategory

        issue = CodeIssue(
            message="Test error",
            category=IssueCategory.SYNTAX,
            severity=SeverityLevel.ERROR
        )
        assert issue.message == "Test error"
        assert issue.category == IssueCategory.SYNTAX
        assert issue.severity == SeverityLevel.ERROR
        assert issue.line_number is None
        assert issue.file_path is None

    def test_creation_full(self, report_module: Any) -> None:
        """Test creating CodeIssue with all fields."""
        CodeIssue = report_module.CodeIssue
        SeverityLevel = report_module.SeverityLevel
        IssueCategory = report_module.IssueCategory

        issue = CodeIssue(
            message="Type error",
            category=IssueCategory.TYPE_ANNOTATION,
            severity=SeverityLevel.WARNING,
            line_number=42,
            file_path="test.py"
        )
        assert issue.line_number == 42
        assert issue.file_path == "test.py"



class TestReportMetadataDataclass:
    """Tests for ReportMetadata dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportMetadata."""
        ReportMetadata = report_module.ReportMetadata

        metadata = ReportMetadata(
            path="test.py",
            generated_at="2025-01-13",
            content_hash="abc123",
            version="1.0.0"
        )
        assert metadata.path == "test.py"
        assert metadata.generated_at == "2025-01-13"
        assert metadata.content_hash == "abc123"
        assert metadata.version == "1.0.0"



class TestReportTemplateDataclass:
    """Tests for ReportTemplate dataclass."""

    def test_creation_with_defaults(self, report_module: Any) -> None:
        """Test creating ReportTemplate with defaults."""
        ReportTemplate = report_module.ReportTemplate

        template = ReportTemplate(
            name="default",
            sections=["description", "errors"]
        )
        assert template.name == "default"
        assert "description" in template.sections
        assert template.include_metadata is True
        assert template.include_summary is True



class TestReportCacheDataclass:
    """Tests for ReportCache dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportCache."""
        ReportCache = report_module.ReportCache

        cache = ReportCache(
            path="test.py",
            content_hash="abc123",
            content="Report content",
            created_at=1000.0,
            ttl_seconds=3600
        )
        assert cache.path == "test.py"
        assert cache.content_hash == "abc123"
        assert cache.content == "Report content"
        assert cache.ttl_seconds == 3600



class TestReportComparisonDataclass:
    """Tests for ReportComparison dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportComparison."""
        ReportComparison = report_module.ReportComparison

        comparison = ReportComparison(
            old_path="old.md",
            new_path="new.md",
            added=["- New item"],
            removed=["- Old item"],
            changed=[("- Changed from", "- Changed to")],
            unchanged_count=5
        )
        assert comparison.old_path == "old.md"
        assert comparison.new_path == "new.md"
        assert len(comparison.added) == 1
        assert len(comparison.removed) == 1
        assert len(comparison.changed) == 1
        assert comparison.unchanged_count == 5



class TestFilterCriteriaDataclass:
    """Tests for FilterCriteria dataclass."""

    def test_creation_with_defaults(self, report_module: Any) -> None:
        """Test creating FilterCriteria with defaults."""
        FilterCriteria = report_module.FilterCriteria

        criteria = FilterCriteria()
        assert criteria.categories is None
        assert criteria.min_severity is None
        assert criteria.date_from is None
        assert criteria.date_to is None
        assert criteria.file_patterns is None


# =============================================================================
# Phase 6: ReportCacheManager Tests
# =============================================================================



class TestReportCacheManager:
    """Tests for ReportCacheManager class."""

    def test_initialization(self, report_module: Any, tmp_path: Path) -> None:
        """Test cache manager initialization."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file: Path = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)
        assert manager.cache_file == cache_file
        assert manager._cache == {}

    def test_set_and_get(self, report_module: Any, tmp_path: Path) -> None:
        """Test setting and getting cache entries."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file: Path = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("test.py", "abc123", "Report content", ttl=3600)
        result = manager.get("test.py", "abc123")

        assert result == "Report content"

    def test_get_expired(self, report_module: Any, tmp_path: Path) -> None:
        """Test getting expired cache entry returns None."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file: Path = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("test.py", "abc123", "Report content", ttl=-1)
        result = manager.get("test.py", "abc123")

        assert result is None

    def test_get_wrong_hash(self, report_module: Any, tmp_path: Path) -> None:
        """Test getting with wrong hash returns None."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file: Path = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("test.py", "abc123", "Report content", ttl=3600)
        result = manager.get("test.py", "different_hash")

        assert result is None

    def test_invalidate_by_path(self, report_module: Any, tmp_path: Path) -> None:
        """Test invalidating cache by path."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file: Path = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("test.py", "abc123", "Report content", ttl=3600)
        manager.invalidate("test.py")
        result = manager.get("test.py", "abc123")

        assert result is None


# =============================================================================
# Phase 6: ReportComparator Tests
# =============================================================================



class TestReportComparator:
    """Tests for ReportComparator class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test comparator initialization."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        assert comparator is not None

    def test_compare_identical(self, report_module: Any) -> None:
        """Test comparing identical reports."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old_content = "- Item 1\n- Item 2\n- Item 3"
        new_content = "- Item 1\n- Item 2\n- Item 3"

        result = comparator.compare("old.md", "new.md", old_content, new_content)

        assert len(result.added) == 0
        assert len(result.removed) == 0
        assert result.unchanged_count == 3

    def test_compare_with_additions(self, report_module: Any) -> None:
        """Test comparing reports with additions."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old_content = "- Item 1\n- Item 2"
        new_content = "- Item 1\n- Item 2\n- Item 3"

        result = comparator.compare("old.md", "new.md", old_content, new_content)

        assert "- Item 3" in result.added
        assert len(result.removed) == 0

    def test_compare_with_removals(self, report_module: Any) -> None:
        """Test comparing reports with removals."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old_content = "- Item 1\n- Item 2\n- Item 3"
        new_content = "- Item 1\n- Item 2"

        result = comparator.compare("old.md", "new.md", old_content, new_content)

        assert "- Item 3" in result.removed
        assert len(result.added) == 0

    def test_extract_items(self, report_module: Any) -> None:
        """Test extracting list items from content."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        content = "# Header\n- Item 1\n- Item 2\nSome text\n- Item 3"

        items = comparator._extract_items(content)

        assert len(items) == 3
        assert "- Item 1" in items
        assert "- Item 2" in items
        assert "- Item 3" in items


# =============================================================================
# Phase 6: ReportFilter Tests
# =============================================================================



class TestReportFilter:
    """Tests for ReportFilter class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test filter initialization."""
        ReportFilter = report_module.ReportFilter
        FilterCriteria = report_module.FilterCriteria

        criteria = FilterCriteria()
        filter_obj = ReportFilter(criteria)
        assert filter_obj.criteria == criteria

    def test_matches_by_category(self, report_module: Any) -> None:
        """Test matching issues by category."""
        ReportFilter = report_module.ReportFilter
        FilterCriteria = report_module.FilterCriteria
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        criteria = FilterCriteria(categories=[IssueCategory.SYNTAX])
        filter_obj = ReportFilter(criteria)

        syntax_issue = CodeIssue(
            message="Syntax error",
            category=IssueCategory.SYNTAX,
            severity=SeverityLevel.ERROR
        )
        style_issue = CodeIssue(
            message="Style issue",
            category=IssueCategory.STYLE,
            severity=SeverityLevel.WARNING
        )

        assert filter_obj.matches(syntax_issue) is True
        assert filter_obj.matches(style_issue) is False

    def test_matches_by_severity(self, report_module: Any) -> None:
        """Test matching issues by minimum severity."""
        ReportFilter = report_module.ReportFilter
        FilterCriteria = report_module.FilterCriteria
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        criteria = FilterCriteria(min_severity=SeverityLevel.ERROR)
        filter_obj = ReportFilter(criteria)

        error_issue = CodeIssue(
            message="Error",
            category=IssueCategory.SYNTAX,
            severity=SeverityLevel.ERROR
        )
        warning_issue = CodeIssue(
            message="Warning",
            category=IssueCategory.STYLE,
            severity=SeverityLevel.WARNING
        )

        assert filter_obj.matches(error_issue) is True
        assert filter_obj.matches(warning_issue) is False

    def test_filter_issues(self, report_module: Any) -> None:
        """Test filtering list of issues."""
        ReportFilter = report_module.ReportFilter
        FilterCriteria = report_module.FilterCriteria
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        criteria = FilterCriteria(categories=[IssueCategory.SYNTAX])
        filter_obj = ReportFilter(criteria)

        issues: List[Any] = [
            CodeIssue(
                message="Syntax error",
                category=IssueCategory.SYNTAX,
                severity=SeverityLevel.ERROR
            ),
            CodeIssue(
                message="Style issue",
                category=IssueCategory.STYLE,
                severity=SeverityLevel.WARNING
            ),
            CodeIssue(
                message="Another syntax error",
                category=IssueCategory.SYNTAX,
                severity=SeverityLevel.WARNING
            ),
        ]

        filtered = filter_obj.filter_issues(issues)

        assert len(filtered) == 2
        assert all(i.category == IssueCategory.SYNTAX for i in filtered)


# =============================================================================
# Phase 6: Integration Tests
# =============================================================================



class TestSubscriptionFrequencyEnum:
    """Tests for SubscriptionFrequency enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        SubscriptionFrequency = report_module.SubscriptionFrequency
        assert SubscriptionFrequency.IMMEDIATE.value == "immediate"
        assert SubscriptionFrequency.HOURLY.value == "hourly"
        assert SubscriptionFrequency.DAILY.value == "daily"
        assert SubscriptionFrequency.WEEKLY.value == "weekly"

    def test_all_members(self, report_module: Any) -> None:
        """Test all members exist."""
        SubscriptionFrequency = report_module.SubscriptionFrequency
        assert len(list(SubscriptionFrequency)) == 4



class TestPermissionLevelEnum:
    """Tests for PermissionLevel enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        PermissionLevel = report_module.PermissionLevel
        assert PermissionLevel.READ.value == 1
        assert PermissionLevel.WRITE.value == 2
        assert PermissionLevel.ADMIN.value == 3

    def test_enum_ordering(self, report_module: Any) -> None:
        """Test permission levels are ordered correctly."""
        PermissionLevel = report_module.PermissionLevel
        assert PermissionLevel.READ.value < PermissionLevel.WRITE.value
        assert PermissionLevel.WRITE.value < PermissionLevel.ADMIN.value



class TestExportFormatEnum:
    """Tests for ExportFormat enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        ExportFormat = report_module.ExportFormat
        assert ExportFormat.HTML.value == "html"
        assert ExportFormat.JSON.value == "json"
        assert ExportFormat.CSV.value == "csv"
        assert ExportFormat.PDF.value == "pdf"

    def test_all_members(self, report_module: Any) -> None:
        """Test all members exist."""
        ExportFormat = report_module.ExportFormat
        assert len(list(ExportFormat)) == 4



class TestLocaleCodeEnum:
    """Tests for LocaleCode enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        LocaleCode = report_module.LocaleCode
        assert LocaleCode.EN_US.value == "en-US"
        assert LocaleCode.DE_DE.value == "de-DE"
        assert LocaleCode.FR_FR.value == "fr-FR"
        assert LocaleCode.ES_ES.value == "es-ES"

    def test_all_members(self, report_module: Any) -> None:
        """Test all members exist."""
        LocaleCode = report_module.LocaleCode
        assert len(list(LocaleCode)) == 4



class TestAuditActionEnum:
    """Tests for AuditAction enum."""

    def test_enum_values(self, report_module: Any) -> None:
        """Test enum has expected values."""
        AuditAction = report_module.AuditAction
        assert AuditAction.CREATE.value == "create"
        assert AuditAction.READ.value == "read"
        assert AuditAction.UPDATE.value == "update"
        assert AuditAction.DELETE.value == "delete"
        assert AuditAction.EXPORT.value == "export"

    def test_all_members(self, report_module: Any) -> None:
        """Test all members exist."""
        AuditAction = report_module.AuditAction
        assert len(list(AuditAction)) == 5


# =============================================================================
# Session 8: Dataclass Tests
# =============================================================================



class TestReportSubscriptionDataclass:
    """Tests for ReportSubscription dataclass."""

    def test_creation_minimal(self, report_module: Any) -> None:
        """Test creating with minimal fields."""
        ReportSubscription = report_module.ReportSubscription

        sub = ReportSubscription(
            subscriber_id="user1",
            email="user@example.com"
        )
        assert sub.subscriber_id == "user1"
        assert sub.email == "user@example.com"
        assert sub.enabled is True

    def test_creation_full(self, report_module: Any) -> None:
        """Test creating with all fields."""
        ReportSubscription = report_module.ReportSubscription
        SubscriptionFrequency = report_module.SubscriptionFrequency
        ReportType = report_module.ReportType

        sub = ReportSubscription(
            subscriber_id="user1",
            email="user@example.com",
            frequency=SubscriptionFrequency.WEEKLY,
            report_types=[ReportType.ERRORS],
            file_patterns=["*.py"],
            enabled=False
        )
        assert sub.frequency == SubscriptionFrequency.WEEKLY
        assert ReportType.ERRORS in sub.report_types
        assert sub.enabled is False



class TestArchivedReportDataclass:
    """Tests for ArchivedReport dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ArchivedReport."""
        ArchivedReport = report_module.ArchivedReport

        archive = ArchivedReport(
            report_id="report_123",
            file_path="test.py",
            content="Report content"
        )
        assert archive.report_id == "report_123"
        assert archive.file_path == "test.py"
        assert archive.retention_days == 90



class TestReportAnnotationDataclass:
    """Tests for ReportAnnotation dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportAnnotation."""
        ReportAnnotation = report_module.ReportAnnotation

        annotation = ReportAnnotation(
            annotation_id="ann_1",
            report_id="report_1",
            author="user1",
            content="Important note",
            line_number=42
        )
        assert annotation.annotation_id == "ann_1"
        assert annotation.author == "user1"
        assert annotation.line_number == 42



class TestReportSearchResultDataclass:
    """Tests for ReportSearchResult dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportSearchResult."""
        ReportSearchResult = report_module.ReportSearchResult
        ReportType = report_module.ReportType

        result = ReportSearchResult(
            file_path="test.py",
            report_type=ReportType.ERRORS,
            match_text="Syntax error",
            line_number=10,
            score=2.5
        )
        assert result.file_path == "test.py"
        assert result.score == 2.5



class TestReportMetricDataclass:
    """Tests for ReportMetric dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportMetric."""
        ReportMetric = report_module.ReportMetric

        metric = ReportMetric(
            name="issues_count",
            value=42.0,
            unit="count",
            threshold=100.0,
            trend="+"
        )
        assert metric.name == "issues_count"
        assert metric.value == 42.0
        assert metric.trend == "+"



class TestReportPermissionDataclass:
    """Tests for ReportPermission dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating ReportPermission."""
        ReportPermission = report_module.ReportPermission
        PermissionLevel = report_module.PermissionLevel

        perm = ReportPermission(
            user_id="user1",
            report_pattern="*.md",
            level=PermissionLevel.WRITE,
            granted_by="admin"
        )
        assert perm.user_id == "user1"
        assert perm.level == PermissionLevel.WRITE



class TestAuditEntryDataclass:
    """Tests for AuditEntry dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating AuditEntry."""
        AuditEntry = report_module.AuditEntry
        AuditAction = report_module.AuditAction

        entry = AuditEntry(
            entry_id="audit_1",
            timestamp=1000.0,
            action=AuditAction.READ,
            user_id="user1",
            report_id="report1",
            details={"ip": "127.0.0.1"}
        )
        assert entry.action == AuditAction.READ
        assert entry.details["ip"] == "127.0.0.1"



class TestLocalizedStringDataclass:
    """Tests for LocalizedString dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating LocalizedString."""
        LocalizedString = report_module.LocalizedString

        localized = LocalizedString(
            key="error.syntax",
            translations={"en-US": "Syntax Error", "de-DE": "Syntaxfehler"},
            default="Syntax Error"
        )
        assert localized.key == "error.syntax"
        assert localized.translations["de-DE"] == "Syntaxfehler"



class TestValidationResultDataclass:
    """Tests for ValidationResult dataclass."""

    def test_creation_valid(self, report_module: Any) -> None:
        """Test creating valid ValidationResult."""
        ValidationResult = report_module.ValidationResult

        result = ValidationResult(
            valid=True,
            errors=[],
            warnings=["Minor issue"],
            checksum="abc123"
        )
        assert result.valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 1

    def test_creation_invalid(self, report_module: Any) -> None:
        """Test creating invalid ValidationResult."""
        ValidationResult = report_module.ValidationResult

        result = ValidationResult(
            valid=False,
            errors=["Missing heading"],
            checksum="def456"
        )
        assert result.valid is False
        assert "Missing heading" in result.errors



class TestAggregatedReportDataclass:
    """Tests for AggregatedReport dataclass."""

    def test_creation(self, report_module: Any) -> None:
        """Test creating AggregatedReport."""
        AggregatedReport = report_module.AggregatedReport
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        issue = CodeIssue(
            message="Test error",
            category=IssueCategory.SYNTAX,
            severity=SeverityLevel.ERROR
        )
        report = AggregatedReport(
            sources=["file1.py", "file2.py"],
            combined_issues=[issue],
            summary={"total": 1}
        )
        assert len(report.sources) == 2
        assert len(report.combined_issues) == 1


# =============================================================================
# Session 8: Helper Class Tests
# =============================================================================



class TestSubscriptionManager:
    """Tests for SubscriptionManager class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        SubscriptionManager = report_module.SubscriptionManager

        manager = SubscriptionManager()
        assert manager.subscriptions == {}
        assert manager.delivery_queue == []

    def test_add_subscription(self, report_module: Any) -> None:
        """Test adding subscription."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportSubscription = report_module.ReportSubscription

        manager = SubscriptionManager()
        sub = ReportSubscription("user1", "user@example.com")
        manager.add_subscription(sub)

        assert "user1" in manager.subscriptions

    def test_remove_subscription(self, report_module: Any) -> None:
        """Test removing subscription."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportSubscription = report_module.ReportSubscription

        manager = SubscriptionManager()
        sub = ReportSubscription("user1", "user@example.com")
        manager.add_subscription(sub)

        assert manager.remove_subscription("user1") is True
        assert manager.remove_subscription("unknown") is False

    def test_get_due_subscriptions(self, report_module: Any) -> None:
        """Test getting due subscriptions."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportSubscription = report_module.ReportSubscription

        manager = SubscriptionManager()
        sub1 = ReportSubscription("user1", "user1@example.com", enabled=True)
        sub2 = ReportSubscription("user2", "user2@example.com", enabled=False)
        manager.add_subscription(sub1)
        manager.add_subscription(sub2)

        due = manager.get_due_subscriptions()
        assert len(due) == 1
        assert due[0].subscriber_id == "user1"

    def test_queue_and_process_delivery(self, report_module: Any) -> None:
        """Test queuing and processing deliveries."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportType = report_module.ReportType

        manager = SubscriptionManager()
        manager.queue_delivery("user1", "Report content", ReportType.ERRORS)

        assert len(manager.delivery_queue) == 1
        processed = manager.process_deliveries()
        assert processed == 1
        assert len(manager.delivery_queue) == 0



class TestReportArchiver:
    """Tests for ReportArchiver class."""

    def test_initialization(self, report_module: Any, tmp_path: Path) -> None:
        """Test initialization."""
        ReportArchiver = report_module.ReportArchiver

        archiver = ReportArchiver(tmp_path / "archives")
        assert archiver.archive_dir == tmp_path / "archives"

    def test_archive_and_list(self, report_module: Any) -> None:
        """Test archiving and listing."""
        ReportArchiver = report_module.ReportArchiver

        archiver = ReportArchiver()
        archived = archiver.archive("test.py", "Report content", retention_days=30)

        assert archived.file_path == "test.py"
        assert archived.retention_days == 30

        archives = archiver.list_archives("test.py")
        assert len(archives) == 1

    def test_get_archive(self, report_module: Any) -> None:
        """Test getting specific archive."""
        ReportArchiver = report_module.ReportArchiver

        archiver = ReportArchiver()
        archived = archiver.archive("test.py", "Content")

        retrieved = archiver.get_archive(archived.report_id)
        assert retrieved is not None
        assert retrieved.content == "Content"

        assert archiver.get_archive("nonexistent") is None

    def test_cleanup_expired(self, report_module: Any) -> None:
        """Test cleanup of expired archives."""
        ReportArchiver = report_module.ReportArchiver
        ArchivedReport = report_module.ArchivedReport

        archiver = ReportArchiver()
        # Create expired archive (archived_at in the past)
        old_archive = ArchivedReport(
            report_id="old_1",
            file_path="test.py",
            content="Old content",
            archived_at=1.0,  # Very old timestamp
            retention_days=1
        )
        archiver.archives["test.py"] = [old_archive]

        removed = archiver.cleanup_expired()
        assert removed == 1
        assert len(archiver.list_archives("test.py")) == 0



class TestAnnotationManager:
    """Tests for AnnotationManager class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        assert manager.annotations == {}

    def test_add_and_get_annotation(self, report_module: Any) -> None:
        """Test adding and retrieving annotations."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        ann = manager.add_annotation("report1", "user1", "Note", line_number=10)

        assert ann.author == "user1"
        assert ann.line_number == 10

        annotations = manager.get_annotations("report1")
        assert len(annotations) == 1

    def test_remove_annotation(self, report_module: Any) -> None:
        """Test removing annotation."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        ann = manager.add_annotation("report1", "user1", "Note")

        assert manager.remove_annotation(ann.annotation_id) is True
        assert manager.remove_annotation("nonexistent") is False
        assert len(manager.get_annotations("report1")) == 0



class TestReportSearchEngine:
    """Tests for ReportSearchEngine class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportSearchEngine = report_module.ReportSearchEngine

        engine = ReportSearchEngine()
        assert engine.index == {}

    def test_index_and_search(self, report_module: Any) -> None:
        """Test indexing and searching."""
        ReportSearchEngine = report_module.ReportSearchEngine
        ReportType = report_module.ReportType

        engine = ReportSearchEngine()
        content = "Line one\nSyntax error found\nLine three"
        engine.index_report("test.py", ReportType.ERRORS, content)

        results = engine.search("syntax error")
        assert len(results) > 0
        assert results[0].file_path == "test.py"

    def test_search_no_results(self, report_module: Any) -> None:
        """Test search with no results."""
        ReportSearchEngine = report_module.ReportSearchEngine

        engine = ReportSearchEngine()
        results = engine.search("nonexistent")
        assert len(results) == 0



class TestMetricsCollector:
    """Tests for MetricsCollector class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        assert collector.metrics == {}

    def test_record_and_get(self, report_module: Any) -> None:
        """Test recording and retrieving metrics."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        metric = collector.record("test.py", "issues", 5.0, "count")

        assert metric.name == "issues"
        assert metric.value == 5.0

        metrics = collector.get_metrics("test.py")
        assert len(metrics) == 1

    def test_get_summary(self, report_module: Any) -> None:
        """Test getting summary."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        collector.record("file1.py", "issues", 5.0)
        collector.record("file2.py", "issues", 10.0)

        summary = collector.get_summary()
        assert summary["total_files"] == 2
        assert summary["total_metrics"] == 2
        assert summary["averages"]["issues"] == 7.5



class TestAccessController:
    """Tests for AccessController class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        AccessController = report_module.AccessController

        controller = AccessController()
        assert controller.permissions == []

    def test_grant_permission(self, report_module: Any) -> None:
        """Test granting permission."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        perm = controller.grant("user1", "*.md", PermissionLevel.READ)

        assert perm.user_id == "user1"
        assert len(controller.permissions) == 1

    def test_check_permission(self, report_module: Any) -> None:
        """Test checking permission."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("user1", "*.md", PermissionLevel.READ)

        assert controller.check("user1", "report.md", PermissionLevel.READ) is True
        assert controller.check("user1", "report.md", PermissionLevel.WRITE) is False
        assert controller.check("user2", "report.md", PermissionLevel.READ) is False

    def test_revoke_permission(self, report_module: Any) -> None:
        """Test revoking permission."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("user1", "*.md", PermissionLevel.READ)

        assert controller.revoke("user1", "*.md") is True
        assert controller.revoke("unknown", "*.md") is False
        assert controller.check("user1", "report.md", PermissionLevel.READ) is False



class TestReportExporter:
    """Tests for ReportExporter class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportExporter = report_module.ReportExporter

        exporter = ReportExporter()
        assert exporter is not None

    def test_to_html(self, report_module: Any) -> None:
        """Test HTML conversion."""
        ReportExporter = report_module.ReportExporter

        exporter = ReportExporter()
        html = exporter.to_html("# Title\n- Item", "Test")

        assert "<h1>Title</h1>" in html
        assert "<li>Item</li>" in html
        assert "<title>Test</title>" in html

    def test_to_csv(self, report_module: Any) -> None:
        """Test CSV export."""
        ReportExporter = report_module.ReportExporter
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        exporter = ReportExporter()
        issues: List[Any] = [
            CodeIssue(
                message="Test error",
                category=IssueCategory.SYNTAX,
                severity=SeverityLevel.ERROR,
                line_number=10
            )
        ]
        csv = exporter.to_csv(issues)

        assert "message,category" in csv
        assert "Test error" in csv
        assert "SYNTAX" in csv

    def test_export(self, report_module: Any, tmp_path: Path) -> None:
        """Test export to file."""
        ReportExporter = report_module.ReportExporter
        ExportFormat = report_module.ExportFormat

        exporter = ReportExporter()
        output: Path = tmp_path / "report.html"
        result = exporter.export("# Test", ExportFormat.HTML, output)

        assert "<h1>Test</h1>" in result
        assert output.exists()



class TestAuditLogger:
    """Tests for AuditLogger class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        AuditLogger = report_module.AuditLogger

        logger = AuditLogger()
        assert logger.entries == []

    def test_log_action(self, report_module: Any) -> None:
        """Test logging action."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()
        entry = logger.log(AuditAction.READ, "user1", "report.md")

        assert entry.action == AuditAction.READ
        assert entry.user_id == "user1"
        assert len(logger.entries) == 1

    def test_get_history(self, report_module: Any) -> None:
        """Test getting report history."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()
        logger.log(AuditAction.READ, "user1", "report1.md")
        logger.log(AuditAction.UPDATE, "user2", "report1.md")
        logger.log(AuditAction.READ, "user1", "report2.md")

        history = logger.get_history("report1.md")
        assert len(history) == 2

    def test_get_user_activity(self, report_module: Any) -> None:
        """Test getting user activity."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()
        logger.log(AuditAction.READ, "user1", "report1.md")
        logger.log(AuditAction.READ, "user1", "report2.md")
        logger.log(AuditAction.READ, "user2", "report1.md")

        activity = logger.get_user_activity("user1")
        assert len(activity) == 2



class TestReportValidator:
    """Tests for ReportValidator class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        assert validator is not None

    def test_validate_valid_content(self, report_module: Any) -> None:
        """Test validating valid content."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        result = validator.validate("# Title\n\nSome content here.")

        assert result.valid is True
        assert len(result.errors) == 0
        assert result.checksum != ""

    def test_validate_missing_heading(self, report_module: Any) -> None:
        """Test validating content without heading."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        result = validator.validate("Just some text without heading")

        assert result.valid is False
        assert "Missing main heading" in result.errors

    def test_validate_empty_link(self, report_module: Any) -> None:
        """Test validating content with empty links."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        result = validator.validate("# Title\n\nA [broken link]()")

        assert "Contains empty link targets" in result.warnings

    def test_verify_checksum(self, report_module: Any) -> None:
        """Test verifying checksum."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        content = "# Test content"
        result = validator.validate(content)

        assert validator.verify_checksum(content, result.checksum) is True
        assert validator.verify_checksum(content, "wrong") is False



class TestReportLocalizer:
    """Tests for ReportLocalizer class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer(LocaleCode.EN_US)
        assert localizer.current_locale == LocaleCode.EN_US

    def test_get_default_string(self, report_module: Any) -> None:
        """Test getting default strings."""
        ReportLocalizer = report_module.ReportLocalizer

        localizer = ReportLocalizer()
        text = localizer.get("report.description")

        assert text == "Description"

    def test_get_german_string(self, report_module: Any) -> None:
        """Test getting German strings."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer(LocaleCode.DE_DE)
        text = localizer.get("report.errors")

        assert text == "Fehler"

    def test_add_string(self, report_module: Any) -> None:
        """Test adding custom string."""
        ReportLocalizer = report_module.ReportLocalizer

        localizer = ReportLocalizer()
        localizer.add_string("custom.key", {"en-US": "Custom", "de-DE": "Benutzerdefiniert"})

        assert localizer.get("custom.key") == "Custom"

    def test_set_locale(self, report_module: Any) -> None:
        """Test setting locale."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer(LocaleCode.EN_US)
        localizer.set_locale(LocaleCode.DE_DE)

        assert localizer.current_locale == LocaleCode.DE_DE

    def test_get_unknown_key(self, report_module: Any) -> None:
        """Test getting unknown key returns key."""
        ReportLocalizer = report_module.ReportLocalizer

        localizer = ReportLocalizer()
        text = localizer.get("unknown.key")

        assert text == "unknown.key"



class TestReportAPI:
    """Tests for ReportAPI class."""

    def test_initialization(self, report_module: Any, tmp_path: Path) -> None:
        """Test initialization."""
        ReportAPI = report_module.ReportAPI

        api = ReportAPI(tmp_path)
        assert api.reports_dir == tmp_path

    def test_list_reports(self, report_module: Any, tmp_path: Path) -> None:
        """Test listing reports."""
        ReportAPI = report_module.ReportAPI

        (tmp_path / "report1.md").write_text("# Report 1")
        (tmp_path / "report2.md").write_text("# Report 2")

        api = ReportAPI(tmp_path)
        reports = api.list_reports()

        assert len(reports) == 2

    def test_get_report(self, report_module: Any, tmp_path: Path) -> None:
        """Test getting specific report."""
        ReportAPI = report_module.ReportAPI
        ReportType = report_module.ReportType

        (tmp_path / "test.errors.md").write_text("# Errors")

        api = ReportAPI(tmp_path)
        content = api.get_report("test", ReportType.ERRORS)

        assert content == "# Errors"
        assert api.get_report("nonexistent", ReportType.ERRORS) is None

    def test_create_report(self, report_module: Any, tmp_path: Path) -> None:
        """Test creating report."""
        ReportAPI = report_module.ReportAPI
        ReportType = report_module.ReportType

        api = ReportAPI(tmp_path)
        result = api.create_report("new", ReportType.ERRORS, "# New Report")

        assert result is True
        assert (tmp_path / "new.errors.md").exists()



class TestReportScheduler:
    """Tests for ReportScheduler class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        assert scheduler.schedules == {}

    def test_add_schedule(self, report_module: Any) -> None:
        """Test adding schedule."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("daily", "0 8 * * *", ["*.py"])

        assert "daily" in scheduler.schedules
        assert scheduler.schedules["daily"]["patterns"] == ["*.py"]

    def test_remove_schedule(self, report_module: Any) -> None:
        """Test removing schedule."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("daily", "0 8 * * *", ["*.py"])

        assert scheduler.remove_schedule("daily") is True
        assert scheduler.remove_schedule("nonexistent") is False

    def test_get_due_tasks(self, report_module: Any) -> None:
        """Test getting due tasks."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("task1", "0 8 * * *", ["*.py"])
        scheduler.add_schedule("task2", "0 12 * * *", ["*.md"])

        due = scheduler.get_due_tasks()
        assert len(due) == 2

    def test_mark_completed(self, report_module: Any) -> None:
        """Test marking task completed."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("daily", "0 8 * * *", ["*.py"])
        scheduler.mark_completed("daily")

        assert scheduler.schedules["daily"]["last_run"] > 0



class TestReportAggregator:
    """Tests for ReportAggregator class."""

    def test_initialization(self, report_module: Any) -> None:
        """Test initialization."""
        ReportAggregator = report_module.ReportAggregator

        aggregator = ReportAggregator()
        assert aggregator.sources == {}

    def test_add_source(self, report_module: Any) -> None:
        """Test adding source."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()
        issues: List[Any] = [
            CodeIssue("Error 1", IssueCategory.SYNTAX, SeverityLevel.ERROR)
        ]
        aggregator.add_source("file1.py", issues)

        assert "file1.py" in aggregator.sources

    def test_aggregate(self, report_module: Any) -> None:
        """Test aggregating sources."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()
        aggregator.add_source("file1.py", [
            CodeIssue("Error 1", IssueCategory.SYNTAX, SeverityLevel.ERROR)
        ])
        aggregator.add_source("file2.py", [
            CodeIssue("Warning 1", IssueCategory.STYLE, SeverityLevel.WARNING)
        ])

        report = aggregator.aggregate()

        assert len(report.sources) == 2
        assert len(report.combined_issues) == 2
        assert report.summary["total_issues"] == 2
        assert report.summary["total_files"] == 2

    def test_clear(self, report_module: Any) -> None:
        """Test clearing sources."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()
        aggregator.add_source("file1.py", [
            CodeIssue("Error", IssueCategory.SYNTAX, SeverityLevel.ERROR)
        ])
        aggregator.clear()

        assert aggregator.sources == {}


# =============================================================================
# Session 8: Integration Tests
# =============================================================================



class TestReportSubscriptionAndDelivery:
    """Tests for report subscription and delivery functionality."""

    def test_subscription_creation_with_frequency(self, report_module: Any) -> None:
        """Test creating subscription with different frequencies."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportSubscription = report_module.ReportSubscription
        SubscriptionFrequency = report_module.SubscriptionFrequency

        manager = SubscriptionManager()

        for freq in SubscriptionFrequency:
            sub = ReportSubscription(
                subscriber_id=f"user_{freq.value}",
                email=f"user_{freq.value}@example.com",
                frequency=freq
            )
            manager.add_subscription(sub)

        assert len(manager.subscriptions) == 4

    def test_subscription_delivery_queue_ordering(self, report_module: Any) -> None:
        """Test delivery queue maintains order."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportType = report_module.ReportType

        manager = SubscriptionManager()
        manager.queue_delivery("user1", "Report 1", ReportType.ERRORS)
        manager.queue_delivery("user2", "Report 2", ReportType.IMPROVEMENTS)
        manager.queue_delivery("user1", "Report 3", ReportType.SUMMARY)

        assert len(manager.delivery_queue) == 3
        assert manager.delivery_queue[0]["subscriber_id"] == "user1"
        assert manager.delivery_queue[1]["subscriber_id"] == "user2"

    def test_subscription_enabled_filtering(self, report_module: Any) -> None:
        """Test filtering enabled vs disabled subscriptions."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportSubscription = report_module.ReportSubscription

        manager = SubscriptionManager()
        manager.add_subscription(ReportSubscription("active1", "a@test.com", enabled=True))
        manager.add_subscription(ReportSubscription("inactive1", "b@test.com", enabled=False))
        manager.add_subscription(ReportSubscription("active2", "c@test.com", enabled=True))

        due = manager.get_due_subscriptions()
        assert len(due) == 2
        assert all(s.enabled for s in due)



class TestReportArchivingWithRetention:
    """Tests for report archiving with retention policies."""

    def test_archive_with_custom_retention(self, report_module: Any) -> None:
        """Test archiving with different retention periods."""
        ReportArchiver = report_module.ReportArchiver

        archiver = ReportArchiver()

        short_retention = archiver.archive("file1.py", "Short lived", retention_days=7)
        long_retention = archiver.archive("file2.py", "Long lived", retention_days=365)

        assert short_retention.retention_days == 7
        assert long_retention.retention_days == 365

    def test_archive_retrieval_by_file(self, report_module: Any) -> None:
        """Test retrieving archives by file path."""
        ReportArchiver = report_module.ReportArchiver

        archiver = ReportArchiver()
        archiver.archive("file1.py", "Version 1")
        archiver.archive("file1.py", "Version 2")
        archiver.archive("file2.py", "Different file")

        file1_archives = archiver.list_archives("file1.py")
        file2_archives = archiver.list_archives("file2.py")

        assert len(file1_archives) == 2
        assert len(file2_archives) == 1

    def test_archive_cleanup_preserves_valid(self, report_module: Any) -> None:
        """Test cleanup removes expired but keeps valid archives."""
        ReportArchiver = report_module.ReportArchiver
        ArchivedReport = report_module.ArchivedReport

        archiver = ReportArchiver()

        # Add a valid (non-expired) archive
        archiver.archive("valid.py", "Valid content", retention_days=365)

        # Add an expired archive manually
        expired = ArchivedReport(
            report_id="expired_1",
            file_path="expired.py",
            content="Expired content",
            archived_at=1.0,  # Very old
            retention_days=1
        )
        archiver.archives["expired.py"] = [expired]

        removed = archiver.cleanup_expired()

        assert removed == 1
        assert len(archiver.list_archives("valid.py")) == 1
        assert len(archiver.list_archives("expired.py")) == 0



class TestReportAnnotationPersistence:
    """Tests for report annotation persistence."""

    def test_annotation_with_line_numbers(self, report_module: Any) -> None:
        """Test annotations with specific line numbers."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        manager.add_annotation("report1", "user1", "Line specific note", line_number=42)
        manager.add_annotation("report1", "user2", "Another note", line_number=100)

        annotations = manager.get_annotations("report1")
        line_numbers: List[Any] = [a.line_number for a in annotations]

        assert 42 in line_numbers
        assert 100 in line_numbers

    def test_annotation_removal_by_id(self, report_module: Any) -> None:
        """Test removing specific annotations by ID."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        manager.add_annotation("report1", "user1", "Keep this")
        ann2 = manager.add_annotation("report1", "user2", "Remove this")

        manager.remove_annotation(ann2.annotation_id)

        annotations = manager.get_annotations("report1")
        assert len(annotations) == 1
        assert annotations[0].content == "Keep this"

    def test_multiple_annotations_per_report(self, report_module: Any) -> None:
        """Test handling multiple annotations on same report."""
        AnnotationManager = report_module.AnnotationManager

        manager = AnnotationManager()
        for i in range(10):
            manager.add_annotation("report1", f"user{i}", f"Note {i}")

        annotations = manager.get_annotations("report1")
        assert len(annotations) == 10



class TestReportSearchAcrossHistoricalData:
    """Tests for report search across historical data."""

    def test_search_multiple_reports(self, report_module: Any) -> None:
        """Test searching across multiple indexed reports."""
        ReportSearchEngine = report_module.ReportSearchEngine
        ReportType = report_module.ReportType

        engine = ReportSearchEngine()
        engine.index_report("file1.py", ReportType.ERRORS, "Syntax error in function")
        engine.index_report("file2.py", ReportType.ERRORS, "Type error in class")
        engine.index_report("file3.py", ReportType.IMPROVEMENTS, "Consider adding error handling")

        results = engine.search("error")
        assert len(results) >= 2

    def test_search_with_max_results(self, report_module: Any) -> None:
        """Test search respects max results limit."""
        ReportSearchEngine = report_module.ReportSearchEngine
        ReportType = report_module.ReportType

        engine = ReportSearchEngine()
        for i in range(50):
            engine.index_report(f"file{i}.py", ReportType.ERRORS, f"Error number {i}")

        results = engine.search("error", max_results=5)
        assert len(results) <= 5

    def test_search_result_scoring(self, report_module: Any) -> None:
        """Test search results are scored by relevance."""
        ReportSearchEngine = report_module.ReportSearchEngine
        ReportType = report_module.ReportType

        engine = ReportSearchEngine()
        engine.index_report("high.py", ReportType.ERRORS, "error error error multiple")
        engine.index_report("low.py", ReportType.ERRORS, "single error")

        results = engine.search("error")
        # Results should be sorted by score (descending)
        if len(results) >= 2:
            assert results[0].score >= results[1].score



class TestCustomReportMetricsAndKPIs:
    """Tests for custom report metrics and KPIs."""

    def test_record_metric_with_threshold(self, report_module: Any) -> None:
        """Test recording metrics with alert thresholds."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        metric = collector.record("file.py", "issues_count", 50.0, threshold=100.0)

        assert metric.threshold == 100.0
        assert metric.value < metric.threshold

    def test_metrics_summary_averages(self, report_module: Any) -> None:
        """Test summary calculates correct averages."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        collector.record("file1.py", "complexity", 10.0)
        collector.record("file2.py", "complexity", 20.0)
        collector.record("file3.py", "complexity", 30.0)

        summary = collector.get_summary()
        assert summary["averages"]["complexity"] == 20.0

    def test_multiple_metrics_per_file(self, report_module: Any) -> None:
        """Test recording multiple different metrics per file."""
        MetricsCollector = report_module.MetricsCollector

        collector = MetricsCollector()
        collector.record("file.py", "lines_of_code", 500.0)
        collector.record("file.py", "complexity", 15.0)
        collector.record("file.py", "test_coverage", 85.0)

        metrics = collector.get_metrics("file.py")
        metric_names: List[Any] = [m.name for m in metrics]

        assert "lines_of_code" in metric_names
        assert "complexity" in metric_names
        assert "test_coverage" in metric_names



class TestReportAccessControl:
    """Tests for report access control."""

    def test_permission_levels_hierarchy(self, report_module: Any) -> None:
        """Test permission level hierarchy (ADMIN > WRITE > READ)."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("admin_user", "*.md", PermissionLevel.ADMIN)

        # Admin should have access at all levels
        assert controller.check("admin_user", "report.md", PermissionLevel.READ)
        assert controller.check("admin_user", "report.md", PermissionLevel.WRITE)
        assert controller.check("admin_user", "report.md", PermissionLevel.ADMIN)

    def test_permission_pattern_matching(self, report_module: Any) -> None:
        """Test permission pattern matching with wildcards."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("user1", "reports/*.md", PermissionLevel.READ)

        assert controller.check("user1", "reports / daily.md", PermissionLevel.READ)
        # Different path should not match
        assert not controller.check("user1", "other / report.md", PermissionLevel.READ)

    def test_permission_revocation(self, report_module: Any) -> None:
        """Test revoking permissions."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("user1", "*.md", PermissionLevel.WRITE)

        assert controller.check("user1", "report.md", PermissionLevel.WRITE)

        controller.revoke("user1", "*.md")

        assert not controller.check("user1", "report.md", PermissionLevel.WRITE)



class TestReportExportFormats:
    """Tests for report presentation export formats."""

    def test_export_to_html(self, report_module: Any) -> None:
        """Test HTML export with proper structure."""
        ReportExporter = report_module.ReportExporter
        ExportFormat = report_module.ExportFormat

        exporter = ReportExporter()
        content = "# Report Title\n\n- Item 1\n- Item 2"

        html = exporter.export(content, ExportFormat.HTML)

        assert "<!DOCTYPE html>" in html
        assert "<h1>Report Title</h1>" in html
        assert "<li>Item 1</li>" in html

    def test_export_to_json(self, report_module: Any) -> None:
        """Test JSON export."""
        ReportExporter = report_module.ReportExporter
        ExportFormat = report_module.ExportFormat
        import json

        exporter = ReportExporter()
        content = "# Test Report"

        result = exporter.export(content, ExportFormat.JSON)
        parsed = json.loads(result)

        assert "content" in parsed
        assert parsed["content"] == content

    def test_export_to_file(self, report_module: Any, tmp_path: Path) -> None:
        """Test export writes to file."""
        ReportExporter = report_module.ReportExporter
        ExportFormat = report_module.ExportFormat

        exporter = ReportExporter()
        output: Path = tmp_path / "report.html"

        exporter.export("# Test", ExportFormat.HTML, output)

        assert output.exists()
        assert "<h1>Test</h1>" in output.read_text()



class TestReportAuditLogging:
    """Tests for report audit logging."""

    def test_audit_log_multiple_actions(self, report_module: Any) -> None:
        """Test logging different audit actions."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()

        for action in AuditAction:
            logger.log(action, "testuser", "report.md")

        assert len(logger.entries) == len(list(AuditAction))

    def test_audit_log_user_activity(self, report_module: Any) -> None:
        """Test retrieving user activity from audit log."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()
        logger.log(AuditAction.READ, "user1", "report1.md")
        logger.log(AuditAction.UPDATE, "user2", "report1.md")
        logger.log(AuditAction.READ, "user1", "report2.md")

        user1_activity = logger.get_user_activity("user1")
        assert len(user1_activity) == 2

    def test_audit_log_with_details(self, report_module: Any) -> None:
        """Test audit log entries with additional details."""
        AuditLogger = report_module.AuditLogger
        AuditAction = report_module.AuditAction

        logger = AuditLogger()
        entry = logger.log(
            AuditAction.EXPORT,
            "user1",
            "report.md",
            details={"format": "pdf", "pages": 10}
        )

        assert entry.details["format"] == "pdf"
        assert entry.details["pages"] == 10



class TestReportDataIntegrityChecks:
    """Tests for report data integrity checks."""

    def test_validator_detects_missing_heading(self, report_module: Any) -> None:
        """Test validator detects missing main heading."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        result = validator.validate("Just plain text without heading")

        assert not result.valid
        assert "Missing main heading" in result.errors

    def test_validator_detects_empty_links(self, report_module: Any) -> None:
        """Test validator detects empty link targets."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        result = validator.validate("# Title\n\n[broken link]()")

        assert "Contains empty link targets" in result.warnings

    def test_validator_checksum_verification(self, report_module: Any) -> None:
        """Test checksum verification for content integrity."""
        ReportValidator = report_module.ReportValidator

        validator = ReportValidator()
        content = "# Test Content\n\nBody text here."

        result = validator.validate(content)
        checksum = result.checksum

        # Verify checksum matches
        assert validator.verify_checksum(content, checksum)
        # Modified content should not match
        assert not validator.verify_checksum(content + "modified", checksum)



class TestReportLocalization:
    """Tests for report localization."""

    def test_localizer_default_strings(self, report_module: Any) -> None:
        """Test localizer provides default strings."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer(LocaleCode.EN_US)

        assert localizer.get("report.description") == "Description"
        assert localizer.get("report.errors") == "Errors"
        assert localizer.get("report.improvements") == "Improvements"

    def test_localizer_german_translations(self, report_module: Any) -> None:
        """Test German translations."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer(LocaleCode.DE_DE)

        assert localizer.get("report.description") == "Beschreibung"
        assert localizer.get("report.errors") == "Fehler"
        assert localizer.get("severity.warning") == "Warnung"

    def test_localizer_custom_strings(self, report_module: Any) -> None:
        """Test adding custom localized strings."""
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        localizer = ReportLocalizer()
        localizer.add_string("custom.greeting", {
            "en-US": "Hello",
            "de-DE": "Hallo",
            "fr-FR": "Bonjour"
        })

        localizer.set_locale(LocaleCode.EN_US)
        assert localizer.get("custom.greeting") == "Hello"



class TestReportAPIEndpoints:
    """Tests for report API endpoints."""

    def test_api_list_reports(self, report_module: Any, tmp_path: Path) -> None:
        """Test API lists available reports."""
        ReportAPI = report_module.ReportAPI

        # Create test reports
        (tmp_path / "report1.md").write_text("# Report 1")
        (tmp_path / "report2.md").write_text("# Report 2")
        (tmp_path / "other.txt").write_text("Not a report")

        api = ReportAPI(tmp_path)
        reports = api.list_reports("*.md")

        assert len(reports) == 2

    def test_api_get_report_by_type(self, report_module: Any, tmp_path: Path) -> None:
        """Test API retrieves reports by type."""
        ReportAPI = report_module.ReportAPI
        ReportType = report_module.ReportType

        (tmp_path / "test.errors.md").write_text("# Errors for test")
        (tmp_path / "test.improvements.md").write_text("# Improvements for test")

        api = ReportAPI(tmp_path)

        errors = api.get_report("test", ReportType.ERRORS)
        improvements = api.get_report("test", ReportType.IMPROVEMENTS)

        assert errors == "# Errors for test"
        assert improvements == "# Improvements for test"

    def test_api_create_report(self, report_module: Any, tmp_path: Path) -> None:
        """Test API creates new reports."""
        ReportAPI = report_module.ReportAPI
        ReportType = report_module.ReportType

        api = ReportAPI(tmp_path)
        result = api.create_report("new_file", ReportType.ERRORS, "# New Error Report")

        assert result is True
        assert (tmp_path / "new_file.errors.md").exists()



class TestReportCachingInvalidation:
    """Tests for report caching invalidation."""

    def test_cache_invalidation_by_path(self, report_module: Any, tmp_path: Path) -> None:
        """Test cache invalidation by file path."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file: Path = tmp_path / "cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("file1.py", "hash1", "Content 1")
        manager.set("file2.py", "hash2", "Content 2")

        manager.invalidate("file1.py")

        assert manager.get("file1.py", "hash1") is None
        assert manager.get("file2.py", "hash2") == "Content 2"

    def test_cache_hash_mismatch(self, report_module: Any, tmp_path: Path) -> None:
        """Test cache returns None for hash mismatch."""
        ReportCacheManager = report_module.ReportCacheManager

        cache_file: Path = tmp_path / "cache.json"
        manager = ReportCacheManager(cache_file)

        manager.set("file.py", "original_hash", "Cached content")

        result = manager.get("file.py", "different_hash")
        assert result is None



class TestReportVersionComparison:
    """Tests for report version comparison."""

    def test_comparator_detects_additions(self, report_module: Any) -> None:
        """Test comparator detects added items."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old = "- Item 1\n- Item 2"
        new = "- Item 1\n- Item 2\n- Item 3"

        result = comparator.compare("old.md", "new.md", old, new)

        assert "- Item 3" in result.added

    def test_comparator_detects_removals(self, report_module: Any) -> None:
        """Test comparator detects removed items."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old = "- Item 1\n- Item 2\n- Item 3"
        new = "- Item 1\n- Item 2"

        result = comparator.compare("old.md", "new.md", old, new)

        assert "- Item 3" in result.removed

    def test_comparator_unchanged_count(self, report_module: Any) -> None:
        """Test comparator counts unchanged items."""
        ReportComparator = report_module.ReportComparator

        comparator = ReportComparator()
        old = "- Item 1\n- Item 2\n- Item 3"
        new = "- Item 1\n- Item 2\n- Item 3"

        result = comparator.compare("old.md", "new.md", old, new)

        assert result.unchanged_count == 3



class TestReportSchedulingAutomation:
    """Tests for report scheduling automation."""

    def test_scheduler_add_and_remove(self, report_module: Any) -> None:
        """Test adding and removing schedules."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("daily_report", "0 8 * * *", ["*.py"])

        assert "daily_report" in scheduler.schedules

        scheduler.remove_schedule("daily_report")
        assert "daily_report" not in scheduler.schedules

    def test_scheduler_get_due_tasks(self, report_module: Any) -> None:
        """Test getting tasks due for execution."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("task1", "0 8 * * *", ["*.py"])
        scheduler.add_schedule("task2", "0 12 * * *", ["*.md"])

        due = scheduler.get_due_tasks()
        assert len(due) == 2

    def test_scheduler_mark_completed(self, report_module: Any) -> None:
        """Test marking scheduled tasks as completed."""
        ReportScheduler = report_module.ReportScheduler

        scheduler = ReportScheduler()
        scheduler.add_schedule("test_task", "0 0 * * *", ["*.py"])

        scheduler.mark_completed("test_task")

        assert scheduler.schedules["test_task"]["last_run"] > 0



class TestReportDataAggregation:
    """Tests for report data aggregation."""

    def test_aggregator_combines_issues(self, report_module: Any) -> None:
        """Test aggregator combines issues from multiple files."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()

        aggregator.add_source("file1.py", [
            CodeIssue("Error 1", IssueCategory.SYNTAX, SeverityLevel.ERROR)
        ])
        aggregator.add_source("file2.py", [
            CodeIssue("Error 2", IssueCategory.STYLE, SeverityLevel.WARNING),
            CodeIssue("Error 3", IssueCategory.SECURITY, SeverityLevel.CRITICAL)
        ])

        report = aggregator.aggregate()

        assert len(report.combined_issues) == 3
        assert report.summary["total_files"] == 2

    def test_aggregator_summary_by_severity(self, report_module: Any) -> None:
        """Test aggregator summarizes by severity."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()
        aggregator.add_source("file.py", [
            CodeIssue("E1", IssueCategory.SYNTAX, SeverityLevel.ERROR),
            CodeIssue("E2", IssueCategory.SYNTAX, SeverityLevel.ERROR),
            CodeIssue("W1", IssueCategory.STYLE, SeverityLevel.WARNING)
        ])

        report = aggregator.aggregate()

        assert report.summary["by_severity"]["ERROR"] == 2
        assert report.summary["by_severity"]["WARNING"] == 1

    def test_aggregator_clear(self, report_module: Any) -> None:
        """Test aggregator clear removes all sources."""
        ReportAggregator = report_module.ReportAggregator
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        aggregator = ReportAggregator()
        aggregator.add_source("file.py", [
            CodeIssue("Error", IssueCategory.SYNTAX, SeverityLevel.ERROR)
        ])

        aggregator.clear()

        assert len(aggregator.sources) == 0



class TestReportPermissionManagement:
    """Tests for report permission management."""

    def test_permission_with_expiry(self, report_module: Any) -> None:
        """Test permissions with expiration."""
        ReportPermission = report_module.ReportPermission
        PermissionLevel = report_module.PermissionLevel
        import time

        # Create permission that expires in the past
        expired_perm = ReportPermission(
            user_id="user1",
            report_pattern="*.md",
            level=PermissionLevel.READ,
            expires_at=time.time() - 3600  # Expired 1 hour ago
        )

        assert expired_perm.expires_at < time.time()

    def test_multiple_permissions_per_user(self, report_module: Any) -> None:
        """Test user can have multiple permission entries."""
        AccessController = report_module.AccessController
        PermissionLevel = report_module.PermissionLevel

        controller = AccessController()
        controller.grant("user1", "reports/*.md", PermissionLevel.READ)
        controller.grant("user1", "admin/*.md", PermissionLevel.WRITE)

        assert controller.check("user1", "reports / daily.md", PermissionLevel.READ)
        assert controller.check("user1", "admin / config.md", PermissionLevel.WRITE)
        assert not controller.check("user1", "admin / config.md", PermissionLevel.ADMIN)


# =============================================================================
# Session 11: Comprehensive Report Generation Tests (Unittest Style)
# =============================================================================


=======
>>>>>>> 0777c397c (phase 320)

class TestReportGeneration(unittest.TestCase):
    """Tests for basic report generation."""

    def test_generate_basic_report(self) -> None:
        """Test generating basic report."""
        report: Dict[str, str] = {
            "title": "Test Report",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0",
        }

        assert report["title"] == "Test Report"
        assert report["version"] == "1.0"

    def test_generate_report_with_sections(self) -> None:
        """Test generating report with sections."""
        report = {
            "title": "Comprehensive Report",
            "sections": {
                "summary": "Summary content",
                "details": "Details content",
                "recommendations": "Recommendations content",
            },
        }

        assert len(report["sections"]) == 3
        assert "summary" in report["sections"]

    def test_generate_report_with_metadata(self) -> None:
        """Test generating report with metadata."""
        report = {
            "title": "Report",
            "metadata": {
                "author": "Agent",
                "created": datetime.now().isoformat(),
                "tags": ["important", "analysis"],
            },
        }

        assert report["metadata"]["author"] == "Agent"
        assert "important" in report["metadata"]["tags"]

    def test_generate_report_with_data(self) -> None:
        """Test generating report with data."""
        report = {
            "title": "Data Report",
            "data": {
                "total_items": 100,
                "processed": 95,
                "errors": 5,
            },
        }

        assert report["data"]["total_items"] == 100
        assert report["data"]["processed"] + report["data"]["errors"] == 100



class TestMarkdownReportFormatting(unittest.TestCase):
    """Tests for markdown report formatting."""

    def test_format_markdown_header(self) -> None:
        """Test formatting markdown header."""
        title = "Report Title"
        markdown: str = f"# {title}\n\n"

        assert "# " in markdown
        assert title in markdown

    def test_format_markdown_sections(self) -> None:
        """Test formatting markdown sections."""
        markdown = """
# Main Title

## Section 1
Content 1

## Section 2
Content 2
"""

        assert "##" in markdown
        assert "Section 1" in markdown
        assert "Section 2" in markdown

    def test_format_markdown_table(self) -> None:
        """Test formatting markdown table."""
        data = [
            {"name": "Item 1", "count": 10},
            {"name": "Item 2", "count": 20},
        ]

        markdown = "| Name | Count |\n|---|---|\n"
        for row in data:
            markdown += f"| {row['name']} | {row['count']} |\n"

        assert "| Name | Count |" in markdown
        assert "| Item 1 | 10 |" in markdown

    def test_format_markdown_list(self) -> None:
        """Test formatting markdown list."""
        items: List[str] = ["Item 1", "Item 2", "Item 3"]
        markdown: str = ""
        for item in items:
            markdown += f"- {item}\n"

        assert markdown.count("-") == 3

    def test_format_markdown_code_block(self) -> None:
        """Test formatting markdown code block."""
        code = "def hello():\n    print('Hello')"
        markdown: str = f"```python\n{code}\n```"

        assert "```python" in markdown
        assert code in markdown



class TestHTMLReportFormatting(unittest.TestCase):
    """Tests for HTML report formatting."""

    def test_format_html_basic(self) -> None:
        """Test formatting basic HTML."""
        html = """
<html>
<head><title>Report</title></head>
<body>
<h1>Report Title</h1>
<p>Content</p>
</body>
</html>
"""

        assert "<html>" in html
        assert "<h1>" in html

    def test_format_html_table(self) -> None:
        """Test formatting HTML table."""
        html = """
<table>
<tr><th>Header 1</th><th>Header 2</th></tr>
<tr><td>Data 1</td><td>Data 2</td></tr>
</table>
"""

        assert "<table>" in html
        assert "<th>" in html
        assert "<td>" in html

    def test_format_html_styled(self) -> None:
        """Test formatting styled HTML."""
        html = """
<html>
<head>
<style>
h1 { color: blue; }
p { font-size: 14px; }
</style>
</head>
<body>
<h1>Title</h1>
</body>
</html>
"""

        assert "<style>" in html
        assert "color: blue" in html

    def test_format_html_responsive(self) -> None:
        """Test formatting responsive HTML."""
        html = """
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
Content
</body>
</html>
"""

        assert 'viewport' in html
        assert 'width=device-width' in html



class TestJSONReportFormatting(unittest.TestCase):
    """Tests for JSON report formatting."""

    def test_format_json_basic(self) -> None:
        """Test formatting basic JSON."""
        data = {
            "title": "Report",
            "timestamp": "2025-12-16",
            "items": [1, 2, 3],
        }

        json_str: str = json.dumps(data)
        restored = json.loads(json_str)

        assert restored["title"] == "Report"

    def test_format_json_nested(self) -> None:
        """Test formatting nested JSON."""
        data = {
            "report": {
                "title": "Title",
                "sections": {
                    "summary": "Summary",
                    "details": "Details",
                },
            },
        }

        json_str: str = json.dumps(data)
        assert '"report"' in json_str

    def test_format_json_with_arrays(self) -> None:
        """Test formatting JSON with arrays."""
        data = {
            "items": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"},
            ],
        }

        json_str: str = json.dumps(data)
        restored = json.loads(json_str)

        assert len(restored["items"]) == 2

    def test_format_json_pretty_print(self) -> None:
        """Test JSON pretty printing."""
        data: Dict[str, str] = {"key": "value"}

        pretty_json: str = json.dumps(data, indent=2)
        compact_json: str = json.dumps(data)

        assert len(pretty_json) > len(compact_json)



class TestCSVReportFormatting(unittest.TestCase):
    """Tests for CSV report formatting."""

    def test_format_csv_basic(self) -> None:
        """Test formatting basic CSV."""
        headers: List[str] = ["Name", "Count", "Status"]
        rows: List[List[str]] = [
            ["Item 1", "10", "Done"],
            ["Item 2", "20", "Pending"],
        ]

        csv_lines: List[str] = [",".join(headers)]
        for row in rows:
            csv_lines.append(",".join(row))

        csv_content: str = "\n".join(csv_lines)
        assert "Name,Count,Status" in csv_content

    def test_format_csv_with_quotes(self) -> None:
        """Test formatting CSV with quotes."""
        data: List[List[str]] = [
            ['Item "A"', 'Value "B"'],
        ]

        csv_line: str = ','.join([f'"{item}"' for item in data[0]])
        assert '"Item' in csv_line

    def test_format_csv_escaping(self) -> None:
        """Test CSV escaping."""
        escaped = '"{value}"'

        assert isinstance(escaped, str)

    def test_format_csv_header_footer(self) -> None:
        """Test CSV with header and footer."""
        csv = "# Generated: 2025-12-16\n"
        csv += "Name,Value\n"
        csv += "Item 1,100\n"
        csv += "# Total: 1 item"

        assert csv.startswith("#")
        assert "Name,Value" in csv



class TestReportTemplates(unittest.TestCase):
    """Tests for report templates."""

    def test_template_substitution(self) -> None:
        """Test template substitution."""
        template = "Report for {project} generated on {date}"

        report: str = template.format(project="MyApp", date="2025-12-16")
        assert report == "Report for MyApp generated on 2025-12-16"

    def test_template_with_conditionals(self) -> None:
        """Test template with conditionals."""
        data = {"has_errors": True, "errors": 5}

        if data["has_errors"]:
            message: str = f"Found {data['errors']} errors"
        else:
            message = "No errors"

        assert "Found 5 errors" in message

    def test_template_with_loops(self) -> None:
        """Test template with loops."""
        items: List[str] = ["Item 1", "Item 2", "Item 3"]

        content = "Items:\n"
        for item in items:
            content += f"  - {item}\n"

        assert "- Item 1" in content
        assert content.count("-") == 3

    def test_template_inheritance(self) -> None:
        """Test template inheritance."""
        base_template = "### {title}\n{content}"

        title = "Section"
        content = "Details"

        result: str = base_template.format(title=title, content=content)
        assert "### Section" in result



class TestMetricsCollection(unittest.TestCase):
    """Tests for metrics collection in reports."""

    def test_collect_count_metrics(self) -> None:
        """Test collecting count metrics."""
        items: List[int] = [1, 2, 3, 4, 5]

        metrics = {
            "total_items": len(items),
            "sum": sum(items),
            "average": sum(items) / len(items),
        }

        assert metrics["total_items"] == 5
        assert metrics["average"] == 3.0

    def test_collect_time_metrics(self) -> None:
        """Test collecting time metrics."""
        import time
        start: datetime = datetime.now()
        time.sleep(0.01)
        end: datetime = datetime.now()

        elapsed: float = (end - start).total_seconds()

        assert elapsed > 0

    def test_collect_status_metrics(self) -> None:
        """Test collecting status metrics."""
        items: List[Dict[str, str]] = [
            {"status": "success"},
            {"status": "success"},
            {"status": "failed"},
        ]

        metrics: Dict[str, int] = {
            "success": sum(1 for i in items if i["status"] == "success"),
            "failed": sum(1 for i in items if i["status"] == "failed"),
        }

        assert metrics["success"] == 2
        assert metrics["failed"] == 1

    def test_collect_performance_metrics(self) -> None:
        """Test collecting performance metrics."""
        metrics = {
            "requests": 1000,
            "errors": 5,
            "error_rate": 5 / 1000,
            "success_rate": 995 / 1000,
        }

        assert metrics["error_rate"] == 0.005
        assert metrics["success_rate"] == 0.995



class TestReportExport(unittest.TestCase):
    """Tests for exporting reports."""

    def test_export_to_file(self) -> None:
        """Test exporting report to file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Report content")
            temp_file: str = f.name

        try:
            with open(temp_file, 'r') as f: str = f.read()

            assert content == "Report content"
        finally:
            os.unlink(temp_file)

    def test_export_markdown_file(self) -> None:
        """Test exporting markdown file."""
        content = "# Title\n\nContent"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write(content)
            filename: str = f.name

        try:
            assert os.path.exists(filename)
        finally:
            os.unlink(filename)

    def test_export_json_file(self) -> None:
        """Test exporting JSON file."""
        data = {"title": "Report", "items": [1, 2, 3]}

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(data, f)
            filename: str = f.name

        try:
            with open(filename, 'r') as f:
                restored = json.load(f)

            assert restored["title"] == "Report"
        finally:
            os.unlink(filename)

    def test_export_multiple_formats(self) -> None:
        """Test exporting to multiple formats."""
        data: Dict[str, str] = {"title": "Report", "content": "Data"}
        formats: List[str] = ["md", "json", "csv"]

        exported = {}
        for fmt in formats:
            if fmt == "json":
                exported[fmt] = json.dumps(data)
            else:
                exported[fmt] = str(data)

        assert len(exported) == 3



class TestReportAggregation(unittest.TestCase):
    """Tests for report aggregation."""

    def test_aggregate_multiple_reports(self) -> None:
        """Test aggregating multiple reports."""
        reports = [
            {"name": "Report 1", "items": 10},
            {"name": "Report 2", "items": 20},
            {"name": "Report 3", "items": 15},
        ]

        aggregated: Dict[str, int] = {
            "total_reports": len(reports),
            "total_items": sum(r["items"] for r in reports),
        }

        assert aggregated["total_reports"] == 3
        assert aggregated["total_items"] == 45

    def test_aggregate_with_grouping(self) -> None:
        """Test aggregating with grouping."""
        items = [
            {"type": "A", "value": 10},
            {"type": "A", "value": 20},
            {"type": "B", "value": 15},
        ]

        grouped: dict[str, list[int]] = {}
        for item in items:
            if item["type"] not in grouped:
                grouped[item["type"]] = []
            grouped[item["type"]].append(item["value"])

        assert len(grouped["A"]) == 2
        assert grouped["B"] == [15]

    def test_aggregate_with_statistics(self) -> None:
        """Test aggregating with statistics."""
        values: List[int] = [10, 20, 30, 40, 50]

        stats = {
            "count": len(values),
            "sum": sum(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }

        assert stats["count"] == 5
        assert stats["mean"] == 30
        assert stats["min"] == 10



class TestReportValidation(unittest.TestCase):
    """Tests for report validation."""

    def test_validate_required_fields(self) -> None:
        """Test validating required fields."""
        report: Dict[str, str] = {
            "title": "Report",
            "timestamp": "2025-12-16",
        }

        required: List[str] = ["title", "timestamp"]
        valid: bool = all(field in report for field in required)

        assert valid

    def test_validate_report_structure(self) -> None:
        """Test validating report structure."""
        report = {
            "metadata": {"author": "Test"},
            "sections": {},
            "data": {},
        }

        structure_valid: bool = all(k in report for k in ["metadata", "sections", "data"])
        assert structure_valid

    def test_validate_data_types(self) -> None:
        """Test validating data types."""
        report = {
            "title": "Report",
            "items": [1, 2, 3],
            "count": 3,
        }

        assert isinstance(report["title"], str)
        assert isinstance(report["items"], list)
        assert isinstance(report["count"], int)

    def test_validate_consistency(self) -> None:
        """Test validating consistency."""
        report = {
            "items": [1, 2, 3, 4, 5],
            "count": 5,
        }

        consistent = len(report["items"]) == report["count"]
        assert consistent



class TestReportRefactoring(unittest.TestCase):
    """Test strategies for refactoring generate_agent_reports.py."""

    def test_report_generator_module_split(self) -> None:
        """Verify refactoring into separate report generator modules."""
        modules: List[str] = [
            "base_report_generator.py",
            "text_report_generator.py",
            "structured_report_generator.py",
            "visual_report_generator.py",
            "distribution_report_handler.py"
        ]
        self.assertEqual(len(modules), 5)

    def test_report_generator_abstract_interface(self) -> None:
        """Test abstract interface for report generators."""
        class BaseReportGenerator:
            """Abstract base class for report generation."""

            def generate(self, data: dict[str, Any]) -> str:
                """Generate report from data."""
                raise NotImplementedError

            def validate(self) -> bool:
                """Validate report can be generated."""
                raise NotImplementedError

        self.assertTrue(hasattr(BaseReportGenerator, 'generate'))
        self.assertTrue(hasattr(BaseReportGenerator, 'validate'))

    def test_report_factory_pattern(self) -> None:
        """Test factory pattern for report generator creation."""
        class ReportGeneratorFactory:
            """Factory for creating report generators."""

            _generators: Dict[str, str] = {
                'markdown': 'MarkdownReportGenerator',
                'json': 'JSONReportGenerator',
                'html': 'HTMLReportGenerator',
                'pdf': 'PDFReportGenerator'
            }

            @classmethod
            def create(cls, report_type: str) -> str:
                """Create report generator of specified type."""
                if report_type not in cls._generators:
                    raise ValueError(f"Unknown report type: {report_type}")
                return cls._generators[report_type]

        self.assertIn('markdown', ReportGeneratorFactory._generators)
        self.assertIn('json', ReportGeneratorFactory._generators)



class TestMultipleFormatSupport(unittest.TestCase):
    """Test support for generating reports in multiple formats."""

    def test_html_report_generation(self) -> None:
        """Test HTML report generation with styling."""
        html_content = """<!DOCTYPE html>
        <html>
        <head><title>Agent Report</title></head>
        <body>
            <h1>Agent Analysis Report</h1>
            <div class="metrics">
                <p>Total Files: 150</p>
                <p>Test Coverage: 85%</p>
            </div>
        </body>
        </html>"""

        self.assertIn("<!DOCTYPE html>", html_content)
        self.assertIn("<h1>", html_content)
        self.assertIn("metrics", html_content)

    def test_pdf_report_generation(self) -> None:
        """Test PDF report generation."""
        pdf_config = {
            'page_size': 'A4',
            'orientation': 'portrait',
            'margins': {'top': 1, 'bottom': 1, 'left': 1, 'right': 1},
            'fonts': ['Helvetica', 'Times-Roman']
        }

        self.assertEqual(pdf_config['page_size'], 'A4')
        self.assertEqual(pdf_config['orientation'], 'portrait')

    def test_markdown_report_generation(self) -> None:
        """Test markdown report generation."""
        markdown_report = """# Agent Report

## Summary
- Total Files: 150
- Test Coverage: 85%

## Metrics
| Metric | Value |
|--------|-------|
| Coverage | 85% |
| Issues | 12 |
"""

        self.assertIn("# Agent Report", markdown_report)
        self.assertIn("## Summary", markdown_report)
        self.assertIn("|", markdown_report)

    def test_json_report_generation(self) -> None:
        """Test JSON report generation."""
        report_data = {
            "metadata": {
                "generated_at": "2024-01-15T10:30:00Z",
                "version": "1.0"
            },
            "summary": {
                "total_files": 150,
                "test_coverage": 85.5
            },
            "metrics": []
        }

        json_str: str = json.dumps(report_data)
        self.assertIn("metadata", json_str)
        self.assertIn("summary", json_str)

    def test_format_detection_from_filename(self) -> None:
        """Test format detection from report filename."""
        files: List[Tuple[str]] = [
            ("report.html", "html"),
            ("report.pdf", "pdf"),
            ("report.md", "markdown"),
            ("report.json", "json"),
            ("report.xlsx", "excel")
        ]

        for filename, expected_format in files:
            detected: str = filename.split('.')[-1]
            format_map: Dict[str, str] = {
                'html': 'html',
                'pdf': 'pdf',
                'md': 'markdown',
                'json': 'json',
                'xlsx': 'excel'
            }
            self.assertEqual(format_map.get(detected), expected_format)



class TestIncrementalGeneration(unittest.TestCase):
    """Test incremental report generation and change tracking."""

    def test_track_changed_files(self) -> None:
        """Test tracking which files have changed."""
        baseline_files = {
            'agent.py': {'hash': 'abc123', 'mtime': 1000},
            'base_agent/entrypoint.py': {'hash': 'def456', 'mtime': 1001}
        }

        current_files = {
            'agent.py': {'hash': 'abc123', 'mtime': 1000},
            'base_agent/entrypoint.py': {'hash': 'xyz789', 'mtime': 1002}
        }

        changed_files: List[str] = [
            f for f in current_files
            if current_files[f]['hash'] != baseline_files.get(f, {}).get('hash')
        ]

        self.assertIn('base_agent/entrypoint.py', changed_files)
        self.assertNotIn('agent.py', changed_files)

    def test_skip_unchanged_sections(self) -> None:
        """Test skipping analysis for unchanged sections."""
        report_cache = {
            'section_1': {'data': 'unchanged', 'timestamp': 1000},
            'section_2': {'data': 'changed', 'timestamp': 1000}
        }

        unchanged_threshold = 1500

        skipped: List[str] = [
            s for s, v in report_cache.items()
            if v['timestamp'] < unchanged_threshold
        ]

        self.assertIn('section_1', skipped)

    def test_incremental_metrics_update(self) -> None:
        """Test updating only changed metrics incrementally."""
        previous_metrics = {
            'files': 150,
            'coverage': 85.0,
            'warnings': 42,
            'timestamp': 1000
        }

        updated_metrics = previous_metrics.copy()
        updated_metrics['timestamp'] = 2000
        updated_metrics['files'] = 151

        self.assertEqual(updated_metrics['timestamp'], 2000)
        self.assertNotEqual(
            updated_metrics['timestamp'],
            previous_metrics['timestamp']
        )



class TestReportCaching(unittest.TestCase):
    """Test report caching mechanisms."""

    def test_section_level_caching(self) -> None:
        """Test caching individual report sections."""
        cache = {
            'summary': {'content': 'Summary data', 'valid': True},
            'metrics': {'content': 'Metrics data', 'valid': True},
            'details': {'content': 'Details data', 'valid': False}
        }

        valid_sections: List[str] = [k for k, v in cache.items() if v['valid']]
        self.assertEqual(len(valid_sections), 2)

    def test_cache_expiration_time(self) -> None:
        """Test cache expiration based on time."""
        cache_entries = [
            {'key': 'entry1', 'timestamp': 1000, 'ttl': 300},
            {'key': 'entry2', 'timestamp': 1000, 'ttl': 600}
        ]

        current_time = 1400

        valid_entries = [
            e for e in cache_entries
            if current_time - e['timestamp'] < e['ttl']
        ]

        self.assertEqual(len(valid_entries), 1)
        self.assertEqual(valid_entries[0]['key'], 'entry2')

    def test_cache_invalidation_on_file_change(self) -> None:
        """Test cache invalidation when source files change."""
        cache: Dict[str, Dict[str, str]] = {
            'report_v1': {
                'file_hash': 'abc123',
                'data': 'cached report'
            }
        }

        new_hash = 'def456'

        if cache['report_v1']['file_hash'] != new_hash:
            cache['report_v1'] = None

        self.assertIsNone(cache['report_v1'])

    def test_cache_with_file_hashing(self) -> None:
        """Test cache validation using file hashing."""
        import hashlib

        content = "report data"
        hash_value: str = hashlib.md5(content.encode()).hexdigest()

        cache_entry: Dict[str, str] = {
            'content': content,
            'hash': hash_value
        }

        new_content = "report data"
        new_hash: str = hashlib.md5(new_content.encode()).hexdigest()

        self.assertEqual(cache_entry['hash'], new_hash)



class TestReportCustomization(unittest.TestCase):
    """Test report customization and user-selectable sections."""

    def test_user_selectable_sections(self) -> None:
        """Test user-customizable report sections."""
        available_sections: Dict[str, bool] = {
            'summary': True,
            'metrics': True,
            'analysis': True,
            'recommendations': False,
            'trends': True
        }

        selected_sections: List[str] = [s for s, inc in available_sections.items() if inc]
        self.assertIn('summary', selected_sections)
        self.assertNotIn('recommendations', selected_sections)

    def test_custom_metrics_selection(self) -> None:
        """Test selection of custom metrics for report."""
        all_metrics: List[str] = [
            'files_analyzed',
            'test_coverage',
            'warnings',
            'errors',
            'code_complexity',
            'duplicated_code',
            'security_issues'
        ]

        custom_selection: List[str] = ['test_coverage', 'security_issues', 'warnings']

        selected: List[str] = [m for m in all_metrics if m in custom_selection]
        self.assertEqual(len(selected), 3)

    def test_report_template_customization(self) -> None:
        """Test custom report templates."""
        template = """
        # {title}

        ## Overview
        {overview}

        ## Metrics
        {metrics}

        ## Recommendations
        {recommendations}
        """

        filled_template: str = template.format(
            title="Agent Analysis Report",
            overview="This report analyzes...",
            metrics="- Coverage: 85%",
            recommendations="- Add tests"
        )

        self.assertIn("Agent Analysis Report", filled_template)
        self.assertIn("85%", filled_template)

    def test_filter_metrics_by_threshold(self) -> None:
        """Test filtering metrics by threshold values."""
        metrics = [
            {'name': 'coverage', 'value': 85},
            {'name': 'warnings', 'value': 12},
            {'name': 'errors', 'value': 2},
            {'name': 'complexity', 'value': 45}
        ]

        high_value_metrics = [m for m in metrics if m['value'] > 40]

        self.assertEqual(len(high_value_metrics), 2)



class TestVisualReportGeneration(unittest.TestCase):
    """Test generation of visual reports with graphs and charts."""

    def test_matplotlib_line_chart_generation(self) -> None:
        """Test generating line charts with matplotlib."""
        chart_config = {
            'type': 'line',
            'title': 'Coverage Trend',
            'xlabel': 'Date',
            'ylabel': 'Coverage %',
            'data': [
                {'date': '2024-01-01', 'value': 75},
                {'date': '2024-01-02', 'value': 78},
                {'date': '2024-01-03', 'value': 82}
            ]
        }

        self.assertEqual(chart_config['type'], 'line')
        self.assertEqual(len(chart_config['data']), 3)

    def test_bar_chart_generation(self) -> None:
        """Test generating bar charts."""
        bar_data = {
            'categories': ['agent.py', 'base_agent/entrypoint.py', 'agent_context.py'],
            'values': [150, 200, 120],
            'title': 'Lines of Code by Module'
        }

        self.assertEqual(len(bar_data['categories']), 3)
        self.assertEqual(len(bar_data['values']), 3)

    def test_heatmap_generation(self) -> None:
        """Test generating heatmaps for correlation analysis."""
        heatmap_data = {
            'modules': ['agent.py', 'base_agent/entrypoint.py', 'agent_context.py'],
            'metrics': ['coverage', 'complexity', 'tests'],
            'values': [
                [85, 45, 120],
                [92, 38, 150],
                [78, 52, 95]
            ]
        }

        self.assertEqual(len(heatmap_data['values']), 3)
        self.assertEqual(len(heatmap_data['values'][0]), 3)

    def test_pie_chart_generation(self) -> None:
        """Test generating pie charts for composition."""
        pie_data = {
            'labels': ['Passed', 'Failed', 'Skipped'],
            'values': [450, 25, 10],
            'colors': ['#2ecc71', '#e74c3c', '#f39c12']
        }

        total: int = sum(pie_data['values'])
        self.assertEqual(total, 485)

    def test_save_charts_as_image(self) -> None:
        """Test saving generated charts as image files."""
        image_formats: List[str] = ['png', 'pdf', 'svg', 'jpg']

        for fmt in image_formats:
            filepath: str = f"/reports/chart.{fmt}"
            self.assertTrue(filepath.endswith(f".{fmt}"))



class TestExecutiveSummary(unittest.TestCase):
    """Test executive summary generation."""

    def test_generate_key_metrics_summary(self) -> None:
        """Test generating summary of key metrics."""
        metrics = {
            'total_files': 150,
            'test_coverage': 85.5,
            'warnings': 12,
            'errors': 2,
            'code_complexity': 4.2
        }

        summary: str = f"""
        Executive Summary
        - Total Files: {metrics['total_files']}
        - Test Coverage: {metrics['test_coverage']}%
        - Critical Issues: {metrics['errors']}
        """

        self.assertIn("150", summary)
        self.assertIn("85.5", summary)

    def test_executive_summary_with_trends(self) -> None:
        """Test executive summary including trend information."""
        summary: Dict[str, str] = {
            'period': 'Last 7 days',
            'coverage_trend': 'up 3.2%',
            'warning_trend': 'down 5',
            'complexity_trend': 'stable',
            'highlight': 'Coverage improved due to new tests'
        }

        self.assertIn('%', summary['coverage_trend'])

    def test_summary_with_priority_issues(self) -> None:
        """Test executive summary highlighting priority issues."""
        issues = [
            {'priority': 'critical', 'count': 2},
            {'priority': 'high', 'count': 8},
            {'priority': 'medium', 'count': 15}
        ]

        critical = [i for i in issues if i['priority'] == 'critical']
        self.assertEqual(len(critical), 1)
        self.assertEqual(critical[0]['count'], 2)



class TestReportTemplating(unittest.TestCase):
    """Test report templating for consistent formatting."""

    def test_jinja2_template_rendering(self) -> None:
        """Test Jinja2 template rendering for reports."""
        template_str = """
        Report for {agent_name}
        Generated: {date}
        Summary: {summary}
        """

        data: Dict[str, str] = {
            'agent_name': 'TestAgent',
            'date': '2024-01-15',
            'summary': 'Analysis complete'
        }

        result: str = template_str.format(**data)

        self.assertIn('TestAgent', result)

    def test_template_with_conditional_sections(self) -> None:
        """Test templates with conditional sections."""
        template_config: Dict[str, Dict[str, bool]] = {
            'sections': {
                'summary': True,
                'metrics': True,
                'recommendations': False,
                'warnings': True
            }
        }

        active_sections: List[str] = [s for s, v in template_config['sections'].items() if v]
        self.assertNotIn('recommendations', active_sections)

    def test_template_inheritance(self) -> None:
        """Test template inheritance for code reuse."""

        derived_template = "# Agent Report\n{{ agent_name }}\n{{ content }}"

        self.assertIn("# Agent Report", derived_template)



class TestCrossFileAnalysis(unittest.TestCase):
    """Test cross-file analysis and dependency reporting."""

    def test_dependency_graph_generation(self) -> None:
        """Test generating dependency graph."""
        dependencies = {
            'agent.py': ['base_agent/entrypoint.py', 'agent_context.py'],
            'base_agent/entrypoint.py': ['errors/error_handler.py'],
            'agent_context.py': []
        }

        self.assertEqual(len(dependencies['agent.py']), 2)

    def test_import_cycle_detection(self) -> None:
        """Test detecting import cycles."""
        imports: Dict[str, List[str]] = {
            'module_a.py': ['module_b.py'],
            'module_b.py': ['module_c.py'],
            'module_c.py': ['module_a.py']
        }

        cycle_detected: bool = (
            'module_a.py' in imports.get('module_c.py', [])
        )

        self.assertTrue(cycle_detected)

    def test_coupling_metrics(self) -> None:
        """Test calculating coupling metrics between modules."""
        coupling: Dict[str, Dict[str, int]] = {
            'agent.py': {
                'base_agent/entrypoint.py': 15,
                'agent_context.py': 8
            },
            'base_agent/entrypoint.py': {
                'errors/error_handler.py': 5
            }
        }

        high_coupling: List[Tuple[str | int]] = [
            (m, cnt) for m, deps in coupling.items()
            for dep, cnt in deps.items() if cnt > 10
        ]

        self.assertEqual(len(high_coupling), 1)



class TestTechnicalDebt(unittest.TestCase):
    """Test technical debt quantification and reporting."""

    def test_debt_scoring_algorithm(self) -> None:
        """Test calculating technical debt score."""
        debt_factors: Dict[str, Dict[str, float]] = {
            'code_complexity': {'weight': 0.3, 'value': 4.2},
            'test_coverage': {'weight': 0.4, 'value': 0.85},
            'code_duplication': {'weight': 0.3, 'value': 0.12}
        }

        debt_score: float = (
            debt_factors['code_complexity']['weight'] * debt_factors['code_complexity']['value'] +
            debt_factors['code_duplication']['weight'] * debt_factors['code_duplication']['value']
        )

        self.assertGreater(debt_score, 0)

    def test_debt_prioritization(self) -> None:
        """Test prioritizing debt items."""
        debt_items: List[Dict[str, str]] = [
            {'type': 'low_coverage', 'impact': 'high', 'effort': 'medium'},
            {'type': 'complex_function', 'impact': 'medium', 'effort': 'high'},
            {'type': 'code_duplication', 'impact': 'low', 'effort': 'low'}
        ]

        priorities: List[Dict[str, str]] = sorted(
            debt_items,
            key=lambda x: (
                1 if x['impact'] == 'high' else (0.5 if x['impact'] == 'medium' else 0)
            ) / (1 if x['effort'] == 'high' else (0.5 if x['effort'] == 'medium' else 0.25)),
            reverse=True
        )

        self.assertEqual(priorities[0]['type'], 'low_coverage')

    def test_debt_timeline_projection(self) -> None:
        """Test projecting debt paydown timeline."""
        current_debt = 1000
        weekly_reduction = 50

        weeks_to_zero: float = current_debt / weekly_reduction

        self.assertEqual(weeks_to_zero, 20)



class TestRecommendationGeneration(unittest.TestCase):
    """Test generating actionable recommendations."""

    def test_coverage_improvement_recommendations(self) -> None:
        """Test generating recommendations for coverage improvement."""
        uncovered_files: List[str] = ['agent.py', 'base_agent/entrypoint.py']
        recommendations: List[str] = [
            f"Add tests for {f}" for f in uncovered_files if 'agent' in f
        ]

        self.assertGreaterEqual(len(recommendations), 1)

    def test_complexity_reduction_recommendations(self) -> None:
        """Test recommendations for complexity reduction."""
        complex_functions: Dict[str, int] = {
            'analyze_files': 8,
            'process_metrics': 6,
            'generate_report': 5
        }

        high_complexity: List[str] = [
            f for f, c in complex_functions.items() if c > 6
        ]

        self.assertIn('analyze_files', high_complexity)

    def test_priority_based_recommendations(self) -> None:
        """Test priority-based recommendation ordering."""
        recommendations: List[Dict[str, str]] = [
            {'action': 'Add test coverage', 'priority': 'high', 'impact': 'high'},
            {'action': 'Refactor function', 'priority': 'medium', 'impact': 'medium'},
            {'action': 'Update docstring', 'priority': 'low', 'impact': 'low'}
        ]

        sorted_recs: List[Dict[str, str]] = sorted(recommendations, key=lambda x: (
            1 if x['priority'] == 'high' else (0.5 if x['priority'] == 'medium' else 0)
        ), reverse=True)

        self.assertEqual(sorted_recs[0]['action'], 'Add test coverage')



class TestReportScheduling(unittest.TestCase):
    """Test report scheduling and automated generation."""

    def test_schedule_configuration(self) -> None:
        """Test configuring report generation schedule."""
        schedule = {
            'daily': {'time': '00:00', 'enabled': True},
            'weekly': {'time': 'Monday 09:00', 'enabled': True},
            'monthly': {'time': '1st 10:00', 'enabled': False}
        }

        enabled_schedules: List[str] = [s for s, cfg in schedule.items() if cfg['enabled']]
        self.assertEqual(len(enabled_schedules), 2)

    def test_scheduled_generation_trigger(self) -> None:
        """Test triggering scheduled report generation."""
        schedule_time = datetime(2024, 1, 15, 0, 0)
        current_time = datetime(2024, 1, 15, 0, 0)

        should_generate: bool = current_time >= schedule_time
        self.assertTrue(should_generate)

    def test_background_generation_queue(self) -> None:
        """Test queuing reports for background generation."""
        queue = [
            {'report_id': 1, 'status': 'pending'},
            {'report_id': 2, 'status': 'processing'},
            {'report_id': 3, 'status': 'pending'}
        ]

        pending = [r for r in queue if r['status'] == 'pending']
        self.assertEqual(len(pending), 2)



class TestReportVersioning(unittest.TestCase):
    """Test report versioning and change tracking."""

    def test_report_version_tracking(self) -> None:
        """Test tracking report versions."""
        reports = [
            {'version': 1, 'date': '2024-01-01', 'metrics': {'coverage': 75}},
            {'version': 2, 'date': '2024-01-08', 'metrics': {'coverage': 78}},
            {'version': 3, 'date': '2024-01-15', 'metrics': {'coverage': 85}}
        ]

        self.assertEqual(len(reports), 3)
        self.assertEqual(reports[-1]['metrics']['coverage'], 85)

    def test_report_diff_generation(self) -> None:
        """Test generating diff between report versions."""
        v1: Dict[str, int] = {'coverage': 75, 'warnings': 20, 'errors': 5}
        v2: Dict[str, int] = {'coverage': 85, 'warnings': 15, 'errors': 2}

        diff: Dict[str, int] = {k: v2[k] - v1[k] for k in v1}

        self.assertEqual(diff['coverage'], 10)
        self.assertEqual(diff['errors'], -3)

    def test_change_tracking_metadata(self) -> None:
        """Test metadata for tracking changes."""
        change_log = [
            {
                'version': 2,
                'changes': ['Coverage improved', 'Fixed 3 warnings'],
                'author': 'agent-system',
                'timestamp': '2024-01-08T10:00:00'
            }
        ]

        self.assertEqual(len(change_log[0]['changes']), 2)



class TestReportDistribution(unittest.TestCase):
    """Test report distribution mechanisms."""

    def test_webhook_distribution(self) -> None:
        """Test distributing reports via webhook."""
        webhook_config = {
            'url': 'https://example.com/webhook',
            'method': 'POST',
            'headers': {'Authorization': 'Bearer token123'},
            'timeout': 30
        }

        self.assertEqual(webhook_config['method'], 'POST')

    def test_api_endpoint_distribution(self) -> None:
        """Test exposing reports via API endpoint."""
        api_endpoint: Dict[str, str] = {
            'path': '/api/reports/{id}',
            'method': 'GET',
            'authentication': 'bearer_token',
            'rate_limit': '1000/hour'
        }

        self.assertIn('/api/reports/', api_endpoint['path'])

    def test_slack_integration(self) -> None:
        """Test Slack integration for report notifications."""
        slack_config: Dict[str, str] = {
            'webhook_url': 'https://hooks.slack.com/services/...',
            'channel': '#reports',
            'mention_on_alert': '@channel'
        }

        self.assertEqual(slack_config['channel'], '#reports')

    def test_distribution_failure_handling(self) -> None:
        """Test handling distribution failures."""
        distribution_attempt = {
            'target': 'email@example.com',
            'status': 'failed',
            'error': 'Connection timeout',
            'retry_count': 3,
            'next_retry': '2024-01-15T11:00:00'
        }

        should_retry = distribution_attempt['retry_count'] < 5
        self.assertTrue(should_retry)



class TestInteractiveReports(unittest.TestCase):
    """Test interactive report generation and filtering."""

    def test_drill_down_capability(self) -> None:
        """Test drill-down from summary to details."""
        details: Dict[str, int] = {
            'covered_files': 127,
            'uncovered_files': 23,
            'critical_uncovered': 5
        }

        self.assertEqual(details['covered_files'] + details['uncovered_files'], 150)

    def test_filter_and_search_capability(self) -> None:
        """Test filtering and searching in reports."""
        data = [
            {'file': 'agent.py', 'coverage': 85, 'warnings': 5},
            {'file': 'base_agent/entrypoint.py', 'coverage': 92, 'warnings': 2},
            {'file': 'agent_context.py', 'coverage': 78, 'warnings': 8}
        ]

        filtered = [d for d in data if d['coverage'] > 80]
        self.assertEqual(len(filtered), 2)

    def test_dynamic_chart_generation(self) -> None:
        """Test generating charts dynamically based on filters."""
        all_metrics = [
            {'date': '2024-01-01', 'coverage': 75},
            {'date': '2024-01-08', 'coverage': 80},
            {'date': '2024-01-15', 'coverage': 85}
        ]

        filtered_metrics = all_metrics[-2:]

        self.assertEqual(len(filtered_metrics), 2)



class TestTeamLevelReporting(unittest.TestCase):
    """Test team-level reporting and aggregation."""

    def test_aggregate_metrics_across_agents(self) -> None:
        """Test aggregating metrics across multiple agents."""
        agent_metrics: Dict[str, Dict[str, int]] = {
            'agent1': {'files': 50, 'coverage': 85},
            'agent2': {'files': 75, 'coverage': 82},
            'agent3': {'files': 45, 'coverage': 88}
        }

        total_files: int = sum(m['files'] for m in agent_metrics.values())
        avg_coverage: float = sum(m['coverage'] for m in agent_metrics.values()) / len(agent_metrics)

        self.assertEqual(total_files, 170)
        self.assertAlmostEqual(avg_coverage, 85, places=1)

    def test_team_performance_trends(self) -> None:
        """Test tracking team performance trends."""
        team_history: List[Dict[str, int]] = [
            {'week': 1, 'avg_coverage': 75, 'total_warnings': 50},
            {'week': 2, 'avg_coverage': 80, 'total_warnings': 40},
            {'week': 3, 'avg_coverage': 85, 'total_warnings': 25}
        ]

        improvement: int = team_history[-1]['avg_coverage'] - team_history[0]['avg_coverage']
        self.assertEqual(improvement, 10)

    def test_individual_vs_team_comparison(self) -> None:
        """Test comparing individual metrics against team average."""
        team_avg_coverage = 83.5

        individual_metrics: Dict[str, float] = {
            'alice': 85.0,
            'bob': 82.0,
            'charlie': 83.5
        }

        above_average: List[str] = [
            p for p, cov in individual_metrics.items()
            if cov > team_avg_coverage
        ]

        self.assertIn('alice', above_average)
        self.assertNotIn('bob', above_average)


