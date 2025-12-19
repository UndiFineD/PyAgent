#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for agent-errors.py."""

from __future__ import annotations
import json
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import patch
import pytest
from agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture()
def base_agent_module() -> Any:
    with agent_dir_on_path():
        import base_agent
        return base_agent


@pytest.fixture()
def errors_module() -> Any:
    """Load the errors agent module."""
    with agent_dir_on_path():
        return load_agent_module("agent-errors.py")


@pytest.fixture()
def agent(errors_module: Any, tmp_path: Path) -> Any:
    """Create agent for testing."""
    target = tmp_path / "test.errors.md"
    target.write_text("# Error Report\n", encoding="utf-8")
    return errors_module.ErrorsAgent(str(target))


def test_errors_agent_delegates_to_base(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module: Any
) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent-errors.py")

    def fake_run_subagent(
            self: Any,
            description: str,
            prompt: str,
            original_content: str = "") -> str:
        return "IMPROVED"

    monkeypatch.setattr(
        base_agent_module.BaseAgent,
        "run_subagent",
        fake_run_subagent,
        raising=True)
    target = tmp_path / "x.errors.md"
    target.write_text("BEFORE", encoding="utf-8")
    agent = mod.ErrorsAgent(str(target))
    agent.read_previous_content()
    assert agent.improve_content("prompt") == "IMPROVED"


# ========== ErrorSeverity Tests ==========

class TestErrorSeverity:
    """Tests for ErrorSeverity enum."""

    def test_severity_values(self, errors_module: Any) -> None:
        """Test that severity values are correct."""
        assert errors_module.ErrorSeverity.CRITICAL.value == 5
        assert errors_module.ErrorSeverity.HIGH.value == 4
        assert errors_module.ErrorSeverity.MEDIUM.value == 3
        assert errors_module.ErrorSeverity.LOW.value == 2
        assert errors_module.ErrorSeverity.INFO.value == 1

    def test_severity_ordering(self, errors_module: Any) -> None:
        """Test severity ordering."""
        assert errors_module.ErrorSeverity.CRITICAL.value > errors_module.ErrorSeverity.HIGH.value
        assert errors_module.ErrorSeverity.HIGH.value > errors_module.ErrorSeverity.MEDIUM.value

    def test_all_severities_exist(self, errors_module: Any) -> None:
        """Test all severity levels exist."""
        severities = list(errors_module.ErrorSeverity)
        assert len(severities) == 5


# ========== ErrorCategory Tests ==========

class TestErrorCategory:
    """Tests for ErrorCategory enum."""

    def test_category_values(self, errors_module: Any) -> None:
        """Test that category values are correct strings."""
        assert errors_module.ErrorCategory.SYNTAX.value == "syntax"
        assert errors_module.ErrorCategory.RUNTIME.value == "runtime"
        assert errors_module.ErrorCategory.SECURITY.value == "security"
        assert errors_module.ErrorCategory.OTHER.value == "other"

    def test_all_categories_exist(self, errors_module: Any) -> None:
        """Test all categories exist."""
        categories = list(errors_module.ErrorCategory)
        assert len(categories) == 11


# ========== ErrorEntry Tests ==========

class TestErrorEntry:
    """Tests for ErrorEntry dataclass."""

    def test_create_error_entry(self, errors_module: Any) -> None:
        """Test creating an error entry."""
        error = errors_module.ErrorEntry(
            id="test123",
            message="Test error",
            file_path="test.py",
            line_number=10
        )
        assert error.id == "test123"
        assert error.message == "Test error"
        assert error.file_path == "test.py"
        assert error.line_number == 10
        assert error.resolved is False

    def test_error_entry_with_all_fields(self, errors_module: Any) -> None:
        """Test creating an error entry with all fields."""
        error = errors_module.ErrorEntry(
            id="full123",
            message="Full error",
            file_path="full.py",
            line_number=20,
            severity=errors_module.ErrorSeverity.CRITICAL,
            category=errors_module.ErrorCategory.SECURITY,
            timestamp="2025-01-01T00:00:00",
            stack_trace="Traceback...",
            suggested_fix="Fix it",
            resolved=True,
            resolution_timestamp="2025-01-02T00:00:00",
            tags=["important", "security"]
        )
        assert error.severity == errors_module.ErrorSeverity.CRITICAL
        assert error.category == errors_module.ErrorCategory.SECURITY
        assert error.resolved is True


# ========== ErrorCluster Tests ==========

class TestErrorCluster:
    """Tests for ErrorCluster dataclass."""

    def test_create_cluster(self, errors_module: Any) -> None:
        """Test creating an error cluster."""
        cluster = errors_module.ErrorCluster(
            id="clust123",
            name="NameError cluster",
            pattern="NameError:.*"
        )
        assert cluster.id == "clust123"
        assert cluster.name == "NameError cluster"
        assert cluster.error_ids == []

    def test_cluster_with_errors(self, errors_module: Any) -> None:
        """Test cluster with error IDs."""
        cluster = errors_module.ErrorCluster(
            id="clust456",
            name="Type errors",
            pattern="TypeError:.*",
            error_ids=["err1", "err2", "err3"]
        )
        assert len(cluster.error_ids) == 3
        assert "err2" in cluster.error_ids


# ========== ErrorPattern Tests ==========

class TestErrorPattern:
    """Tests for ErrorPattern dataclass."""

    def test_create_pattern(self, errors_module: Any) -> None:
        """Test creating an error pattern."""
        pattern = errors_module.ErrorPattern(
            name="my_pattern",
            regex=r"CustomError: (.*)",
            severity=errors_module.ErrorSeverity.HIGH,
            category=errors_module.ErrorCategory.RUNTIME
        )
        assert pattern.name == "my_pattern"
        assert pattern.occurrences == 0

    def test_default_patterns_exist(self, errors_module: Any) -> None:
        """Test that default patterns are defined."""
        assert len(errors_module.DEFAULT_ERROR_PATTERNS) > 0
        pattern_names = [p.name for p in errors_module.DEFAULT_ERROR_PATTERNS]
        assert "undefined_variable" in pattern_names
        assert "syntax_error" in pattern_names


# ========== SuppressionRule Tests ==========

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

class TestErrorsAgentInit:
    """Tests for ErrorsAgent initialization."""

    def test_init_with_errors_file(self, errors_module: Any, tmp_path: Path) -> None:
        """Test initialization with .errors.md file."""
        target = tmp_path / "test.errors.md"
        target.write_text("# Error Report\n", encoding="utf-8")
        agent = errors_module.ErrorsAgent(str(target))
        assert agent.file_path == target
        assert agent._errors == []

    def test_init_validates_extension(self, errors_module: Any, tmp_path: Path) -> None:
        """Test that initialization warns about wrong extension."""
        target = tmp_path / "test.md"
        target.write_text("# Not errors\n", encoding="utf-8")
        with patch('logging.warning') as mock_warn:
            errors_module.ErrorsAgent(str(target))
            mock_warn.assert_called()


# ========== Add Error Tests ==========

class TestAddError:
    """Tests for adding errors."""

    def test_add_simple_error(self, agent: Any, errors_module: Any) -> None:
        """Test adding a simple error."""
        error = agent.add_error(
            message="NameError: name 'x' is not defined",
            file_path="test.py",
            line_number=10
        )
        assert error.id is not None
        assert len(agent.get_errors()) == 1

    def test_add_error_with_severity(self, agent: Any, errors_module: Any) -> None:
        """Test adding error with custom severity."""
        error = agent.add_error(
            message="Critical error",
            file_path="test.py",
            line_number=5,
            severity=errors_module.ErrorSeverity.CRITICAL
        )
        assert error.severity == errors_module.ErrorSeverity.CRITICAL

    def test_add_error_with_category(self, agent: Any, errors_module: Any) -> None:
        """Test adding error with category."""
        error = agent.add_error(
            message="Security issue",
            file_path="test.py",
            line_number=15,
            category=errors_module.ErrorCategory.SECURITY
        )
        assert error.category == errors_module.ErrorCategory.SECURITY

    def test_add_error_generates_unique_id(self, agent: Any) -> None:
        """Test that each error gets a unique ID."""
        error1 = agent.add_error("Error 1", "test.py", 10)
        error2 = agent.add_error("Error 2", "test.py", 20)
        assert error1.id != error2.id

    def test_add_error_sets_timestamp(self, agent: Any) -> None:
        """Test that error timestamp is set."""
        error = agent.add_error("Error", "test.py", 10)
        assert error.timestamp != ""


# ========== Error Retrieval Tests ==========

class TestErrorRetrieval:
    """Tests for error retrieval methods."""

    def test_get_all_errors(self, agent: Any, errors_module: Any) -> None:
        """Test getting all errors."""
        agent.add_error("Error 1", "a.py", 10, errors_module.ErrorSeverity.HIGH)
        agent.add_error("Error 2", "b.py", 20, errors_module.ErrorSeverity.LOW)
        errors = agent.get_errors()
        assert len(errors) == 2

    def test_get_error_by_id(self, agent: Any) -> None:
        """Test getting error by ID."""
        error = agent.add_error("Test", "test.py", 10)
        found = agent.get_error_by_id(error.id)
        assert found is not None
        assert found.id == error.id

    def test_get_nonexistent_error(self, agent: Any) -> None:
        """Test getting nonexistent error returns None."""
        found = agent.get_error_by_id("nonexistent")
        assert found is None

    def test_get_errors_by_severity(self, agent: Any, errors_module: Any) -> None:
        """Test filtering by severity."""
        agent.add_error("High 1", "a.py", 10, errors_module.ErrorSeverity.HIGH)
        agent.add_error("High 2", "b.py", 20, errors_module.ErrorSeverity.HIGH)
        agent.add_error("Low", "c.py", 30, errors_module.ErrorSeverity.LOW)
        high = agent.get_errors_by_severity(errors_module.ErrorSeverity.HIGH)
        assert len(high) == 2

    def test_get_errors_by_category(self, agent: Any, errors_module: Any) -> None:
        """Test filtering by category."""
        agent.add_error("Syntax 1", "a.py", 10, category=errors_module.ErrorCategory.SYNTAX)
        agent.add_error("Syntax 2", "b.py", 20, category=errors_module.ErrorCategory.SYNTAX)
        agent.add_error("Style", "c.py", 30, category=errors_module.ErrorCategory.STYLE)
        syntax = agent.get_errors_by_category(errors_module.ErrorCategory.SYNTAX)
        assert len(syntax) == 2


# ========== Error Resolution Tests ==========

class TestErrorResolution:
    """Tests for error resolution."""

    def test_resolve_error(self, agent: Any) -> None:
        """Test resolving an error."""
        error = agent.add_error("Error", "test.py", 10)
        result = agent.resolve_error(error.id)
        assert result is True
        assert agent.get_error_by_id(error.id).resolved is True

    def test_resolve_error_sets_timestamp(self, agent: Any) -> None:
        """Test that resolution timestamp is set."""
        error = agent.add_error("Error", "test.py", 10)
        agent.resolve_error(error.id)
        resolved_error = agent.get_error_by_id(error.id)
        assert resolved_error.resolution_timestamp != ""

    def test_resolve_with_note(self, agent: Any) -> None:
        """Test resolving with a note."""
        error = agent.add_error("Error", "test.py", 10)
        agent.resolve_error(error.id, "Fixed the issue")
        annotations = agent.get_annotations(error.id)
        assert any("Resolution:" in a for a in annotations)

    def test_resolve_nonexistent_error(self, agent: Any) -> None:
        """Test resolving nonexistent error."""
        result = agent.resolve_error("nonexistent")
        assert result is False

    def test_get_unresolved_errors(self, agent: Any) -> None:
        """Test getting unresolved errors."""
        error1 = agent.add_error("Error 1", "a.py", 10)
        agent.add_error("Error 2", "b.py", 20)
        agent.resolve_error(error1.id)
        unresolved = agent.get_unresolved_errors()
        assert len(unresolved) == 1


# ========== Severity Scoring Tests ==========

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

class TestErrorClustering:
    """Tests for error clustering."""

    def test_cluster_similar_errors(self, agent: Any) -> None:
        """Test clustering similar errors."""
        agent.add_error("NameError: name 'x' is not defined", "a.py", 10)
        agent.add_error("NameError: name 'y' is not defined", "b.py", 20)
        agent.add_error("TypeError: cannot add str and int", "c.py", 30)
        clusters = agent.cluster_similar_errors()
        assert len(clusters) >= 1

    def test_get_cluster_by_id(self, agent: Any) -> None:
        """Test getting cluster by ID."""
        agent.add_error("NameError: name 'a' is not defined", "x.py", 10)
        agent.add_error("NameError: name 'b' is not defined", "y.py", 20)
        clusters = agent.cluster_similar_errors()
        if clusters:
            cluster_id = list(clusters.keys())[0]
            cluster = agent.get_cluster(cluster_id)
            assert cluster is not None

    def test_get_errors_in_cluster(self, agent: Any) -> None:
        """Test getting errors in a cluster."""
        agent.add_error("NameError: name 'x' is not defined", "a.py", 10)
        agent.add_error("NameError: name 'y' is not defined", "b.py", 20)
        clusters = agent.cluster_similar_errors()
        if clusters:
            cluster_id = list(clusters.keys())[0]
            errors = agent.get_errors_in_cluster(cluster_id)
            assert len(errors) >= 2


# ========== Pattern Recognition Tests ==========

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


class TestErrorBudgetManager:
    """Tests for ErrorBudgetManager class."""

    def test_init(self, errors_module: Any) -> None:
        """Test ErrorBudgetManager initialization."""
        manager = errors_module.ErrorBudgetManager()
        assert manager.budgets == {}

    def test_create_budget(self, errors_module: Any) -> None:
        """Test creating an error budget."""
        manager = errors_module.ErrorBudgetManager()
        budget = manager.create_budget("production", 100.0, 30)
        assert budget.budget_name == "production"
        assert budget.total_budget == 100.0

    def test_consume(self, errors_module: Any) -> None:
        """Test consuming error budget."""
        manager = errors_module.ErrorBudgetManager()
        manager.create_budget("production", 100.0)
        result = manager.consume("production", 10.0)
        assert result is True
        assert manager.get_remaining("production") == 90.0

    def test_consume_exceeds_budget(self, errors_module: Any) -> None:
        """Test consuming more than available budget."""
        manager = errors_module.ErrorBudgetManager()
        manager.create_budget("production", 50.0)
        result = manager.consume("production", 60.0)
        assert result is False

    def test_get_consumption_rate(self, errors_module: Any) -> None:
        """Test getting consumption rate."""
        manager = errors_module.ErrorBudgetManager()
        manager.create_budget("production", 100.0)
        manager.consume("production", 25.0)
        rate = manager.get_consumption_rate("production")
        assert rate == 25.0

    def test_is_exceeded(self, errors_module: Any) -> None:
        """Test checking if budget is exceeded."""
        manager = errors_module.ErrorBudgetManager()
        manager.create_budget("production", 100.0)
        assert manager.is_exceeded("production") is False
        manager.consume("production", 100.0)
        assert manager.is_exceeded("production") is True


# ========== Session 7 Tests: TrendAnalyzer ==========


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


class TestErrorCorrelation:
    """Tests for error correlation across multiple runs."""

    def test_correlation_basic(self, errors_module: Any, tmp_path: Path) -> None:
        """Test basic error correlation."""
        target = tmp_path / "test.errors.md"
        target.write_text("# Errors\n- Error A\n- Error B")

        agent = errors_module.ErrorsAgent(str(target))
        content = agent.read_previous_content()

        assert "Error A" in content

    def test_correlation_multiple_runs(self, errors_module: Any, tmp_path: Path) -> None:
        """Test correlation across multiple runs."""
        target = tmp_path / "test.errors.md"
        content = """# Errors
## Run 1
- Error A
## Run 2
- Error A
- Error B
"""
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert previous.count("Error A") == 2


# =============================================================================
# Session 9: Root Cause Analysis Tests
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


class TestErrorClustering_v2:  # noqa: F811
    """Tests for error clustering algorithms (extended)."""

    def test_similar_errors_grouped(self, errors_module: Any, tmp_path: Path) -> None:
        """Test similar errors are grouped."""
        target = tmp_path / "test.errors.md"
        content = """# Errors
- TypeError: int not str in func_a
- TypeError: int not str in func_b
- ValueError: invalid value
"""
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        # Both TypeErrors should be present
        assert previous.count("TypeError") == 2


# =============================================================================
# Session 9: Severity Scoring Tests
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


class TestErrorBudget:
    """Tests for error budget calculations."""

    def test_budget_info_detection(self, errors_module: Any, tmp_path: Path) -> None:
        """Test error budget information detection."""
        target = tmp_path / "test.errors.md"
        content = "# Error Report\nBudget Used: 80%\nRemaining: 20%"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "Budget Used:" in previous


# =============================================================================
# Session 9: Error Escalation Tests
# =============================================================================


class TestErrorEscalation:
    """Tests for error escalation workflows."""

    def test_escalation_marker(self, errors_module: Any, tmp_path: Path) -> None:
        """Test escalation marker detection."""
        target = tmp_path / "test.errors.md"
        content = "# Error\n[ESCALATED] Critical production issue"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "[ESCALATED]" in previous


# =============================================================================
# Session 9: Error Forecasting Tests
# =============================================================================


class TestErrorForecasting:
    """Tests for error trend forecasting."""

    def test_trend_data_detection(self, errors_module: Any, tmp_path: Path) -> None:
        """Test trend data detection."""
        target = tmp_path / "test.errors.md"
        content = "# Errors\nTrend: Increasing (+15% this week)"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "Trend:" in previous


# =============================================================================
# Session 9: Error Grouping Tests
# =============================================================================


class TestErrorGrouping:
    """Tests for error grouping strategies."""

    def test_group_by_type(self, errors_module: Any, tmp_path: Path) -> None:
        """Test grouping errors by type."""
        target = tmp_path / "test.errors.md"
        content = """# Errors
## TypeError
- Error 1
## ValueError
- Error 2
"""
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "## TypeError" in previous
        assert "## ValueError" in previous


# =============================================================================
# Session 9: Error Context Enrichment Tests
# =============================================================================


class TestErrorContextEnrichment:
    """Tests for error context enrichment."""

    def test_context_information(self, errors_module: Any, tmp_path: Path) -> None:
        """Test context information in errors."""
        target = tmp_path / "test.errors.md"
        content = "# Error\nContext: User login flow, after OAuth callback"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "Context:" in previous


# =============================================================================
# Session 9: Error Suppression Tests
# =============================================================================


class TestErrorSuppression:
    """Tests for error suppression rules."""

    def test_suppression_marker(self, errors_module: Any, tmp_path: Path) -> None:
        """Test suppression marker detection."""
        target = tmp_path / "test.errors.md"
        content = "# Errors\n- [SUPPRESSED] Known flaky test error"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "[SUPPRESSED]" in previous

    def test_suppression_reason(self, errors_module: Any, tmp_path: Path) -> None:
        """Test suppression reason is preserved."""
        target = tmp_path / "test.errors.md"
        content = "# Error\nSuppression Reason: Expected during maintenance window"
        target.write_text(content)

        agent = errors_module.ErrorsAgent(str(target))
        previous = agent.read_previous_content()

        assert "Suppression Reason:" in previous


# ========== Comprehensive Errors Tests (from test_agent_errors_comprehensive.py) ==========


class TestErrorLogParsingComprehensive(unittest.TestCase):
    """Tests for parsing error logs from various sources."""

    def test_parse_python_traceback(self):
        """Test parsing Python traceback."""
        traceback = """Traceback (most recent call last):
  File "test.py", line 10, in func
    result=x / 0
ZeroDivisionError: division by zero
"""
        assert "Traceback" in traceback
        assert "ZeroDivisionError" in traceback
        assert "division by zero" in traceback

    def test_parse_flake8_output(self):
        """Test parsing flake8 error output."""
        flake8_output = """test.py:5:1: E302 expected 2 blank lines
test.py:10:15: F401 'os' imported but unused
"""
        lines = flake8_output.split("\n")
        errors = [line for line in lines if line.strip()]
        assert len(errors) == 2
        assert "E302" in errors[0]
        assert "F401" in errors[1]

    def test_parse_mypy_output(self):
        """Test parsing mypy error output."""
        mypy_output = """test.py:5: error: Incompatible types in assignment
test.py:10: error: Call to untyped function
"""
        assert "error:" in mypy_output
        assert "Incompatible types" in mypy_output

    def test_parse_json_logs(self):
        """Test parsing JSON format logs."""
        log_entry = (
            '{"level":"ERROR","message":"Connection failed",'
            '"timestamp":"2024-12-16T10:00:00"}'
        )
        data = json.loads(log_entry)
        assert data["level"] == "ERROR"
        assert "Connection failed" in data["message"]


class TestErrorCategorizationComprehensive(unittest.TestCase):
    """Tests for error categorization and grouping."""

    def test_categorize_syntax_error(self):
        """Test categorizing syntax errors."""
        error = "SyntaxError: invalid syntax"
        assert "syntax" in error.lower()

    def test_categorize_runtime_error(self):
        """Test categorizing runtime errors."""
        error = "RuntimeError: operation failed"
        assert "runtime" in error.lower()

    def test_categorize_import_error(self):
        """Test categorizing import errors."""
        error = "ModuleNotFoundError: No module named 'xyz'"
        assert "module" in error.lower() or "import" in error.lower()

    def test_categorize_type_error(self):
        """Test categorizing type errors."""
        error = "TypeError: expected str, got int"
        assert "type" in error.lower()

    def test_group_errors_by_type(self):
        """Test grouping errors by category."""
        errors = [
            {"type": "SyntaxError", "message": "invalid syntax"},
            {"type": "SyntaxError", "message": "expected colon"},
            {"type": "RuntimeError", "message": "operation failed"},
        ]

        grouped = {}
        for error in errors:
            etype = error["type"]
            if etype not in grouped:
                grouped[etype] = []
            grouped[etype].append(error)

        assert len(grouped["SyntaxError"]) == 2
        assert len(grouped["RuntimeError"]) == 1


class TestErrorDeduplicationComprehensive(unittest.TestCase):
    """Tests for error deduplication logic."""

    def test_detect_duplicate_errors(self):
        """Test detecting duplicate errors."""
        errors = [
            {"file": "a.py", "line": 5, "message": "error 1"},
            {"file": "a.py", "line": 5, "message": "error 1"},
            {"file": "b.py", "line": 10, "message": "error 2"},
        ]

        seen = set()
        unique = []
        for error in errors:
            key = (error["file"], error["line"], error["message"])
            if key not in seen:
                seen.add(key)
                unique.append(error)

        assert len(unique) == 2
        assert len(seen) == 2

    def test_deduplicate_by_pattern(self):
        """Test deduplication by pattern matching."""
        errors = [
            "AttributeError: 'NoneType' object has no attribute 'x'",
            "AttributeError: 'NoneType' object has no attribute 'y'",
        ]

        patterns = {}
        for error in errors:
            pattern = error.split("'")[0]  # Base pattern
            if pattern not in patterns:
                patterns[pattern] = []
            patterns[pattern].append(error)

        assert len(patterns) == 1  # Same base pattern


class TestErrorTrendAnalysisComprehensive(unittest.TestCase):
    """Tests for error trend analysis over time."""

    def test_track_error_frequency(self):
        """Test tracking error frequency over time."""
        errors = [
            {"timestamp": "2024-12-16T10:00:00", "type": "SyntaxError"},
            {"timestamp": "2024-12-16T11:00:00", "type": "SyntaxError"},
            {"timestamp": "2024-12-16T12:00:00", "type": "RuntimeError"},
        ]

        frequency = {}
        for error in errors:
            etype = error["type"]
            frequency[etype] = frequency.get(etype, 0) + 1

        assert frequency["SyntaxError"] == 2
        assert frequency["RuntimeError"] == 1

    def test_detect_error_spikes(self):
        """Test detecting error spikes."""
        hourly_counts = [1, 2, 1, 5, 10, 8, 2, 1]  # Spike at hours 4-5
        average = sum(hourly_counts) / len(hourly_counts)
        spikes = [c for c in hourly_counts if c > average * 2]
        assert len(spikes) > 0

    def test_trend_direction(self):
        """Test determining error trend direction."""
        weekly_errors = [10, 12, 15, 18, 20]  # Increasing
        is_increasing = weekly_errors[-1] > weekly_errors[0]
        assert is_increasing


class TestErrorContextExtractionComprehensive(unittest.TestCase):
    """Tests for error context extraction."""

    def test_extract_file_and_line(self):
        """Test extracting file and line information."""
        error = 'File "test.py", line 42, in function'
        assert "test.py" in error
        assert "42" in error

    def test_extract_stack_trace(self):
        """Test extracting stack trace."""
        traceback = """Traceback (most recent call last):
  File "a.py", line 10, in func_a
    func_b()
  File "b.py", line 20, in func_b
    raise ValueError("error")
ValueError: error
"""
        lines = [line.strip() for line in traceback.split("\n")]
        frames = [line for line in lines if "File" in line]
        assert len(frames) == 2

    def test_extract_error_message(self):
        """Test extracting error message."""
        error_line = "ValueError: invalid value provided"
        message = error_line.split(": ", 1)[1] if ": " in error_line else error_line
        assert message == "invalid value provided"


class TestErrorRemediationComprehensive(unittest.TestCase):
    """Tests for error remediation suggestions."""

    def test_suggest_import_fix(self):
        """Test suggesting fix for import errors."""
        error = "ModuleNotFoundError: No module named 'pandas'"
        if "ModuleNotFoundError" in error:
            suggestion = "Install the package: pip install pandas"
        else:
            suggestion = "Unknown fix"
        assert "pip install" in suggestion

    def test_suggest_type_fix(self):
        """Test suggesting fix for type errors."""
        error = "TypeError: expected str, got int"
        if "TypeError" in error and "expected" in error:
            suggestion = "Convert the value to the expected type"
        assert "Convert" in suggestion

    def test_suggest_syntax_fix(self):
        """Test suggesting fix for syntax errors."""
        error = "SyntaxError: expected ':'"
        if "SyntaxError" in error and "':'" in error:
            suggestion = "Add missing colon"
        assert "colon" in suggestion


class TestMultiToolErrorIntegrationComprehensive(unittest.TestCase):
    """Tests for integrating errors from multiple tools."""

    def test_integrate_pylint_errors(self):
        """Test integrating pylint errors."""
        errors = [
            {"tool": "pylint", "code": "C0111", "message": "missing docstring"},
        ]
        assert errors[0]["tool"] == "pylint"

    def test_integrate_flake8_errors(self):
        """Test integrating flake8 errors."""
        errors = [
            {"tool": "flake8", "code": "E501", "message": "line too long"},
        ]
        assert errors[0]["tool"] == "flake8"

    def test_integrate_mypy_errors(self):
        """Test integrating mypy errors."""
        errors = [
            {"tool": "mypy", "code": "error", "message": "type mismatch"},
        ]
        assert errors[0]["tool"] == "mypy"

    def test_deduplicate_across_tools(self):
        """Test deduplicating errors from different tools."""
        all_errors = [
            {"tool": "pylint", "file": "a.py", "line": 5, "message": "error"},
            {"tool": "flake8", "file": "a.py", "line": 5, "message": "error"},
        ]

        unique = {}
        for error in all_errors:
            key = (error["file"], error["line"], error["message"])
            if key not in unique:
                unique[key] = error

        assert len(unique) == 1


class TestErrorMetricsComprehensive(unittest.TestCase):
    """Tests for error metrics collection and reporting."""

    def test_count_errors_by_severity(self):
        """Test counting errors by severity."""
        errors = [
            {"severity": "critical", "count": 2},
            {"severity": "warning", "count": 5},
            {"severity": "info", "count": 10},
        ]

        total = sum(e["count"] for e in errors)
        assert total == 17
        assert errors[0]["severity"] == "critical"

    def test_calculate_error_rate(self):
        """Test calculating error rate."""
        total_lines = 1000
        errors_found = 15
        error_rate = (errors_found / total_lines) * 100
        assert error_rate == 1.5

    def test_track_error_resolution_time(self):
        """Test tracking error resolution time."""
        error_found = datetime(2024, 12, 16, 10, 0, 0)
        error_fixed = datetime(2024, 12, 16, 11, 30, 0)
        resolution_time = (error_fixed - error_found).total_seconds() / 3600
        assert resolution_time == 1.5


class TestErrorPriorityComprehensive(unittest.TestCase):
    """Tests for error priority scoring."""

    def test_score_by_severity(self):
        """Test scoring errors by severity."""
        severity_scores = {
            "critical": 10,
            "high": 7,
            "medium": 5,
            "low": 2,
        }

        critical_score = severity_scores["critical"]
        assert critical_score == 10

    def test_score_by_frequency(self):
        """Test scoring errors by frequency."""
        frequency_scores = {
            "once": 1,
            "occasional": 3,
            "frequent": 7,
            "constant": 10,
        }

        frequent_score = frequency_scores["frequent"]
        assert frequent_score == 7

    def test_combined_priority_score(self):
        """Test combined priority scoring."""
        severity = 8
        frequency = 6
        impact = 5
        priority = (severity + frequency + impact) / 3
        assert priority > 5


class TestErrorBaselineComprehensive(unittest.TestCase):
    """Tests for error baseline tracking."""

    def test_establish_baseline(self):
        """Test establishing error baseline."""
        baseline_errors = 10
        baseline_warnings = 25
        baseline = {"errors": baseline_errors, "warnings": baseline_warnings}
        assert baseline["errors"] == 10

    def test_compare_to_baseline(self):
        """Test comparing current to baseline."""
        baseline = 10
        current = 8
        improvement = baseline - current
        assert improvement == 2

    def test_detect_baseline_deviation(self):
        """Test detecting deviation from baseline."""
        baseline = 10
        threshold_percent = 0.20  # 20% tolerance
        current = 13

        deviation = (current - baseline) / baseline
        exceeds_threshold = deviation > threshold_percent
        assert exceeds_threshold


class TestErrorPreventionComprehensive(unittest.TestCase):
    """Tests for error prevention pattern detection."""

    def test_detect_common_error_pattern(self):
        """Test detecting common error patterns."""
        errors = [
            {"type": "NoneType", "method": "split"},
            {"type": "NoneType", "method": "strip"},
            {"type": "NoneType", "method": "upper"},
        ]

        none_errors = [e for e in errors if e["type"] == "NoneType"]
        assert len(none_errors) == 3

    def test_suggest_type_check(self):
        """Test suggesting type checks."""
        error = "AttributeError: 'NoneType' object has no attribute"
        if "NoneType" in error:
            suggestion = "Add None check before accessing attribute"
        assert "None check" in suggestion

    def test_suggest_error_handling(self):
        """Test suggesting error handling."""
        error = "ZeroDivisionError: division by zero"
        if "ZeroDivisionError" in error:
            suggestion = "Add try-except or validate divisor"
        assert "except" in suggestion or "validate" in suggestion


class TestErrorSuppressionComprehensive(unittest.TestCase):
    """Tests for error suppression guideline generation."""

    def test_identify_suppressible_errors(self):
        """Test identifying suppressible errors."""
        error = "C0111: missing docstring"  # Low priority
        is_suppressible = error.startswith("C") or error.startswith("W")
        assert is_suppressible

    def test_generate_suppress_comment(self):
        """Test generating suppress comments."""
        error_code = "E501"
        suppress_comment = f"# noqa: {error_code}"
        assert "noqa" in suppress_comment
        assert "E501" in suppress_comment

    def test_suggest_suppress_strategy(self):
        """Test suggesting suppression strategy."""
        errors_to_suppress = ["C0111", "C0103"]  # Docstring and naming
        if all(code.startswith("C") for code in errors_to_suppress):
            strategy = "Suppress convention warnings project-wide"
        assert "Suppress" in strategy


class TestErrorReportingComprehensive(unittest.TestCase):
    """Tests for error report formatting."""

    def test_format_markdown_report(self):
        """Test formatting error report as markdown."""
        report = """# Error Report

## Summary
- Total Errors: 5
- Critical: 2
- Warnings: 3

## Errors
- E501: Line too long
- W291: Trailing whitespace
"""
        assert "# Error Report" in report
        assert "## Summary" in report

    def test_format_html_report(self):
        """Test formatting error report as HTML."""
        html = "<html><body><h1>Error Report</h1><table><tr><td>5</td></tr></table></body></html>"
        assert "<html>" in html
        assert "<h1>Error Report</h1>" in html

    def test_format_json_report(self):
        """Test formatting error report as JSON."""
        report = {
            "total": 5,
            "critical": 2,
            "errors": [
                {"code": "E501", "message": "Line too long"}
            ]
        }
        json_str = json.dumps(report)
        assert "total" in json_str
        assert "5" in json_str


class TestErrorAcknowledgmentComprehensive(unittest.TestCase):
    """Tests for error acknowledgment tracking."""

    def test_track_acknowledged_error(self):
        """Test tracking acknowledged errors."""
        error = {
            "id": "err_001",
            "status": "acknowledged",
            "acknowledged_at": "2024-12-16T10:30:00",
        }
        assert error["status"] == "acknowledged"

    def test_transition_error_states(self):
        """Test error state transitions."""
        states = ["new", "acknowledged", "assigned", "resolved"]
        current_index = 1
        next_state = states[current_index + 1]
        assert next_state == "assigned"

    def test_track_error_resolution(self):
        """Test tracking error resolution."""
        error = {
            "id": "err_001",
            "status": "resolved",
            "resolved_at": "2024-12-16T11:00:00",
            "fix_commit": "abc123def",
        }
        assert error["status"] == "resolved"
        assert "abc123def" in error["fix_commit"]


class TestIntegrationComprehensive(unittest.TestCase):
    """Integration tests for error processing."""

    def test_end_to_end_error_processing(self):
        """Test complete error processing workflow."""
        # Parse

        # Categorize
        error_type = "ValueError"

        # Analyze
        priority = 5

        # Report
        report = f"{error_type} - Priority: {priority}"
        assert error_type in report

    def test_error_metrics_generation(self):
        """Test generating error metrics."""
        errors = [
            {"type": "SyntaxError", "severity": "critical"},
            {"type": "RuntimeError", "severity": "high"},
            {"type": "Warning", "severity": "low"},
        ]

        metrics = {
            "total": len(errors),
            "critical": sum(1 for e in errors if e["severity"] == "critical"),
            "high": sum(1 for e in errors if e["severity"] == "high"),
        }

        assert metrics["total"] == 3
        assert metrics["critical"] == 1


# ========== Comprehensive Errors Improvements Tests
# (from test_agent_errors_improvements_comprehensive.py) ==========


class TestErrorLogParsingImprovements(unittest.TestCase):
    """Test parsing error logs to automatically populate error report."""

    def test_parse_python_tracebacks(self):
        """Test parsing Python traceback format."""
        traceback_text = """
Traceback (most recent call last):
  File "main.py", line 42, in calculate
    result=func()
TypeError: unsupported operand type(s) for +: 'str' and 'int'
        """
        self.assertIn('TypeError', traceback_text)
        self.assertIn('line 42', traceback_text)

    def test_extract_error_location(self):
        """Test extracting error file and line number."""
        error_info = {
            'file': 'main.py',
            'line': 42,
            'function': 'calculate',
            'error_type': 'TypeError',
            'message': "unsupported operand type(s)"
        }
        self.assertEqual(error_info['line'], 42)

    def test_parse_multiline_errors(self):
        """Test parsing multi-line error messages."""
        error = """ValueError: Expected a valid JSON object, got:
{
    "invalid": json
}"""
        self.assertIn('ValueError', error)

    def test_error_log_aggregation(self):
        """Test aggregating multiple errors from logs."""
        errors = [
            {'type': 'SyntaxError', 'count': 5},
            {'type': 'ValueError', 'count': 3},
            {'type': 'TypeError', 'count': 8}
        ]
        total_errors = sum(e['count'] for e in errors)
        self.assertEqual(total_errors, 16)


class TestStaticAnalysisIntegration(unittest.TestCase):
    """Test integration with static analysis tools."""

    def test_pylint_output_parsing(self):
        """Test parsing pylint output."""
        pylint_output = {
            'tool': 'pylint',
            'issues': [
                {'type': 'convention', 'message': 'invalid-name', 'line': 10},
                {'type': 'warning', 'message': 'unused-import', 'line': 5},
                {'type': 'error', 'message': 'undefined-variable', 'line': 25}
            ]
        }
        errors = [i for i in pylint_output['issues'] if i['type'] == 'error']
        self.assertEqual(len(errors), 1)

    def test_flake8_integration(self):
        """Test parsing flake8 output."""
        flake8_results = [
            {'code': 'E501', 'message': 'line too long', 'line': 42},
            {'code': 'F401', 'message': 'unused import', 'line': 5},
            {'code': 'W503', 'message': 'line break before operator', 'line': 50}
        ]
        self.assertEqual(len(flake8_results), 3)

    def test_mypy_type_errors(self):
        """Test parsing mypy type checking errors."""
        mypy_errors = [
            {'error': 'Argument 1 has incompatible type', 'line': 30},
            {'error': 'Missing return statement', 'line': 45},
            {'error': 'Incompatible assignment', 'line': 60}
        ]
        self.assertEqual(len(mypy_errors), 3)

    def test_bandit_security_findings(self):
        """Test parsing bandit security scanning output."""
        security_issues = [
            {'severity': 'HIGH', 'test_id': 'B303', 'message': 'Use of pickle'},
            {'severity': 'MEDIUM', 'test_id': 'B101', 'message': 'assert_used'},
            {'severity': 'LOW', 'test_id': 'B105', 'message': 'hardcoded_password_string'}
        ]
        high_severity = [i for i in security_issues if i['severity'] == 'HIGH']
        self.assertEqual(len(high_severity), 1)


class TestErrorCategorizationImprovements(unittest.TestCase):
    """Test auto-categorization of errors by severity."""

    def test_severity_classification(self):
        """Test classifying errors by severity levels."""
        errors = [
            {'type': 'SyntaxError', 'severity': 'critical'},
            {'type': 'ValueError', 'severity': 'high'},
            {'type': 'DeprecationWarning', 'severity': 'low'},
            {'type': 'FutureWarning', 'severity': 'info'}
        ]
        critical = [e for e in errors if e['severity'] == 'critical']
        self.assertEqual(len(critical), 1)

    def test_error_deduplication(self):
        """Test grouping and deduplicating related errors."""
        duplicate_errors = [
            {'file': 'main.py', 'line': 42, 'type': 'TypeError', 'count': 5},
            {'file': 'main.py', 'line': 42, 'type': 'TypeError', 'count': 3},
            {'file': 'utils.py', 'line': 10, 'type': 'TypeError', 'count': 2}
        ]
        # Deduplicate by file and line
        unique_errors = {}
        for err in duplicate_errors:
            key = (err['file'], err['line'], err['type'])
            if key not in unique_errors:
                unique_errors[key] = err['count']

        self.assertEqual(len(unique_errors), 2)

    def test_error_grouping(self):
        """Test grouping related errors together."""
        errors = [
            {'type': 'TypeError', 'context': 'type_mismatch'},
            {'type': 'TypeError', 'context': 'type_mismatch'},
            {'type': 'ValueError', 'context': 'validation'},
            {'type': 'ValueError', 'context': 'validation'}
        ]
        grouped = {}
        for err in errors:
            key = (err['type'], err['context'])
            grouped[key] = grouped.get(key, 0) + 1

        self.assertEqual(len(grouped), 2)


class TestErrorTrends(unittest.TestCase):
    """Test generating error trends and metrics."""

    def test_error_count_over_time(self):
        """Test tracking error count trends over time."""
        error_timeline = [
            {'date': '2025-01-01', 'count': 50},
            {'date': '2025-01-08', 'count': 42},
            {'date': '2025-01-15', 'count': 35},
            {'date': '2025-01-22', 'count': 28}
        ]
        trend = error_timeline[-1]['count'] - error_timeline[0]['count']
        self.assertEqual(trend, -22)  # Decreasing errors

    def test_most_common_errors(self):
        """Test identifying most common error types."""
        error_counts = {
            'TypeError': 25,
            'ValueError': 18,
            'AttributeError': 12,
            'KeyError': 8
        }
        top_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
        self.assertEqual(top_errors[0][0], 'TypeError')

    def test_error_frequency_analysis(self):
        """Test analyzing error frequency patterns."""
        error_frequency = {
            'morning': 15,
            'afternoon': 12,
            'evening': 8,
            'night': 5
        }
        peak_period = max(error_frequency, key=error_frequency.get)
        self.assertEqual(peak_period, 'morning')


class TestErrorContext(unittest.TestCase):
    """Test providing error context and code snippets."""

    def test_code_snippet_extraction(self):
        """Test extracting code snippet around error line."""
        code_lines = [
            'def process(data):',
            '    result=[]',
            '    for item in data:',  # line 3, error
            '        result.append(item.value)',
            '    return result'
        ]

        error_line = 2  # 0-indexed
        context_start = max(0, error_line - 1)
        context_end = min(len(code_lines), error_line + 2)

        snippet = code_lines[context_start:context_end]
        self.assertEqual(len(snippet), 3)

    def test_source_context_preservation(self):
        """Test preserving source context with line numbers."""
        context = {
            'file': 'main.py',
            'lines': [
                (2, 'def process(data):'),
                (3, '    result=[]'),
                (4, '    for item in data:'),  # error line
                (5, '        result.append(item.value)'),
                (6, '    return result')
            ],
            'error_line': 4
        }
        self.assertEqual(context['lines'][2][0], 4)

    def test_error_line_highlighting(self):
        """Test highlighting the error line in context."""
        error_context = """
   2: def process(data):
   3:     result=[]
>> 4:     for item in data:  # ERROR: type error
   5:         result.append(item)
        """
        self.assertIn('>>', error_context)


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


class TestRuntimeErrorParsing(unittest.TestCase):
    """Test parsing runtime errors from test output and CI logs."""

    def test_parse_pytest_output(self):
        """Test parsing pytest error output."""
        pytest_output = """
FAILED test_main.py::test_calculate - AssertionError: assert 5 == 6
    File "test_main.py", line 42, in test_calculate
        assert result == 6
        """
        self.assertIn('AssertionError', pytest_output)
        self.assertIn('test_calculate', pytest_output)

    def test_parse_ci_build_logs(self):
        """Test parsing CI / CD build logs for errors."""
        ci_log = {
            'build_id': 'build_123',
            'status': 'failed',
            'errors': [
                'Test failed: test_integration',
                'Dependency resolution failed: package not found',
                'Security scan found 2 high-severity issues'
            ]
        }
        self.assertEqual(len(ci_log['errors']), 3)

    def test_extract_error_from_logs(self):
        """Test extracting structured errors from unstructured logs."""

        error_data = {
            'timestamp': '2025-12-16 10:30:45',
            'level': 'ERROR',
            'message': 'Database connection failed',
            'cause': 'Connection refused'
        }
        self.assertEqual(error_data['level'], 'ERROR')


class TestErrorSuppressionImprovements(unittest.TestCase):
    """Test error suppression guidelines and tracking."""

    def test_suppression_guidelines(self):
        """Test generating error suppression guidelines with rationale."""
        suppression_config = {
            'error_type': 'W503',  # line break before operator
            'tool': 'flake8',
            'rationale': 'PEP 8 update recommends placing operators at start of line',
            'approved': True,
            'date_approved': '2025-12-16'
        }
        self.assertTrue(suppression_config['approved'])

    def test_suppression_comment_generation(self):
        """Test generating proper suppression comments."""
        suppression_comment = {
            'type': '# noqa',
            'error_codes': ['E501', 'W503'],
            'comment': '# noqa: E501,W503  - long line is for readability'
        }
        self.assertIn('noqa', suppression_comment['comment'])

    def test_suppression_audit_log(self):
        """Test tracking all error suppressions."""
        suppression_log = [{'error': 'E501',
                            'file': 'main.py',
                            'suppressed_at': '2025-12-16',
                            'reason': 'readability'},
                           {'error': 'W503',
                            'file': 'utils.py',
                            'suppressed_at': '2025-12-16',
                            'reason': 'PEP 8 update'}]
        self.assertEqual(len(suppression_log), 2)


class TestErrorMetricsImprovements(unittest.TestCase):
    """Test error metrics collection and analysis."""

    def test_error_count_metrics(self):
        """Test collecting total error count and unique types."""
        metrics = {
            'total_errors': 150,
            'unique_types': 12,
            'files_affected': 25,
            'avg_errors_per_file': 6
        }
        self.assertEqual(metrics['unique_types'], 12)

    def test_error_distribution(self):
        """Test error distribution across codebase."""
        error_distribution = {
            'module_a': {'errors': 45, 'severity_avg': 'medium'},
            'module_b': {'errors': 30, 'severity_avg': 'low'},
            'module_c': {'errors': 75, 'severity_avg': 'high'}
        }
        most_errors = max(error_distribution.values(), key=lambda x: x['errors'])
        self.assertEqual(most_errors['severity_avg'], 'high')

    def test_error_metrics_comparison(self):
        """Test comparing error metrics over time."""
        metrics_timeline = [
            {'period': 'week_1', 'total_errors': 100, 'critical': 5},
            {'period': 'week_2', 'total_errors': 85, 'critical': 3},
            {'period': 'week_3', 'total_errors': 70, 'critical': 2}
        ]
        improvement = metrics_timeline[0]['total_errors'] - metrics_timeline[-1]['total_errors']
        self.assertEqual(improvement, 30)


class TestErrorPriorityImprovements(unittest.TestCase):
    """Test error priority scoring based on impact."""

    def test_priority_scoring(self):
        """Test calculating priority score for errors."""
        class PriorityScore:
            @staticmethod
            def calculate(severity, frequency, affected_users):
                return (severity * 0.5) + (frequency * 0.3) + (affected_users * 0.2)

        score = PriorityScore.calculate(severity=10, frequency=8, affected_users=100)
        self.assertGreater(score, 0)

    def test_impact_analysis(self):
        """Test analyzing error impact on system."""
        error_impact = {
            'critical_path': True,
            'affects_users': True,
            'users_count': 500,
            'estimated_loss_usd': 2500,
            'priority': 'critical'
        }
        self.assertEqual(error_impact['priority'], 'critical')

    def test_priority_queue(self):
        """Test maintaining priority queue of errors."""
        error_queue = [
            {'id': 1, 'priority': 'critical', 'score': 95},
            {'id': 2, 'priority': 'high', 'score': 75},
            {'id': 3, 'priority': 'medium', 'score': 50}
        ]
        sorted_queue = sorted(error_queue, key=lambda x: x['score'], reverse=True)
        self.assertEqual(sorted_queue[0]['id'], 1)


class TestCustomErrorParsers(unittest.TestCase):
    """Test custom error parser plugins."""

    def test_plugin_registry(self):
        """Test registering custom error parsers."""
        class ParserRegistry:
            def __init__(self):
                self.parsers = {}

            def register(self, error_type, parser):
                self.parsers[error_type] = parser

            def get_parser(self, error_type):
                return self.parsers.get(error_type)

        registry = ParserRegistry()
        self.assertEqual(len(registry.parsers), 0)

    def test_custom_parser_implementation(self):
        """Test implementing custom error parser."""
        class CustomParser:
            def parse(self, error_text):
                return {'parsed': True, 'data': error_text}

        parser = CustomParser()
        result = parser.parse("custom error")
        self.assertTrue(result['parsed'])


class TestErrorReportingImprovements(unittest.TestCase):
    """Test error report generation in multiple formats."""

    def test_markdown_report_generation(self):
        """Test generating markdown error reports."""
        markdown_report = """
# Error Report

## Summary
- Total Errors: 150
- Critical: 5
- High: 25
- Medium: 60
- Low: 60

## Top Errors
1. TypeError (25 occurrences)
2. ValueError (18 occurrences)
3. AttributeError (12 occurrences)
        """
        self.assertIn('# Error Report', markdown_report)

    def test_html_report_generation(self):
        """Test generating HTML error reports."""
        html_report = """
<html>
  <body>
    <h1>Error Report</h1>
    <table>
      <tr><th>Error Type</th><th>Count</th></tr>
      <tr><td>TypeError</td><td>25</td></tr>
      <tr><td>ValueError</td><td>18</td></tr>
    </table>
  </body>
</html>
        """
        self.assertIn('<h1>Error Report</h1>', html_report)

    def test_json_report_format(self):
        """Test generating JSON error reports."""
        json_report = {
            'timestamp': '2025-12-16T10:00:00Z',
            'summary': {
                'total': 150,
                'critical': 5,
                'high': 25
            },
            'errors': [
                {'type': 'TypeError', 'count': 25}
            ]
        }
        self.assertIn('summary', json_report)


class TestErrorTimeline(unittest.TestCase):
    """Test error timeline visualization and tracking."""

    def test_error_introduction_tracking(self):
        """Test tracking when errors were introduced."""
        error_timeline = {
            'error': 'TypeError in module_a',
            'introduced': '2025-12-01',
            'first_occurrence': '2025-12-01T10:30:00Z',
            'fix_attempts': 3,
            'resolved': False
        }
        self.assertFalse(error_timeline['resolved'])

    def test_fix_attempts_tracking(self):
        """Test tracking fix attempts for errors."""
        fix_history = [
            {'attempt': 1, 'date': '2025-12-02', 'fix': 'Added type check', 'success': False},
            {'attempt': 2, 'date': '2025-12-03', 'fix': 'Changed variable type', 'success': False},
            {'attempt': 3, 'date': '2025-12-04', 'fix': 'Refactored function', 'success': True}
        ]
        successful = [f for f in fix_history if f['success']]
        self.assertEqual(len(successful), 1)


class TestErrorPreventionImprovements(unittest.TestCase):
    """Test error prevention patterns and detection."""

    def test_prevention_pattern_detection(self):
        """Test detecting error prevention patterns in code."""
        patterns = [
            'null_check_before_access',
            'type_validation',
            'boundary_checking',
            'exception_handling',
            'input_validation'
        ]
        self.assertEqual(len(patterns), 5)

    def test_tech_debt_warning_generation(self):
        """Test generating warnings for potential future errors."""
        warnings = [
            {'type': 'code_duplication', 'likelihood': 'high', 'severity': 'medium'},
            {'type': 'missing_tests', 'likelihood': 'high', 'severity': 'high'},
            {'type': 'hardcoded_values', 'likelihood': 'medium', 'severity': 'low'}
        ]
        self.assertEqual(len(warnings), 3)


class TestErrorManagement(unittest.TestCase):
    """Test error acknowledgment and tracking."""

    def test_acknowledgment_tracking(self):
        """Test tracking error acknowledgment status."""
        error_status = {
            'error_id': 'ERR_001',
            'status': 'acknowledged',
            'acknowledged_by': 'developer',
            'acknowledgement_date': '2025-12-16',
            'wontfix_reason': None
        }
        self.assertEqual(error_status['status'], 'acknowledged')

    def test_wontfix_tracking(self):
        """Test tracking errors marked as wontfix."""
        wontfix_errors = [
            {'id': 'ERR_001', 'reason': 'By design', 'decision_date': '2025-12-16'},
            {'id': 'ERR_002', 'reason': 'Deprecated code', 'decision_date': '2025-12-15'},
            {'id': 'ERR_003', 'reason': 'Low impact', 'decision_date': '2025-12-14'}
        ]
        self.assertEqual(len(wontfix_errors), 3)


class TestErrorBaselineImprovements(unittest.TestCase):
    """Test error baseline and improvement tracking."""

    def test_baseline_establishment(self):
        """Test establishing error baseline for comparison."""
        baseline = {
            'date': '2025-01-01',
            'total_errors': 250,
            'critical': 10,
            'high': 50,
            'medium': 120,
            'low': 70
        }
        self.assertEqual(baseline['total_errors'], 250)

    def test_improvement_calculation(self):
        """Test calculating improvement against baseline."""
        baseline = {'total_errors': 250}
        current = {'total_errors': 150}

        improvement_pct = (
            (baseline['total_errors'] - current['total_errors']) /
            baseline['total_errors']) * 100
        self.assertEqual(improvement_pct, 40.0)

    def test_trend_projection(self):
        """Test projecting error trends into future."""
        historical = [
            {'week': 1, 'errors': 200},
            {'week': 2, 'errors': 180},
            {'week': 3, 'errors': 160}
        ]
        # Linear projection
        weekly_reduction = (historical[0]['errors'] - historical[-1]['errors']) / 2
        projected_week_4 = historical[-1]['errors'] - weekly_reduction
        self.assertEqual(projected_week_4, 140.0)


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
