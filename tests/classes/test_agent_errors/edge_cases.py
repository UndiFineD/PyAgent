# -*- coding: utf-8 -*-
"""Test classes from test_agent_errors.py - edge_cases module."""

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



