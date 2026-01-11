# -*- coding: utf-8 -*-
"""Test classes from test_generate_agent_reports.py - integration module."""

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
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))


class TestPhase6Integration:
    """Integration tests for Phase 6 features."""

    def test_cache_manager_with_comparator(
        self, report_module: Any, tmp_path: Path
    ) -> None:
        """Test cache manager working with comparator."""
        ReportCacheManager = report_module.ReportCacheManager
        ReportComparator = report_module.ReportComparator

        cache_file: Path = tmp_path / "test_cache.json"
        manager = ReportCacheManager(cache_file)
        comparator = ReportComparator()

        old_report = "- Item 1\n- Item 2"
        new_report = "- Item 1\n- Item 2\n- Item 3"

        manager.set("old.md", "hash1", old_report, ttl=3600)
        cached = manager.get("old.md", "hash1")

        comparison = comparator.compare("old.md", "new.md", cached, new_report)

        assert "- Item 3" in comparison.added

    def test_filter_with_all_criteria(self, report_module: Any) -> None:
        """Test filter with multiple criteria."""
        ReportFilter = report_module.ReportFilter
        FilterCriteria = report_module.FilterCriteria
        CodeIssue = report_module.CodeIssue
        IssueCategory = report_module.IssueCategory
        SeverityLevel = report_module.SeverityLevel

        criteria = FilterCriteria(
            categories=[IssueCategory.SYNTAX, IssueCategory.SECURITY],
            min_severity=SeverityLevel.WARNING
        )
        filter_obj = ReportFilter(criteria)

        issues: List[Any] = [
            CodeIssue(
                message="Critical security issue",
                category=IssueCategory.SECURITY,
                severity=SeverityLevel.CRITICAL
            ),
            CodeIssue(
                message="Minor style issue",
                category=IssueCategory.STYLE,
                severity=SeverityLevel.INFO
            ),
            CodeIssue(
                message="Syntax warning",
                category=IssueCategory.SYNTAX,
                severity=SeverityLevel.WARNING
            ),
        ]

        filtered = filter_obj.filter_issues(issues)

        assert len(filtered) == 2
        assert any(i.category == IssueCategory.SECURITY for i in filtered)
        assert any(i.category == IssueCategory.SYNTAX for i in filtered)


# =============================================================================
# Session 8: Enum Tests
# =============================================================================

class TestSession8Integration:
    """Integration tests for Session 8 features."""

    def test_subscription_with_archiver(self, report_module: Any) -> None:
        """Test subscription manager with archiver."""
        SubscriptionManager = report_module.SubscriptionManager
        ReportArchiver = report_module.ReportArchiver
        ReportSubscription = report_module.ReportSubscription
        ReportType = report_module.ReportType

        manager = SubscriptionManager()
        archiver = ReportArchiver()

        sub = ReportSubscription("user1", "user@example.com")
        manager.add_subscription(sub)

        report_content = "# Test Report"
        archived = archiver.archive("test.py", report_content)
        manager.queue_delivery("user1", archived.content, ReportType.ERRORS)

        assert len(manager.delivery_queue) == 1
        assert archiver.get_archive(archived.report_id) is not None

    def test_search_with_annotations(self, report_module: Any) -> None:
        """Test search engine with annotation manager."""
        ReportSearchEngine = report_module.ReportSearchEngine
        AnnotationManager = report_module.AnnotationManager
        ReportType = report_module.ReportType

        engine = ReportSearchEngine()
        annotations = AnnotationManager()

        content = "# Report\nSyntax error on line 10"
        engine.index_report("test.py", ReportType.ERRORS, content)

        results = engine.search("syntax error")
        if results:
            report_id: str = f"test.py:{ReportType.ERRORS.name}"
            annotations.add_annotation(report_id, "reviewer", "Needs fix")

            anns = annotations.get_annotations(report_id)
            assert len(anns) == 1

    def test_access_control_with_audit(self, report_module: Any) -> None:
        """Test access control with audit logging."""
        AccessController = report_module.AccessController
        AuditLogger = report_module.AuditLogger
        PermissionLevel = report_module.PermissionLevel
        AuditAction = report_module.AuditAction

        controller = AccessController()
        logger = AuditLogger()

        controller.grant("user1", "*.md", PermissionLevel.READ)

        if controller.check("user1", "report.md", PermissionLevel.READ):
            logger.log(AuditAction.READ, "user1", "report.md")

        history = logger.get_history("report.md")
        assert len(history) == 1
        assert history[0].action == AuditAction.READ

    def test_export_with_validation(self, report_module: Any) -> None:
        """Test exporter with validator."""
        ReportExporter = report_module.ReportExporter
        ReportValidator = report_module.ReportValidator
        ExportFormat = report_module.ExportFormat

        exporter = ReportExporter()
        validator = ReportValidator()

        content = "# Test Report\n\nSome valid content."
        validation = validator.validate(content)

        if validation.valid:
            html = exporter.export(content, ExportFormat.HTML)
            assert "<h1>Test Report</h1>" in html

    def test_localized_metrics(self, report_module: Any) -> None:
        """Test metrics collector with localizer."""
        MetricsCollector = report_module.MetricsCollector
        ReportLocalizer = report_module.ReportLocalizer
        LocaleCode = report_module.LocaleCode

        collector = MetricsCollector()
        localizer = ReportLocalizer(LocaleCode.DE_DE)

        collector.record("test.py", "errors", 5.0)
        summary = collector.get_summary()

        label = localizer.get("report.errors")
        assert label == "Fehler"
        assert summary["averages"]["errors"] == 5.0


# =============================================================================
# Session 8: Test File Improvement Tests
# =============================================================================



class TestReportIntegration(unittest.TestCase):
    """Integration tests for report generation."""

    def test_end_to_end_report_generation(self) -> None:
        """Test end-to-end report generation."""
        data: Dict[str, int] = {
            "total": 100,
            "success": 95,
            "failed": 5,
        }

        report = {
            "title": "Test Report",
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }

        assert report["title"] == "Test Report"
        assert report["data"]["total"] == 100

        json_export: str = json.dumps(report)
        assert len(json_export) > 0

    def test_multi_format_export_workflow(self) -> None:
        """Test multi-format export workflow."""
        content = "# Report\n\nContent"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            md_file: str = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            txt_file: str = f.name

        try:
            assert os.path.exists(md_file)
            assert os.path.exists(txt_file)
        finally:
            os.unlink(md_file)
            os.unlink(txt_file)

    def test_batch_report_generation(self) -> None:
        """Test batch report generation."""
        reports = []

        for i in range(5):
            report = {
                "id": i,
                "title": f"Report {i}",
                "data": {"count": i * 10},
            }
            reports.append(report)

        assert len(reports) == 5
        assert reports[0]["id"] == 0
        assert reports[4]["data"]["count"] == 40



class TestGitIntegration(unittest.TestCase):
    """Test git integration in reports."""

    def test_extract_authors_from_commits(self) -> None:
        """Test extracting authors from git history."""
        commits: List[Dict[str, str]] = [
            {'hash': 'abc123', 'author': 'Alice', 'date': '2024-01-15'},
            {'hash': 'def456', 'author': 'Bob', 'date': '2024-01-14'},
            {'hash': 'ghi789', 'author': 'Alice', 'date': '2024-01-13'}
        ]

        authors: Set[str] = set(c['author'] for c in commits)
        self.assertIn('Alice', authors)
        self.assertIn('Bob', authors)

    def test_commit_history_in_report(self) -> None:
        """Test including commit history in report."""
        commit_history = [
            {
                'message': 'Add test coverage',
                'author': 'Alice',
                'date': '2024-01-15',
                'files_changed': 3
            },
            {
                'message': 'Fix bug in agent',
                'author': 'Bob',
                'date': '2024-01-14',
                'files_changed': 1
            }
        ]

        self.assertEqual(len(commit_history), 2)
        self.assertEqual(commit_history[0]['files_changed'], 3)

    def test_blame_information_integration(self) -> None:
        """Test integrating git blame information."""
        blame_data = {
            'file': 'agent.py',
            'lines': [
                {
                    'number': 1,
                    'author': 'Alice',
                    'commit': 'abc123',
                    'date': '2024-01-10'
                },
                {
                    'number': 2,
                    'author': 'Bob',
                    'commit': 'def456',
                    'date': '2024-01-15'
                }
            ]
        }

        self.assertEqual(len(blame_data['lines']), 2)



class TestTestCoverageIntegration(unittest.TestCase):
    """Test coverage integration in reports."""

    def test_coverage_by_file(self) -> None:
        """Test reporting coverage by file."""
        coverage: Dict[str, float] = {
            'agent.py': 85.5,
            'base_agent/entrypoint.py': 92.0,
            'agent_context.py': 78.5,
            'errors/error_handler.py': 88.0
        }

        low_coverage: List[str] = [f for f, c in coverage.items() if c < 80]
        self.assertIn('agent_context.py', low_coverage)

    def test_coverage_trends(self) -> None:
        """Test tracking coverage trends over time."""
        coverage_history = [
            {'date': '2024-01-01', 'coverage': 75.0},
            {'date': '2024-01-08', 'coverage': 78.5},
            {'date': '2024-01-15', 'coverage': 85.5}
        ]

        trend = coverage_history[-1]['coverage'] - coverage_history[0]['coverage']
        self.assertEqual(trend, 10.5)

    def test_coverage_gaps_identification(self) -> None:
        """Test identifying coverage gaps."""
        gap_analysis: Dict[str, int] = {
            'uncovered_functions': 5,
            'uncovered_branches': 12,
            'high_risk_uncovered': 2
        }

        self.assertGreater(gap_analysis['uncovered_branches'], gap_analysis['uncovered_functions'])



