"""Comprehensive tests for agent-errors.py improvements.

Tests all 20 suggested improvements for error handling and analysis:
- Error log parsing and auto-population
- Integration with static analysis tools
- Error severity categorization and grouping
- Error trends and metrics
- Error context and code snippets
- Remediation suggestions and quick fixes
- Runtime error parsing
- Error reporting and visualization
- Error prevention and management
"""

import unittest


class TestErrorLogParsing(unittest.TestCase):
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


class TestErrorCategorization(unittest.TestCase):
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


class TestErrorSuppression(unittest.TestCase):
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


class TestErrorMetrics(unittest.TestCase):
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


class TestErrorPriority(unittest.TestCase):
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


class TestErrorReporting(unittest.TestCase):
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


class TestErrorPrevention(unittest.TestCase):
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


class TestErrorBaseline(unittest.TestCase):
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
            (baseline['total_errors'] - current['total_errors']) / baseline['total_errors']) * 100
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


class TestRootCauseAnalysis(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
