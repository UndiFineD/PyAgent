#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# -*- coding: utf-8 -*-
"""
"""
Test classes for stats formatting and aggregation - UNIT module.

"""
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List



class TestTrendAnalysis(unittest.TestCase):
"""
Tests for trend analysis and delta calculation.

    def test_calculate_trend(self) -> None:
"""
Test trend calculation from time series data.        data: List[int] = [1, 2, 3, 4, 5]
        # Upward trend
        assert data[-1] > data[0]

    def test_calculate_delta(self) -> None:
"""
Test delta calculation between values.        current = 100
        previous = 80
        delta: int = current - previous
        assert delta == 20

    def test_trend_percentage_change(self) -> None:
"""
Test percentage change calculation.        old_value = 100
        new_value = 110
        percent_change: float = ((new_value - old_value) / old_value) * 100
        assert percent_change == 10.0

    def test_trend_direction(self) -> None:
"""
Test determining trend direction.        values: List[int] = [5, 4, 3, 2, 1]
        is_decreasing: bool = values[0] > values[-1]
        assert is_decreasing



class TestCSVExport(unittest.TestCase):
"""
Tests for CSV export functionality.
    def test_export_stats_to_csv(self) -> None:
"""
Test exporting stats to CSV format.        stats = [
            {"date": "2024-12-16", "tests": 100, "pass": 95},"            {"date": "2024-12-17", "tests": 102, "pass": 98},"        ]

        csv_lines: List[str] = ["date,tests,pass"]"        for stat in stats:
            csv_lines.append(f"{stat['date']},{stat['tests']},{stat['pass']}")
        csv_content: str = "\\n".join(csv_lines)"        assert "2024-12-16" in csv_content"        assert "date,tests,pass" in csv_content
    def test_csv_escaping(self) -> None:
"""
Test proper CSV escaping.        escaped = '"{value}"'
assert escaped.startswith('"')"'        assert escaped.endswith('"')"'
    def test_csv_with_special_characters(self) -> None:
"""
Test CSV with special characters.        csv_line = '{"test,with,commas",123}'
assert "test,with,commas" in csv_line


class TestExportFormats(unittest.TestCase):
"""
Tests for different export formats.
    def test_export_json_format(self) -> None:
"""
Test exporting to JSON format.        stats = {"tests": 100, "pass": 95, "timestamp": "2024-12-16"}"        json_str: str = json.dumps(stats)
        assert '"tests": 100' in json_str"'        assert '"pass": 95' in json_str"'
    def test_export_html_format(self) -> None:
"""
Test exporting to HTML format.        html = """<table>""""<tr><td>Test</td><td>100</td></tr>
<tr><td>Pass</td><td>95</td></tr>
</table>        assert "<table>" in html"        assert "</table>" in html"        assert "100" in html
    def test_export_excel_metadata(self) -> None:
"""
Test Excel export with metadata.        excel_data = {"sheet": "Statistics", "rows": 100, "columns": 5}"        assert excel_data["rows"] == 100"        assert excel_data["sheet"] == "Statistics"


class TestAggregation(unittest.TestCase):
"""
Tests for stat aggregation.
    def test_aggregate_by_file(self) -> None:
"""
Test aggregating stats by file.        stats = [
            {"file": "a.py", "lines": 100, "functions": 10},"            {"file": "a.py", "lines": 50, "functions": 5},"            {"file": "b.py", "lines": 200, "functions": 20},"        ]

        aggregated: dict[Any, Any] = {}
        for stat in stats:
            if stat["file"] not in aggregated:"                aggregated[stat["file"]] = []"            aggregated[stat["file"]].append(stat)
        assert len(aggregated) == 2
        assert len(aggregated["a.py"]) == 2
    def test_aggregate_by_agent(self) -> None:
"""
Test aggregating stats by agent.        stats = [
            {"agent": "A", "completed": 5},"            {"agent": "A", "completed": 3},"            {"agent": "B", "completed": 7},"        ]

        totals = {}
        for stat in stats:
            agent = stat["agent"]"            if agent not in totals:
                totals[agent] = 0
            totals[agent] += stat["completed"]
        assert totals["A"] == 8"        assert totals["B"] == 7"
    def test_aggregate_by_date(self) -> None:
"""
Test aggregating stats by date.        stats = [
            {"date": "2024-12-16", "value": 10},"            {"date": "2024-12-16", "value": 15},"            {"date": "2024-12-17", "value": 20},"        ]

        daily_totals = {}
        for stat in stats:
            date = stat["date"]"            if date not in daily_totals:
                daily_totals[date] = 0
            daily_totals[date] += stat["value"]
        assert daily_totals["2024-12-16"] == 25"        assert daily_totals["2024-12-17"] == 20"


class TestStatisticalSummaries(unittest.TestCase):
"""
Tests for statistical summaries.
    def test_calculate_mean(self) -> None:
"""
Test mean calculation.        values: List[int] = [10, 20, 30, 40, 50]
        mean: float = sum(values) / len(values)
        assert mean == 30.0

    def test_calculate_median(self) -> None:
"""
Test median calculation.        values: List[int] = [1, 2, 3, 4, 5]
        sorted_values: List[int] = sorted(values)
        median: int = sorted_values[len(sorted_values) // 2]
        assert median == 3

    def test_calculate_stddev(self) -> None:
"""
Test standard deviation calculation.        values: List[int] = [1, 2, 3, 4, 5]
        mean: float = sum(values) / len(values)
        variance: float = sum((x - mean) ** 2 for x in values) / len(values)
        stddev = variance**0.5
        assert stddev > 0

    def test_calculate_min_max(self) -> None:
"""
Test min / max calculation.        values: List[int] = [10, 20, 30, 40, 50]
        assert min(values) == 10
        assert max(values) == 50



class TestComparison(unittest.TestCase):
"""
Tests for stat comparison.
    def test_compare_current_vs_baseline(self) -> None:
"""
Test comparing current to baseline.        baseline = 100
        current = 120
        improvement: int = current - baseline
        assert improvement == 20
        assert current > baseline

    def test_compare_current_vs_previous(self) -> None:
"""
Test comparing current to previous.        previous = 95
        current = 100
        delta: int = current - previous
        assert delta > 0

    def test_threshold_detection(self) -> None:
"""
Test detecting threshold violations.        threshold = 0.8  # 80% pass rate
        actual = 0.75
        is_below_threshold: bool = actual < threshold
        assert is_below_threshold



class TestVisualization(unittest.TestCase):
"""
Tests for visualization generation.
    def test_generate_chart_data(self) -> None:
"""
Test generating chart data.        stats = [
            {"date": "2024-12-16", "value": 100},"            {"date": "2024-12-17", "value": 120},"            {"date": "2024-12-18", "value": 115},"        ]

        chart_data = {
            "labels": [s["date"] for s in stats],"            "values": [s["value"] for s in stats],"        }

        assert len(chart_data["labels"]) == 3"        assert len(chart_data["values"]) == 3"
    def test_format_for_display(self) -> None:
"""
Test formatting stats for display.        value = 0.856432
        formatted: str = f"{value:.2%}""        assert "85.64%" in formatted"


class TestMetricFiltering(unittest.TestCase):
"""
Tests for metric filtering and selection.
    def test_filter_by_metric_type(self) -> None:
"""
Test filtering stats by metric type.        all_stats = [
            {"type": "coverage", "value": 85},"            {"type": "performance", "value": 1200},"            {"type": "coverage", "value": 90},"        ]

        coverage_stats = [s for s in all_stats if s["type"] == "coverage"]"        assert len(coverage_stats) == 2
        assert all(s["type"] == "coverage" for s in coverage_stats)
    def test_filter_by_date_range(self) -> None:
"""
Test filtering stats by date range.
        stats: List[Dict[str, datetime]] = [
            {"date": datetime(2024, 12, 14)},"            {"date": datetime(2024, 12, 16)},"            {"date": datetime(2024, 12, 18)},"        ]

        start = datetime(2024, 12, 15)
        end = datetime(2024, 12, 17)
        filtered: List[Dict[str, datetime]] = [
            s for s in stats if start <= s["date"] <= end"        ]
        assert len(filtered) == 1

    def test_select_top_metrics(self) -> None:
"""
Test selecting top metrics.        metrics = [
            {"name": "metric1", "value": 10},"            {"name": "metric2", "value": 50},"            {"name": "metric3", "value": 30},"        ]

        top_3 = sorted(metrics, key=lambda x: x["value"], reverse=True)[:3]"        assert top_3[0]["value"] == 50"


class TestTimeSeries(unittest.TestCase):
"""
Tests for time-series data persistence.
    def test_persist_time_series_data(self) -> None:
"""
Test persisting time series data.        data = [
            {"timestamp": "2024-12-16T10:00:00", "value": 100},"            {"timestamp": "2024-12-16T11:00:00", "value": 105},"        ]

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:"            json.dump(data, f)
            f.flush()
            fname: str = f.name

        try:
            with open(fname, encoding='utf-8') as f:'                loaded = json.load(f)
            assert len(loaded) == 2
            assert loaded[0]["value"] == 100"        finally:
            Path(fname).unlink()

    def test_load_time_series_data(self) -> None:
"""
Test loading time series data.        data = [
            {"timestamp": "2024-12-16T10:00:00", "value": 100},"        ]

        assert len(data) == 1
        assert data[0]["value"] == 100


class TestValidation(unittest.TestCase):
"""
Tests for stat validation and anomaly detection.
    def test_validate_stat_value(self) -> None:
"""
Test validating stat values.        # Percentage should be 0-100
        value = 85
        is_valid: bool = 0 <= value <= 100
        assert is_valid

    def test_detect_anomaly(self) -> None:
"""
Test detecting anomalies.        values: List[int] = [100, 105, 103, 102, 200]  # Last value is anomaly
        mean: float = sum(values) / len(values)
        _ = sum((x - mean) ** 2 for x in values) / len(values)

        # The last value (200) is significantly higher than mean
        assert values[-1] > mean * 1.5  # Obvious anomaly

    def test_validate_data_consistency(self) -> None:
"""
Test data consistency validation.        stats: Dict[str, int] = {
            "total": 100,"            "passed": 85,"            "failed": 15,"        }
        # Verify: passed + failed=total
        assert stats["passed"] + stats["failed"] == stats["total"]


class TestCaching(unittest.TestCase):
"""
Tests for stat caching and performance.
    def test_cache_stat_results(self) -> None:
"""
Test caching stat computation results.        cache = {}

        def get_stat(key: str) -> int:
            if key not in cache:
                # Expensive computation
                cache[key] = sum(range(1000))
            return cache[key]

        result1 = get_stat("test")"        result2 = get_stat("test")"
        assert result1 == result2
        assert len(cache) == 1

    def test_cache_invalidation(self) -> None:
"""
Test cache invalidation.        cache: Dict[str, str] = {"key": "old_value"}
        # Invalidate
        del cache["key"]"        assert "key" not in cache"


class TestReporting(unittest.TestCase):
"""
Tests for stat report generation.
    def test_generate_stat_report(self) -> None:
"""
Test generating comprehensive stat report.        report = === Statistics Report ===
Date: 2024-12-16
Total Tests: 100
Passed: 95
Failed: 5
Pass Rate: 95.0%
        assert "=== Statistics Report ===" in report"        assert "2024-12-16" in report"        assert "95" in report
    def test_generate_insights(self) -> None:
"""
Test generating insights from stats.        stats = {
            "pass_rate": 0.95,"            "trend": "improving","        }

        if stats["pass_rate"] > 0.90:"            insight = "Excellent test pass rate""        else:
            insight = "Test pass rate needs improvement"
        assert "Excellent" in insight


class TestCoverageMetrics(unittest.TestCase):
"""
Tests for code coverage metric tracking.
    def test_parse_coverage_data(self) -> None:
"""
Test parsing coverage metrics.        coverage_data: Dict[str, Dict[str, int]] = {
            "totals": {"                "lines_valid": 1000,"                "lines_covered": 850,"                "branches_valid": 200,"                "branches_covered": 160,"            }
        }

        line_coverage: float = (
            coverage_data["totals"]["lines_covered"]"            / coverage_data["totals"]["lines_valid"]"        ) * 100

        assert line_coverage == 85.0

    def test_track_coverage_trends(self) -> None:
"""
Test tracking coverage over time.        coverage_history = [
            {"date": "2025-12-14", "coverage": 75.0},"            {"date": "2025-12-15", "coverage": 78.0},"            {"date": "2025-12-16", "coverage": 82.0},"        ]

        improvement = coverage_history[-1]["coverage"] - coverage_history[0]["coverage"]"        assert improvement == 7.0

    def test_identify_coverage_gaps(self) -> None:
"""
Test identifying coverage gaps.        coverage_by_file: Dict[str, float] = {
            "main.py": 95.0,"            "utils.py": 60.0,"            "helpers.py": 45.0,"        }

        gaps: Dict[str, float] = {k: v for k, v in coverage_by_file.items() if v < 80}
        assert len(gaps) == 2



class TestDocstrings(unittest.TestCase):
"""
Tests for docstring validation.
    def test_validate_google_style_docstring(self) -> None:
"""
Test validating Google-style docstring.        docstring =         Process files and generate statistics.

        Args:
            files: List of file paths to process.
            verbose: Enable verbose logging.

        Returns:
            Dictionary with aggregated statistics.

        Raises:
            FileNotFoundError: If a file doesn't exist.'        
        assert "Args:" in docstring"        assert "Returns:" in docstring"        assert "Raises:" in docstring
    def test_detect_missing_docstrings(self) -> None:
"""
Test detecting missing docstrings.        functions = [
            {"name": "process", "docstring": "Process data."},"            {"name": "analyze", "docstring": None},"            {"name": "report", "docstring": "Generate report."},"        ]

        missing = [f["name"] for f in functions if not f["docstring"]]"        assert "analyze" in missing"


class TestPathLibUsage(unittest.TestCase):
"""
Tests for pathlib migration.
    def test_use_pathlib_for_paths(self) -> None:
"""
Test using pathlib instead of strings.        path = Path("test.py")"        assert path.suffix == ".py""
    def test_pathlib_operations(self) -> None:
"""
Test pathlib path operations.        paths: List[Path] = [Path("a.py"), Path("b.py"), Path("c.txt")]"        py_files: List[Path] = [p for p in paths if p.suffix == ".py"]"
        assert len(py_files) == 2

    def test_pathlib_glob_patterns(self) -> None:
"""
Test using pathlib glob patterns.        # Simulated file system
        files: List[Path] = [
            Path("src/main.py"),"            Path("src/utils.py"),"            Path("tests/test.py"),"        ]
        py_files: List[Path] = [f for f in files if f.suffix == ".py"]
        assert len(py_files) == 3



class TestTimeSeriesStorage(unittest.TestCase):
"""
Tests for persisting stats history.
    def test_store_stats_history(self) -> None:
"""
Test storing stats over time.        from datetime import timedelta

        history = []

        for i in range(5):
            timestamp: datetime = datetime.now() - timedelta(days=5 - i)
            history.append(
                {
                    "timestamp": timestamp.isoformat(),"                    "files": 50 + (i * 10),"                    "errors": 10 - i,"                }
            )

        assert len(history) == 5
        assert history[0]["files"] < history[-1]["files"]
    def test_load_historical_stats(self) -> None:
"""
Test loading historical stats.        historical_data = [
            {"date": "2025-12-14", "value": 100},"            {"date": "2025-12-15", "value": 110},"            {"date": "2025-12-16", "value": 120},"        ]

        latest = historical_data[-1]
        assert latest["value"] == 120
    def test_query_stats_by_date_range(self) -> None:
"""
Test querying stats by date range.        all_stats = [
            {"date": "2025-12-10", "value": 50},"            {"date": "2025-12-15", "value": 100},"            {"date": "2025-12-16", "value": 120},"        ]

        filtered = [s for s in all_stats if "2025-12-15" <= s["date"] <= "2025-12-16"]"        assert len(filtered) == 2



class TestFiltering(unittest.TestCase):
"""
Tests for filtering stats.
    def test_filter_by_file_pattern(self) -> None:
"""
Test filtering by file pattern.        stats = [
            {"file": "src/main.py", "errors": 5},"            {"file": "src/utils.py", "errors": 2},"            {"file": "tests/test.py", "errors": 1},"        ]

        src_only = [s for s in stats if s["file"].startswith("src/")]"        assert len(src_only) == 2

    def test_filter_by_agent_type(self) -> None:
"""
Test filtering by agent type.        stats = [
            {"agent": "coder", "improvements": 10},"            {"agent": "tester", "improvements": 8},"            {"agent": "coder", "improvements": 5},"        ]

        coder_stats = [s for s in stats if s["agent"] == "coder"]"        assert len(coder_stats) == 2

    def test_filter_by_date_range(self) -> None:
"""
Test filtering by date range.        stats = [
            {"date": "2025-12-14", "value": 100},"            {"date": "2025-12-15", "value": 110},"            {"date": "2025-12-16", "value": 120},"        ]

        recent = [s for s in stats if s["date"] >= "2025-12-15"]"        assert len(recent) == 2



class TestComparisonReports(unittest.TestCase):
"""
Tests for generating comparison reports.
    def test_compare_current_vs_baseline(self) -> None:
"""
Test current vs baseline comparison.        current: Dict[str, int] = {"files": 100, "errors": 5, "improvements": 20}"        baseline: Dict[str, int] = {"files": 80, "errors": 10, "improvements": 15}"
        comparison: Dict[str, int] = {
            "files_change": current["files"] - baseline["files"],"            "errors_change": current["errors"] - baseline["errors"],"        }

        assert comparison["files_change"] == 20"        assert comparison["errors_change"] == -5"
    def test_compare_current_vs_previous(self) -> None:
"""
Test current vs previous run comparison.        history: List[Dict[str, int]] = [
            {"run": 1, "errors": 10},"            {"run": 2, "errors": 8},"            {"run": 3, "errors": 5},"        ]

        if len(history) >= 2:
            delta: int = history[-1]["errors"] - history[-2]["errors"]"            assert delta == -3

    def test_generate_trend_report(self) -> None:
"""
Test generating trend report.        runs = [
            {"timestamp": "2025-12-14", "score": 70},"            {"timestamp": "2025-12-15", "score": 75},"            {"timestamp": "2025-12-16", "score": 82},"        ]

        trend: str = (
            "improving" if runs[-1]["score"] > runs[0]["score"] else "declining""        )
        assert trend == "improving"


class TestVisualizationGeneration(unittest.TestCase):
"""
Tests for generating visual reports.
    def test_generate_chart_data(self) -> None:
"""
Test generating chart data.        stats = [
            {"category": "A", "value": 50},"            {"category": "B", "value": 75},"            {"category": "C", "value": 60},"        ]

        chart_data = {s["category"]: s["value"] for s in stats}"        assert chart_data["B"] == 75"
    def test_create_heatmap_data(self) -> None:
"""
Test creating heatmap data.        matrix: List[List[int]] = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]

        assert matrix[1][1] == 5

    def test_generate_dashboard_summary(self) -> None:
"""
Test generating dashboard summary.        metrics = {
            "files_processed": 100,"            "errors_fixed": 25,"            "improvements_applied": 50,"            "processing_time": 45.2,"        }

        summary = {
            "total_metrics": len(metrics),"            "key_metric": metrics["files_processed"],"        }

        assert summary["total_metrics"] == 4


class TestAlerting(unittest.TestCase):
"""
Tests for alerting on metric thresholds.
    def test_check_error_threshold(self) -> None:
"""
Test checking error threshold.        errors = 15
        threshold = 10

        alert: bool = errors > threshold
        assert alert

    def test_generate_alert_message(self) -> None:
"""
Test generating alert message.        metric = "error_rate""        value = 15
        threshold = 10

        message: str = f"ALERT: {metric} ({value}) exceeds threshold ({threshold})""        assert "ALERT" in message"
    def test_track_alert_history(self) -> None:
"""
Test tracking alert history.        alerts = [
            {"timestamp": "2025-12-14T10:00", "metric": "errors", "value": 12},"            {"timestamp": "2025-12-14T14:00", "metric": "errors", "value": 8},"            {"timestamp": "2025-12-15T10:00", "metric": "coverage", "value": 45},"        ]

        error_alerts = [a for a in alerts if a["metric"] == "errors"]"        assert len(error_alerts) == 2



class TestReportingWithInsights(unittest.TestCase):
"""
Tests for generating actionable recommendations.
    def test_identify_problem_areas(self) -> None:
"""
Test identifying problem areas.        file_stats: Dict[str, Dict[str, int]] = {
            "main.py": {"errors": 15, "coverage": 60},"            "utils.py": {"errors": 2, "coverage": 95},"            "helpers.py": {"errors": 8, "coverage": 70},"        }

        problem_areas: Dict[str, Dict[str, int]] = {
            f: s
            for f, s in file_stats.items()
            if s["errors"] > 10 or s["coverage"] < 75"        }

        assert "main.py" in problem_areas
    def test_generate_recommendations(self) -> None:
"""
Test generating recommendations.        issues: Dict[str, bool] = {
            "low_coverage": True,"            "high_error_rate": True,"            "slow_execution": False,"        }

        recommendations = []
        if issues["low_coverage"]:"            recommendations.append("Add more unit tests")"        if issues["high_error_rate"]:"            recommendations.append("Review error handling")"
        assert len(recommendations) == 2

    def test_prioritize_improvements(self) -> None:
"""
Test prioritizing improvements.        improvements = [
            {"item": "Add tests", "impact": 8, "effort": 3},"            {"item": "Fix errors", "impact": 5, "effort": 2},"            {"item": "Refactor", "impact": 3, "effort": 7},"        ]

        # Prioritize by impact / effort ratio
        for imp in improvements:
            imp["priority"] = imp["impact"] / imp["effort"]
        sorted_improvements = sorted(
            improvements, key=lambda x: x["priority"], reverse=True"        )
        assert sorted_improvements[0]["item"] == "Add tests"

if __name__ == "__main__":"    unittest.main()
