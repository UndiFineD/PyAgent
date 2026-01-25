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
"""Core test classes for observability reports - Enums and Dataclasses."""

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
