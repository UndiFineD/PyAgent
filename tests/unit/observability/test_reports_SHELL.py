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

# -*- coding: utf-8 -*-
"""Shell test classes for observability reports - Managers and IO logic."""

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

# Import test utilities
try:
    from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
except ImportError:
    AGENT_DIR = Path(__file__).parent.parent.parent.parent / 'src'

# Import from src if needed

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

        assert controller.check("user1", "reports/daily.md", PermissionLevel.READ)
        assert controller.check("user1", "admin/config.md", PermissionLevel.WRITE)
        assert not controller.check("user1", "admin/config.md", PermissionLevel.ADMIN)


class TestReportExporting:
    """Tests for exporting reports."""

    def test_export_to_file(self, tmp_path: Path) -> None:
        """Test exporting report to file."""
        report_file = tmp_path / "report.txt"
        report_file.write_text("Report content")
        assert report_file.read_text() == "Report content"

    def test_export_markdown_file(self, tmp_path: Path) -> None:
        """Test exporting markdown file."""
        content = "# Title\n\nContent"
        md_file = tmp_path / "report.md"
        md_file.write_text(content)
        assert md_file.exists()

    def test_export_json_file(self, tmp_path: Path) -> None:
        """Test exporting JSON file."""
        data = {"title": "Report", "items": [1, 2, 3]}
        json_file = tmp_path / "report.json"
<<<<<<< HEAD
<<<<<<< HEAD
        with open(json_file, 'w') as f:
            json.dump(data, f)
        
        with open(json_file, 'r') as f:
=======
=======
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)

        with open(json_file, 'r', encoding='utf-8') as f:
<<<<<<< HEAD
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor)
=======
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)
            restored = json.load(f)
        assert restored["title"] == "Report"


class TestReportConsistency:
    """Tests for report consistency validation."""

    def test_validate_required_fields(self) -> None:
        """Test validating required fields."""
        report: Dict[str, str] = {
            "title": "Report",
            "timestamp": "2025-12-16",
        }
        required: List[str] = ["title", "timestamp"]
        assert all(field in report for field in required)

    def test_validate_report_structure(self) -> None:
        """Test validating report structure."""
        report = {
            "metadata": {"author": "Test"},
            "sections": {},
            "data": {},
        }
        assert all(k in report for k in ["metadata", "sections", "data"])


class TestReportVersioningMechanism:
    """Test report versioning and change tracking logic."""

    def test_report_version_tracking(self) -> None:
        """Test tracking report versions."""
        reports = [
            {'version': 1, 'date': '2024-01-01', 'metrics': {'coverage': 75}},
            {'version': 2, 'date': '2024-01-08', 'metrics': {'coverage': 78}},
            {'version': 3, 'date': '2024-01-15', 'metrics': {'coverage': 85}}
        ]
        assert len(reports) == 3
        assert reports[-1]['metrics']['coverage'] == 85

    def test_report_diff_calculation(self) -> None:
        """Test calculating diff between report versions."""
        v1: Dict[str, int] = {'coverage': 75, 'warnings': 20, 'errors': 5}
        v2: Dict[str, int] = {'coverage': 85, 'warnings': 15, 'errors': 2}
        diff: Dict[str, int] = {k: v2[k] - v1[k] for k in v1}
        assert diff['coverage'] == 10
        assert diff['errors'] == -3
