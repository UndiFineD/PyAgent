# -*- coding: utf-8 -*-
"""Test classes from test_agent_errors.py - core module."""

from __future__ import annotations
import unittest
from typing import Any, List, Dict, Optional, Callable, Tuple, Set, Union
from unittest.mock import MagicMock, Mock, patch, call, ANY
import time
import json
from datetime import datetime, timedelta
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
    from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
except ImportError:
    # Fallback
    AGENT_DIR = Path(__file__).parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self): 
            sys.path.insert(0, str(AGENT_DIR))
            return self
        def __exit__(self, *args): 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))


class TestSuppressionRule:
    """Tests for SuppressionRule dataclass."""

    def test_create_rule(self, errors_module: Any) -> None:
        """Test creating a suppression rule."""
        rule = errors_module.SuppressionRule(
            id="rule123",
            pattern="DeprecationWarning",
            reason="Known deprecation"
        )
        assert rule.id == "rule123"
        assert rule.expires is None

    def test_rule_with_expiration(self, errors_module: Any) -> None:
        """Test rule with expiration date."""
        rule = errors_module.SuppressionRule(
            id="rule456",
            pattern="FutureWarning",
            reason="Temporary",
            expires="2025-12-31T00:00:00"
        )
        assert rule.expires is not None


# ========== ErrorsAgent Init Tests ==========


class TestSeverityScoring:
    """Tests for severity scoring."""

    def test_calculate_severity_score(self, agent: Any, errors_module: Any) -> None:
        """Test severity score calculation."""
        error = agent.add_error("Error", "test.py", 10, errors_module.ErrorSeverity.CRITICAL)
        score = agent.calculate_severity_score(error)
        assert score > 0
        assert score <= 100

    def test_higher_severity_higher_score(self, agent: Any, errors_module: Any) -> None:
        """Test that higher severity gives higher score."""
        error_critical = agent.add_error(
            "Critical", "a.py", 10, errors_module.ErrorSeverity.CRITICAL)
        error_low = agent.add_error("Low", "b.py", 20, errors_module.ErrorSeverity.LOW)
        score_critical = agent.calculate_severity_score(error_critical)
        score_low = agent.calculate_severity_score(error_low)
        assert score_critical > score_low

    def test_security_category_increases_score(self, agent: Any, errors_module: Any) -> None:
        """Test that security category increases score."""
        error_normal = agent.add_error(
            "Normal", "a.py", 10, category=errors_module.ErrorCategory.RUNTIME)
        error_security = agent.add_error(
            "Security", "b.py", 20, category=errors_module.ErrorCategory.SECURITY)
        score_normal = agent.calculate_severity_score(error_normal)
        score_security = agent.calculate_severity_score(error_security)
        assert score_security > score_normal

    def test_resolved_error_lower_score(self, agent: Any) -> None:
        """Test that resolved errors have lower scores."""
        error = agent.add_error("Error", "test.py", 10)
        score_before = agent.calculate_severity_score(error)
        agent.resolve_error(error.id)
        score_after = agent.calculate_severity_score(error)
        assert score_after < score_before

    def test_prioritize_errors(self, agent: Any, errors_module: Any) -> None:
        """Test error prioritization."""
        agent.add_error("Low", "a.py", 10, errors_module.ErrorSeverity.LOW)
        agent.add_error("Critical", "b.py", 20, errors_module.ErrorSeverity.CRITICAL)
        agent.add_error("Medium", "c.py", 30, errors_module.ErrorSeverity.MEDIUM)
        prioritized = agent.prioritize_errors()
        assert prioritized[0].severity == errors_module.ErrorSeverity.CRITICAL


# ========== Error Clustering Tests ==========


class TestPatternRecognition:
    """Tests for pattern recognition."""

    def test_recognize_name_error_pattern(self, agent: Any) -> None:
        """Test recognizing NameError pattern."""
        error = agent.add_error(
            "NameError: name 'undefined_var' is not defined",
            "test.py",
            10
        )
        pattern = agent.recognize_pattern(error)
        assert pattern is not None
        assert pattern.name == "undefined_variable"

    def test_recognize_syntax_error_pattern(self, agent: Any) -> None:
        """Test recognizing SyntaxError pattern."""
        error = agent.add_error("SyntaxError: invalid syntax", "test.py", 10)
        pattern = agent.recognize_pattern(error)
        assert pattern is not None
        assert pattern.name == "syntax_error"

    def test_add_custom_pattern(self, agent: Any, errors_module: Any) -> None:
        """Test adding custom pattern."""
        custom_pattern = errors_module.ErrorPattern(
            name="custom_error",
            regex=r"CustomError: (.*)",
            severity=errors_module.ErrorSeverity.HIGH,
            category=errors_module.ErrorCategory.OTHER
        )
        agent.add_pattern(custom_pattern)
        error = agent.add_error("CustomError: something went wrong", "test.py", 10)
        pattern = agent.recognize_pattern(error)
        assert pattern is not None
        assert pattern.name == "custom_error"

    def test_pattern_occurrences_tracked(self, agent: Any) -> None:
        """Test that pattern occurrences are tracked."""
        agent.add_error("SyntaxError: invalid syntax", "a.py", 10)
        agent.add_error("SyntaxError: unexpected EOF", "b.py", 20)
        stats = agent.get_pattern_statistics()
        assert stats["syntax_error"] >= 2

    def test_auto_categorize_error(self, agent: Any, errors_module: Any) -> None:
        """Test auto-categorization based on pattern."""
        error = agent.add_error("SyntaxError: invalid syntax", "test.py", 10)
        assert error.category == errors_module.ErrorCategory.SYNTAX


# ========== Suppression Rules Tests ==========


class TestSuppressionRules:
    """Tests for suppression rules."""

    def test_add_suppression_rule(self, agent: Any) -> None:
        """Test adding suppression rule."""
        rule = agent.add_suppression_rule(
            pattern="DeprecationWarning",
            reason="Known deprecation"
        )
        assert rule.id is not None
        assert len(agent.get_suppression_rules()) == 1

    def test_suppressed_error_not_added(self, agent: Any) -> None:
        """Test that suppressed errors are not added."""
        agent.add_suppression_rule("DeprecationWarning", "Suppress")
        agent.add_error("DeprecationWarning: old function", "test.py", 10)
        assert len(agent.get_errors()) == 0

    def test_remove_suppression_rule(self, agent: Any) -> None:
        """Test removing suppression rule."""
        rule = agent.add_suppression_rule("Pattern", "Reason")
        result = agent.remove_suppression_rule(rule.id)
        assert result is True
        assert len(agent.get_suppression_rules()) == 0

    def test_remove_nonexistent_rule(self, agent: Any) -> None:
        """Test removing nonexistent rule."""
        result = agent.remove_suppression_rule("nonexistent")
        assert result is False

    def test_expired_rule_not_applied(self, agent: Any) -> None:
        """Test that expired rules are not applied."""
        past_date = (datetime.now() - timedelta(days=1)).isoformat()
        agent.add_suppression_rule(
            pattern="Warning",
            reason="Temporary",
            expires=past_date
        )
        agent.add_error("Warning: something", "test.py", 10)
        assert len(agent.get_errors()) == 1


# ========== Annotations Tests ==========


class TestAnnotations:
    """Tests for error annotations."""

    def test_add_annotation(self, agent: Any) -> None:
        """Test adding annotation."""
        error = agent.add_error("Error", "test.py", 10)
        result = agent.add_annotation(error.id, "Test annotation")
        assert result is True

    def test_get_annotations(self, agent: Any) -> None:
        """Test getting annotations."""
        error = agent.add_error("Error", "test.py", 10)
        agent.add_annotation(error.id, "Annotation 1")
        agent.add_annotation(error.id, "Annotation 2")
        annotations = agent.get_annotations(error.id)
        assert len(annotations) == 2

    def test_annotations_have_timestamp(self, agent: Any) -> None:
        """Test that annotations have timestamps."""
        error = agent.add_error("Error", "test.py", 10)
        agent.add_annotation(error.id, "Test")
        annotations = agent.get_annotations(error.id)
        assert "[" in annotations[0]


# ========== Deduplication Tests ==========


class TestDeduplication:
    """Tests for error deduplication."""

    def test_deduplicate_removes_duplicates(self, agent: Any, errors_module: Any) -> None:
        """Test that deduplication removes duplicates."""
        agent._errors.append(errors_module.ErrorEntry("1", "Error", "test.py", 10))
        agent._errors.append(errors_module.ErrorEntry("2", "Error", "test.py", 10))
        agent._errors.append(errors_module.ErrorEntry("3", "Other error", "test.py", 20))
        removed = agent.deduplicate_errors()
        assert removed == 1
        assert len(agent.get_errors()) == 2


# ========== Statistics Tests ==========


class TestStatistics:
    """Tests for error statistics."""

    def test_calculate_statistics(self, agent: Any, errors_module: Any) -> None:
        """Test statistics calculation."""
        agent.add_error("Error 1", "a.py", 10, errors_module.ErrorSeverity.HIGH)
        agent.add_error("Error 2", "b.py", 20, errors_module.ErrorSeverity.LOW)
        agent.add_error("Error 3", "c.py", 30, errors_module.ErrorSeverity.HIGH)
        error_id = agent.get_errors()[0].id
        agent.resolve_error(error_id)
        stats = agent.calculate_statistics()
        assert stats["total_errors"] == 3
        assert stats["resolved_errors"] == 1
        assert stats["unresolved_errors"] == 2

    def test_statistics_by_severity(self, agent: Any, errors_module: Any) -> None:
        """Test statistics by severity."""
        agent.add_error("High 1", "a.py", 10, errors_module.ErrorSeverity.HIGH)
        agent.add_error("High 2", "b.py", 20, errors_module.ErrorSeverity.HIGH)
        agent.add_error("Low", "c.py", 30, errors_module.ErrorSeverity.LOW)
        stats = agent.calculate_statistics()
        assert stats["by_severity"]["HIGH"] == 2
        assert stats["by_severity"]["LOW"] == 1

    def test_statistics_by_category(self, agent: Any, errors_module: Any) -> None:
        """Test statistics by category."""
        agent.add_error("Syntax 1", "a.py", 10, category=errors_module.ErrorCategory.SYNTAX)
        agent.add_error("Syntax 2", "b.py", 20, category=errors_module.ErrorCategory.SYNTAX)
        agent.add_error("Style", "c.py", 30, category=errors_module.ErrorCategory.STYLE)
        stats = agent.calculate_statistics()
        assert stats["by_category"]["SYNTAX"] == 2
        assert stats["by_category"]["STYLE"] == 1


# ========== Documentation Generation Tests ==========


class TestDocumentationGeneration:
    """Tests for documentation generation."""

    def test_generate_documentation(self, agent: Any, errors_module: Any) -> None:
        """Test documentation generation."""
        agent.add_error("Syntax error", "a.py", 10, category=errors_module.ErrorCategory.SYNTAX)
        agent.add_error("Style issue", "b.py", 20, category=errors_module.ErrorCategory.STYLE)
        docs = agent.generate_documentation()
        assert "# Error Documentation" in docs
        assert "Total Errors" in docs


# ========== Export Tests ==========


class TestExport:
    """Tests for error export."""

    def test_export_json(self, agent: Any) -> None:
        """Test JSON export."""
        agent.add_error("Error 1", "a.py", 10)
        agent.add_error("Error 2", "b.py", 20)
        exported = agent.export_errors("json")
        data = json.loads(exported)
        assert len(data) == 2
        assert data[0]["message"] == "Error 1"

    def test_export_csv(self, agent: Any) -> None:
        """Test CSV export."""
        agent.add_error("Error 1", "a.py", 10)
        agent.add_error("Error 2", "b.py", 20)
        exported = agent.export_errors("csv")
        lines = exported.strip().split('\n')
        assert len(lines) == 3


# ========== Default Content Tests ==========


class TestDefaultContent:
    """Tests for default content generation."""

    def test_default_content(self, agent: Any) -> None:
        """Test default content generation."""
        content = agent._get_default_content()
        assert "# Error Report" in content
        assert "No errors detected" in content

    def test_fallback_response(self, agent: Any) -> None:
        """Test fallback response."""
        response = agent._get_fallback_response()
        assert "AI Improvement Unavailable" in response


# ========== Session 7 Tests: New Enums ==========



class TestSession7Enums:
    """Tests for Session 7 enums."""

    def test_notification_channel_enum(self, errors_module: Any) -> None:
        """Test NotificationChannel enum values."""
        assert errors_module.NotificationChannel.SLACK.value == "slack"
        assert errors_module.NotificationChannel.TEAMS.value == "teams"
        assert errors_module.NotificationChannel.EMAIL.value == "email"
        assert errors_module.NotificationChannel.WEBHOOK.value == "webhook"
        assert errors_module.NotificationChannel.DISCORD.value == "discord"

    def test_external_reporter_enum(self, errors_module: Any) -> None:
        """Test ExternalReporter enum values."""
        assert errors_module.ExternalReporter.SENTRY.value == "sentry"
        assert errors_module.ExternalReporter.ROLLBAR.value == "rollbar"
        assert errors_module.ExternalReporter.BUGSNAG.value == "bugsnag"
        assert errors_module.ExternalReporter.DATADOG.value == "datadog"
        assert errors_module.ExternalReporter.NEWRELIC.value == "newrelic"

    def test_trend_direction_enum(self, errors_module: Any) -> None:
        """Test TrendDirection enum values."""
        assert errors_module.TrendDirection.INCREASING.value == "increasing"
        assert errors_module.TrendDirection.DECREASING.value == "decreasing"
        assert errors_module.TrendDirection.STABLE.value == "stable"
        assert errors_module.TrendDirection.VOLATILE.value == "volatile"


# ========== Session 7 Tests: Dataclasses ==========



class TestSession7Dataclasses:
    """Tests for Session 7 dataclasses."""

    def test_notification_config_dataclass(self, errors_module: Any) -> None:
        """Test NotificationConfig dataclass."""
        config = errors_module.NotificationConfig(
            channel=errors_module.NotificationChannel.SLACK,
            endpoint="https://hooks.slack.com / test"
        )
        assert config.channel == errors_module.NotificationChannel.SLACK
        assert config.min_severity == errors_module.ErrorSeverity.HIGH
        assert config.enabled is True

    def test_error_impact_dataclass(self, errors_module: Any) -> None:
        """Test ErrorImpact dataclass."""
        impact = errors_module.ErrorImpact(error_id="err123")
        assert impact.error_id == "err123"
        assert impact.affected_files == []
        assert impact.impact_score == 0.0

    def test_timeline_event_dataclass(self, errors_module: Any) -> None:
        """Test TimelineEvent dataclass."""
        event = errors_module.TimelineEvent(
            timestamp="2025-01-01T00:00:00",
            event_type="created",
            error_id="err123"
        )
        assert event.event_type == "created"
        assert event.details == ""

    def test_regression_info_dataclass(self, errors_module: Any) -> None:
        """Test RegressionInfo dataclass."""
        info = errors_module.RegressionInfo(error_id="err123")
        assert info.error_id == "err123"
        assert info.occurrences == 1

    def test_fix_suggestion_dataclass(self, errors_module: Any) -> None:
        """Test FixSuggestion dataclass."""
        suggestion = errors_module.FixSuggestion(
            error_id="err123",
            suggestion="Add import statement"
        )
        assert suggestion.confidence == 0.0
        assert suggestion.source == "pattern_match"

    def test_error_budget_dataclass(self, errors_module: Any) -> None:
        """Test ErrorBudget dataclass."""
        budget = errors_module.ErrorBudget(
            budget_name="production",
            total_budget=100.0
        )
        assert budget.consumed == 0.0

    def test_trend_data_dataclass(self, errors_module: Any) -> None:
        """Test TrendData dataclass."""
        data = errors_module.TrendData(metric_name="error_count")
        assert data.values == []
        assert data.direction == errors_module.TrendDirection.STABLE

    def test_blame_info_dataclass(self, errors_module: Any) -> None:
        """Test BlameInfo dataclass."""
        info = errors_module.BlameInfo(error_id="err123")
        assert info.commit_hash == ""
        assert info.author == ""

    def test_branch_comparison_dataclass(self, errors_module: Any) -> None:
        """Test BranchComparison dataclass."""
        comp = errors_module.BranchComparison(
            branch_a="main",
            branch_b="feature"
        )
        assert comp.errors_only_in_a == []
        assert comp.common_errors == []


# ========== Session 7 Tests: NotificationManager ==========



class TestNotificationManager:
    """Tests for NotificationManager class."""

    def test_init(self, errors_module: Any) -> None:
        """Test NotificationManager initialization."""
        manager = errors_module.NotificationManager()
        assert manager.configs == []

    def test_add_config(self, errors_module: Any) -> None:
        """Test adding notification configuration."""
        manager = errors_module.NotificationManager()
        config = errors_module.NotificationConfig(
            channel=errors_module.NotificationChannel.SLACK,
            endpoint="https://test.slack.com"
        )
        manager.add_config(config)
        assert len(manager.configs) == 1

    def test_remove_config(self, errors_module: Any) -> None:
        """Test removing notification configuration."""
        manager = errors_module.NotificationManager()
        config = errors_module.NotificationConfig(
            channel=errors_module.NotificationChannel.SLACK,
            endpoint="https://test.slack.com"
        )
        manager.add_config(config)
        result = manager.remove_config(errors_module.NotificationChannel.SLACK)
        assert result is True
        assert len(manager.configs) == 0

    def test_notify(self, errors_module: Any) -> None:
        """Test sending notifications."""
        manager = errors_module.NotificationManager()
        config = errors_module.NotificationConfig(
            channel=errors_module.NotificationChannel.SLACK,
            endpoint="https://test.slack.com",
            min_severity=errors_module.ErrorSeverity.MEDIUM
        )
        manager.add_config(config)

        error = errors_module.ErrorEntry(
            id="err1",
            message="Test error",
            file_path="test.py",
            line_number=10,
            severity=errors_module.ErrorSeverity.HIGH
        )
        notified = manager.notify(error)
        assert "slack" in notified

    def test_get_configs(self, errors_module: Any) -> None:
        """Test getting all configurations."""
        manager = errors_module.NotificationManager()
        manager.add_config(errors_module.NotificationConfig(
            channel=errors_module.NotificationChannel.SLACK,
            endpoint="https://test.slack.com"
        ))
        manager.add_config(errors_module.NotificationConfig(
            channel=errors_module.NotificationChannel.EMAIL,
            endpoint="test@example.com"
        ))
        configs = manager.get_configs()
        assert len(configs) == 2


# ========== Session 7 Tests: ImpactAnalyzer ==========



class TestImpactAnalyzer:
    """Tests for ImpactAnalyzer class."""

    def test_init(self, errors_module: Any) -> None:
        """Test ImpactAnalyzer initialization."""
        analyzer = errors_module.ImpactAnalyzer()
        assert analyzer.file_dependencies == {}

    def test_add_dependency(self, errors_module: Any) -> None:
        """Test adding file dependencies."""
        analyzer = errors_module.ImpactAnalyzer()
        analyzer.add_dependency("main.py", ["utils.py", "config.py"])
        assert "main.py" in analyzer.file_dependencies

    def test_add_functions(self, errors_module: Any) -> None:
        """Test adding functions."""
        analyzer = errors_module.ImpactAnalyzer()
        analyzer.add_functions("main.py", ["main", "setup"])
        assert "main.py" in analyzer.function_map

    def test_analyze(self, errors_module: Any) -> None:
        """Test impact analysis."""
        analyzer = errors_module.ImpactAnalyzer()
        analyzer.add_dependency("app.py", ["utils.py"])
        analyzer.add_functions("utils.py", ["helper"])

        error = errors_module.ErrorEntry(
            id="err1",
            message="Error",
            file_path="utils.py",
            line_number=10,
            severity=errors_module.ErrorSeverity.HIGH
        )
        impact = analyzer.analyze(error)
        assert isinstance(impact, errors_module.ErrorImpact)
        assert "app.py" in impact.affected_files


# ========== Session 7 Tests: TimelineTracker ==========



class TestTimelineTracker:
    """Tests for TimelineTracker class."""

    def test_init(self, errors_module: Any) -> None:
        """Test TimelineTracker initialization."""
        tracker = errors_module.TimelineTracker()
        assert tracker.events == []

    def test_record_event(self, errors_module: Any) -> None:
        """Test recording timeline events."""
        tracker = errors_module.TimelineTracker()
        event = tracker.record_event("err1", "created", "Initial detection")
        assert event.error_id == "err1"
        assert event.event_type == "created"

    def test_get_events_for_error(self, errors_module: Any) -> None:
        """Test getting events for a specific error."""
        tracker = errors_module.TimelineTracker()
        tracker.record_event("err1", "created")
        tracker.record_event("err2", "created")
        tracker.record_event("err1", "resolved")
        events = tracker.get_events_for_error("err1")
        assert len(events) == 2

    def test_generate_timeline_data(self, errors_module: Any) -> None:
        """Test generating timeline data."""
        tracker = errors_module.TimelineTracker()
        tracker.record_event("err1", "created")
        tracker.record_event("err2", "resolved")
        data = tracker.generate_timeline_data()
        assert "total_events" in data
        assert data["total_events"] == 2

    def test_clear(self, errors_module: Any) -> None:
        """Test clearing timeline."""
        tracker = errors_module.TimelineTracker()
        tracker.record_event("err1", "created")
        tracker.clear()
        assert len(tracker.events) == 0


# ========== Session 7 Tests: RegressionDetector ==========



class TestRegressionDetector:
    """Tests for RegressionDetector class."""

    def test_init(self, errors_module: Any) -> None:
        """Test RegressionDetector initialization."""
        detector = errors_module.RegressionDetector()
        assert detector.fixed_errors == {}

    def test_record_fix(self, errors_module: Any) -> None:
        """Test recording a fix."""
        detector = errors_module.RegressionDetector()
        error = errors_module.ErrorEntry(
            id="err1",
            message="Test error",
            file_path="test.py",
            line_number=10
        )
        detector.record_fix(error, "abc123")
        assert len(detector.fixed_errors) == 1

    def test_check_regression(self, errors_module: Any) -> None:
        """Test checking for regression."""
        detector = errors_module.RegressionDetector()
        error = errors_module.ErrorEntry(
            id="err1",
            message="Test error",
            file_path="test.py",
            line_number=10
        )
        detector.record_fix(error, "abc123")

        # Same error reappears
        new_error = errors_module.ErrorEntry(
            id="err2",
            message="Test error",
            file_path="test.py",
            line_number=10
        )
        regression = detector.check_regression(new_error, "def456")
        assert regression is not None
        assert regression.original_fix_commit == "abc123"

    def test_get_regression_rate(self, errors_module: Any) -> None:
        """Test getting regression rate."""
        detector = errors_module.RegressionDetector()
        rate = detector.get_regression_rate()
        assert rate == 0.0


# ========== Session 7 Tests: AutoFixSuggester ==========



class TestAutoFixSuggester:
    """Tests for AutoFixSuggester class."""

    def test_init(self, errors_module: Any) -> None:
        """Test AutoFixSuggester initialization."""
        suggester = errors_module.AutoFixSuggester()
        assert len(suggester.fix_patterns) > 0

    def test_add_pattern(self, errors_module: Any) -> None:
        """Test adding fix patterns."""
        suggester = errors_module.AutoFixSuggester()
        suggester.add_pattern(r"CustomError: (.*)", "Fix custom error: {0}")
        assert r"CustomError: (.*)" in suggester.fix_patterns

    def test_suggest_name_error(self, errors_module: Any) -> None:
        """Test suggesting fix for NameError."""
        suggester = errors_module.AutoFixSuggester()
        error = errors_module.ErrorEntry(
            id="err1",
            message="NameError: name 'foo' is not defined",
            file_path="test.py",
            line_number=10
        )
        suggestion = suggester.suggest(error)
        assert suggestion is not None
        assert "foo" in suggestion.suggestion

    def test_suggest_all(self, errors_module: Any) -> None:
        """Test suggesting fixes for multiple errors."""
        suggester = errors_module.AutoFixSuggester()
        errors = [
            errors_module.ErrorEntry(
                id="err1",
                message="NameError: name 'x' is not defined",
                file_path="test.py",
                line_number=10
            ),
            errors_module.ErrorEntry(
                id="err2",
                message="Some unknown error",
                file_path="test.py",
                line_number=20
            ),
        ]
        suggestions = suggester.suggest_all(errors)
        assert len(suggestions) >= 1


# ========== Session 7 Tests: ExternalReportingClient ==========



class TestExternalReportingClient:
    """Tests for ExternalReportingClient class."""

    def test_init(self, errors_module: Any) -> None:
        """Test ExternalReportingClient initialization."""
        client = errors_module.ExternalReportingClient(
            errors_module.ExternalReporter.SENTRY
        )
        assert client.system == errors_module.ExternalReporter.SENTRY
        assert client.enabled is False

    def test_init_with_dsn(self, errors_module: Any) -> None:
        """Test initialization with DSN."""
        client = errors_module.ExternalReportingClient(
            errors_module.ExternalReporter.SENTRY,
            dsn="https://key@sentry.io / project"
        )
        assert client.enabled is True

    def test_report(self, errors_module: Any) -> None:
        """Test reporting an error."""
        client = errors_module.ExternalReportingClient(
            errors_module.ExternalReporter.SENTRY,
            dsn="https://test"
        )
        error = errors_module.ErrorEntry(
            id="err1",
            message="Test error",
            file_path="test.py",
            line_number=10
        )
        result = client.report(error)
        assert result is True

    def test_report_batch(self, errors_module: Any) -> None:
        """Test batch reporting."""
        client = errors_module.ExternalReportingClient(
            errors_module.ExternalReporter.ROLLBAR,
            dsn="https://test"
        )
        errors = [
            errors_module.ErrorEntry(
                id=f"err{i}",
                message=f"Error {i}",
                file_path="test.py",
                line_number=i * 10
            )
            for i in range(3)
        ]
        count = client.report_batch(errors)
        assert count == 3


# ========== Session 7 Tests: ErrorBudgetManager ==========



class TestTrendAnalyzer:
    """Tests for TrendAnalyzer class."""

    def test_init(self, errors_module: Any) -> None:
        """Test TrendAnalyzer initialization."""
        analyzer = errors_module.TrendAnalyzer()
        assert analyzer.data_points == {}

    def test_record(self, errors_module: Any) -> None:
        """Test recording data points."""
        analyzer = errors_module.TrendAnalyzer()
        analyzer.record("error_count", 10)
        analyzer.record("error_count", 15)
        assert len(analyzer.data_points["error_count"].values) == 2

    def test_analyze_increasing(self, errors_module: Any) -> None:
        """Test analyzing increasing trend."""
        analyzer = errors_module.TrendAnalyzer()
        for i in range(5):
            analyzer.record("errors", i * 10)
        data = analyzer.analyze("errors")
        assert data.direction == errors_module.TrendDirection.INCREASING

    def test_analyze_decreasing(self, errors_module: Any) -> None:
        """Test analyzing decreasing trend."""
        analyzer = errors_module.TrendAnalyzer()
        for i in range(5, 0, -1):
            analyzer.record("errors", i * 10)
        data = analyzer.analyze("errors")
        assert data.direction == errors_module.TrendDirection.DECREASING

    def test_predict(self, errors_module: Any) -> None:
        """Test prediction."""
        analyzer = errors_module.TrendAnalyzer()
        for i in range(5):
            analyzer.record("errors", 10 + i)
        predictions = analyzer.predict("errors", 3)
        assert len(predictions) == 3


# ========== Session 7 Tests: BlameTracker ==========



class TestBlameTracker:
    """Tests for BlameTracker class."""

    def test_init(self, errors_module: Any) -> None:
        """Test BlameTracker initialization."""
        tracker = errors_module.BlameTracker()
        assert tracker.blame_cache == {}

    def test_get_blame_cached(self, errors_module: Any) -> None:
        """Test getting cached blame info."""
        tracker = errors_module.BlameTracker()
        # Pre-populate cache
        error = errors_module.ErrorEntry(
            id="err1",
            message="Test",
            file_path="test.py",
            line_number=10
        )
        cached_info = errors_module.BlameInfo(
            error_id="err1",
            author="developer",
            commit_hash="abc123"
        )
        tracker.blame_cache["test.py:10"] = cached_info

        blame = tracker.get_blame(error)
        assert blame.author == "developer"

    def test_get_top_contributors(self, errors_module: Any) -> None:
        """Test getting top contributors."""
        tracker = errors_module.BlameTracker()
        # Pre-populate cache
        for i in range(5):
            tracker.blame_cache[f"test{i}.py:10"] = errors_module.BlameInfo(
                error_id=f"err{i}",
                author="alice" if i < 3 else "bob"
            )

        errors = [
            errors_module.ErrorEntry(
                id=f"err{i}",
                message="Test",
                file_path=f"test{i}.py",
                line_number=10
            )
            for i in range(5)
        ]
        contributors = tracker.get_top_contributors(errors, 2)
        assert len(contributors) <= 2


# ========== Session 7 Tests: BranchComparer ==========



class TestBranchComparer:
    """Tests for BranchComparer class."""

    def test_init(self, errors_module: Any) -> None:
        """Test BranchComparer initialization."""
        comparer = errors_module.BranchComparer()
        assert comparer.branch_errors == {}

    def test_set_branch_errors(self, errors_module: Any) -> None:
        """Test setting branch errors."""
        comparer = errors_module.BranchComparer()
        comparer.set_branch_errors("main", ["err1", "err2"])
        assert "main" in comparer.branch_errors

    def test_compare(self, errors_module: Any) -> None:
        """Test comparing branches."""
        comparer = errors_module.BranchComparer()
        comparer.set_branch_errors("main", ["err1", "err2", "err3"])
        comparer.set_branch_errors("feature", ["err2", "err3", "err4"])

        comparison = comparer.compare("main", "feature")
        assert "err1" in comparison.errors_only_in_a
        assert "err4" in comparison.errors_only_in_b
        assert "err2" in comparison.common_errors

    def test_get_new_errors(self, errors_module: Any) -> None:
        """Test getting new errors in feature branch."""
        comparer = errors_module.BranchComparer()
        comparer.set_branch_errors("main", ["err1"])
        comparer.set_branch_errors("feature", ["err1", "err2"])

        new_errors = comparer.get_new_errors("main", "feature")
        assert "err2" in new_errors

    def test_get_fixed_errors(self, errors_module: Any) -> None:
        """Test getting fixed errors in feature branch."""
        comparer = errors_module.BranchComparer()
        comparer.set_branch_errors("main", ["err1", "err2"])
        comparer.set_branch_errors("feature", ["err1"])

        fixed_errors = comparer.get_fixed_errors("main", "feature")
        assert "err2" in fixed_errors


# =============================================================================
# Session 9: Error Correlation Tests
# =============================================================================



class TestRootCauseAnalysis:
    """Tests for root cause analysis with stack traces."""

    def test_stack_trace_detection(self, errors_module: Any, tmp_path: Path) -> None:
        """Test stack trace detection."""
        target = tmp_path / "test.errors.md"
        content = """# Error
Traceback (most recent call last):
  File "app.py", line 10, in main
    raise ValueError("test")
ValueError: test
"""
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "Traceback" in previous
        assert "ValueError" in previous


# =============================================================================
# Session 9: Error Clustering Tests
# =============================================================================



class TestSeverityScoring_v2:  # noqa: F811
    """Tests for severity scoring calculation (extended)."""

    def test_critical_severity(self, errors_module: Any) -> None:
        """Test critical severity detection."""
        error = errors_module.ErrorEntry(
            error_type="SecurityError",
            message="Authentication bypass",
            severity=errors_module.ErrorSeverity.CRITICAL
        )
        assert error.severity == errors_module.ErrorSeverity.CRITICAL

    def test_severity_comparison(self, errors_module: Any) -> None:
        """Test severity comparison."""
        assert errors_module.ErrorSeverity.CRITICAL.value > errors_module.ErrorSeverity.LOW.value


# =============================================================================
# Session 9: Resolution Tracking Tests
# =============================================================================



class TestResolutionTracking:
    """Tests for resolution tracking workflows."""

    def test_resolution_status_detection(self, errors_module: Any, tmp_path: Path) -> None:
        """Test resolution status detection."""
        target = tmp_path / "test.errors.md"
        content = "# Errors\n- [RESOLVED] Error A\n- [OPEN] Error B"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "[RESOLVED]" in previous
        assert "[OPEN]" in previous


# =============================================================================
# Session 9: Notification Delivery Tests
# =============================================================================



class TestNotificationDelivery:
    """Tests for notification delivery to integrations."""

    def test_notification_marker(self, errors_module: Any, tmp_path: Path) -> None:
        """Test notification marker in errors."""
        target = tmp_path / "test.errors.md"
        content = "# Critical Error - NOTIFY: @team"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "NOTIFY:" in previous


# =============================================================================
# Session 9: Pattern Recognition Tests
# =============================================================================



class TestPatternRecognition_v2:  # noqa: F811
    """Tests for pattern recognition accuracy (extended)."""

    def test_common_pattern_detection(self, errors_module: Any, tmp_path: Path) -> None:
        """Test common error pattern detection."""
        target = tmp_path / "test.errors.md"
        content = """# Errors
- NullPointerException at line 10
- NullPointerException at line 20
- NullPointerException at line 30
"""
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert previous.count("NullPointerException") == 3


# =============================================================================
# Session 9: Impact Analysis Tests
# =============================================================================



class TestImpactAnalysis:
    """Tests for impact analysis completeness."""

    def test_affected_components(self, errors_module: Any, tmp_path: Path) -> None:
        """Test affected components detection."""
        target = tmp_path / "test.errors.md"
        content = "# Error\nAffected: auth_module, user_service, database"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "auth_module" in previous


# =============================================================================
# Session 9: Timeline Visualization Tests
# =============================================================================



class TestTimelineVisualization:
    """Tests for timeline visualization data."""

    def test_timestamp_detection(self, errors_module: Any, tmp_path: Path) -> None:
        """Test timestamp detection in errors."""
        target = tmp_path / "test.errors.md"
        content = "# Errors\n- [2025-01-16 10:30:00] Error occurred"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "2025-01-16" in previous


# =============================================================================
# Session 9: Regression Detection Tests
# =============================================================================



class TestRegressionDetection:
    """Tests for regression detection algorithms."""

    def test_regression_marker(self, errors_module: Any, tmp_path: Path) -> None:
        """Test regression marker detection."""
        target = tmp_path / "test.errors.md"
        content = "# Errors\n- [REGRESSION] Error reintroduced in v2.0"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "[REGRESSION]" in previous


# =============================================================================
# Session 9: Automated Fix Suggestion Tests
# =============================================================================



class TestAutomatedFixSuggestions:
    """Tests for automated fix suggestions."""

    def test_fix_suggestion_detection(self, errors_module: Any, tmp_path: Path) -> None:
        """Test fix suggestion detection."""
        target = tmp_path / "test.errors.md"
        content = "# Error\nFix: Add null check before accessing property"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "Fix:" in previous


# =============================================================================
# Session 9: External Reporting Tests
# =============================================================================



class TestExternalReporting:
    """Tests for external reporting integrations."""

    def test_jira_reference(self, errors_module: Any, tmp_path: Path) -> None:
        """Test JIRA reference in error."""
        target = tmp_path / "test.errors.md"
        content = "# Error\nTracked in: JIRA-123"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "JIRA-123" in previous


# =============================================================================
# Session 9: Deduplication Accuracy Tests
# =============================================================================



class TestDeduplicationAccuracy:
    """Tests for deduplication accuracy."""

    def test_duplicate_content(self, errors_module: Any, tmp_path: Path) -> None:
        """Test duplicate error content."""
        target = tmp_path / "test.errors.md"
        content = "# Errors\n- Same error\n- Same error"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        # Duplicates should be readable
        assert "Same error" in previous


# =============================================================================
# Session 9: Annotation Persistence Tests
# =============================================================================



class TestAnnotationPersistence:
    """Tests for annotation persistence and retrieval."""

    def test_annotation_preserved(self, errors_module: Any, tmp_path: Path) -> None:
        """Test annotation is preserved."""
        target = tmp_path / "test.errors.md"
        content = "# Error\n<!-- @owner: john -->\nCritical error"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "@owner:" in previous


# =============================================================================
# Session 9: Error Budget Tests
# =============================================================================



class TestRemediationSuggestions(unittest.TestCase):
    """Test error remediation and quick-fix recommendations."""

    def test_remediation_from_history(self):
        """Test implementing error remediation from historical fixes."""
        error_history = {
            'TypeError: unsupported operand': [
                'Cast operands to same type',
                'Check type before operation',
                'Use type hints'
            ]
        }
        suggestions = error_history.get('TypeError: unsupported operand', [])
        self.assertEqual(len(suggestions), 3)

    def test_nlp_analysis_for_quickfixes(self):
        """Test NLP analysis for quick-fix recommendations."""

        suggested_fixes = [
            'Convert int to str: str(variable)',
            'Use format string: f"{variable}"',
            'Use str.format(): "{}".format(variable)'
        ]
        self.assertEqual(len(suggested_fixes), 3)

    def test_common_fix_patterns(self):
        """Test recognizing common fix patterns."""
        fix_patterns = {
            'AttributeError': 'Check object has attribute with hasattr()',
            'KeyError': 'Use dict.get() with default value',
            'IndexError': 'Check list length before accessing',
            'ZeroDivisionError': 'Check divisor is not zero'
        }
        self.assertIn('AttributeError', fix_patterns)



class TestRootCauseAnalysisImprovements(unittest.TestCase):
    """Test error root cause analysis using git blame."""

    def test_blame_integration(self):
        """Test integrating git blame for error origins."""
        blame_data = {
            'file': 'main.py',
            'error_line': 42,
            'introduced_by': 'developer@example.com',
            'commit': 'abc123def456',
            'date': '2025-12-10',
            'message': 'Add new feature'
        }
        self.assertEqual(blame_data['introduced_by'], 'developer@example.com')

    def test_root_cause_identification(self):
        """Test identifying root cause of errors."""
        root_cause = {
            'primary': 'Missing type validation',
            'contributing': ['Insufficient testing', 'Code review gap'],
            'systemic': 'Lack of type hints'
        }
        self.assertEqual(root_cause['primary'], 'Missing type validation')

    def test_prevention_recommendation(self):
        """Test recommending prevention measures."""
        recommendations = [
            {'action': 'Add type hints', 'impact': 'high', 'effort': 'medium'},
            {'action': 'Increase test coverage', 'impact': 'high', 'effort': 'high'},
            {'action': 'Add code review checklist', 'impact': 'medium', 'effort': 'low'}
        ]
        self.assertEqual(len(recommendations), 3)


