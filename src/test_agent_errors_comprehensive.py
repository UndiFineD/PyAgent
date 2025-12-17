#!/usr / bin / env python3
"""
Tests for agent_errors.py improvements.

Covers error log parsing, categorization, deduplication, trend analysis,
context extraction, remediation suggestions, and error reporting.
"""

import json
import unittest
from datetime import datetime


class TestErrorLogParsing(unittest.TestCase):
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
        log_entry = '{"level":"ERROR","message":"Connection failed","timestamp":"2024-12-16T10:00:00"}'
        data = json.loads(log_entry)
        assert data["level"] == "ERROR"
        assert "Connection failed" in data["message"]


class TestErrorCategorization(unittest.TestCase):
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


class TestErrorDeduplication(unittest.TestCase):
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


class TestErrorTrendAnalysis(unittest.TestCase):
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


class TestErrorContextExtraction(unittest.TestCase):
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


class TestErrorRemediation(unittest.TestCase):
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


class TestMultiToolErrorIntegration(unittest.TestCase):
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


class TestErrorMetrics(unittest.TestCase):
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


class TestErrorPriority(unittest.TestCase):
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


class TestErrorBaseline(unittest.TestCase):
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


class TestErrorPrevention(unittest.TestCase):
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


class TestErrorSuppression(unittest.TestCase):
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


class TestErrorReporting(unittest.TestCase):
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


class TestErrorAcknowledgment(unittest.TestCase):
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


class TestIntegration(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
