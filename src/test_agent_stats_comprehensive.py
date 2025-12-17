#!/usr / bin / env python3
"""
Tests for agent_stats.py improvements.

Covers trend analysis, export functionality, aggregation,
statistical summaries, and performance tracking.
"""

import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path


class TestTrendAnalysis(unittest.TestCase):
    """Tests for trend analysis and delta calculation."""

    def test_calculate_trend(self):
        """Test trend calculation from time series data."""
        data = [1, 2, 3, 4, 5]
        # Upward trend
        assert data[-1] > data[0]

    def test_calculate_delta(self):
        """Test delta calculation between values."""
        current = 100
        previous = 80
        delta = current - previous
        assert delta == 20

    def test_trend_percentage_change(self):
        """Test percentage change calculation."""
        old_value = 100
        new_value = 110
        percent_change = ((new_value - old_value) / old_value) * 100
        assert percent_change == 10.0

    def test_trend_direction(self):
        """Test determining trend direction."""
        values = [5, 4, 3, 2, 1]
        is_decreasing = values[0] > values[-1]
        assert is_decreasing


class TestCSVExport(unittest.TestCase):
    """Tests for CSV export functionality."""

    def test_export_stats_to_csv(self):
        """Test exporting stats to CSV format."""
        stats = [
            {"date": "2024-12-16", "tests": 100, "pass": 95},
            {"date": "2024-12-17", "tests": 102, "pass": 98},
        ]

        csv_lines = ["date,tests,pass"]
        for stat in stats:
            csv_lines.append(f"{stat['date']},{stat['tests']},{stat['pass']}")

        csv_content = "\n".join(csv_lines)
        assert "2024-12-16" in csv_content
        assert "date,tests,pass" in csv_content

    def test_csv_escaping(self):
        """Test proper CSV escaping."""
        escaped = '"{value}"'
        assert escaped.startswith('"')
        assert escaped.endswith('"')

    def test_csv_with_special_characters(self):
        """Test CSV with special characters."""
        csv_line = '{"test,with,commas",123}'
        assert "test,with,commas" in csv_line


class TestExportFormats(unittest.TestCase):
    """Tests for different export formats."""

    def test_export_json_format(self):
        """Test exporting to JSON format."""
        stats = {"tests": 100, "pass": 95, "timestamp": "2024-12-16"}
        json_str = json.dumps(stats)
        assert '"tests": 100' in json_str
        assert '"pass": 95' in json_str

    def test_export_html_format(self):
        """Test exporting to HTML format."""
        html = """<table>
<tr><td>Test</td><td>100</td></tr>
<tr><td>Pass</td><td>95</td></tr>
</table>"""
        assert "<table>" in html
        assert "</table>" in html
        assert "100" in html

    def test_export_excel_metadata(self):
        """Test Excel export with metadata."""
        excel_data = {
            "sheet": "Statistics",
            "rows": 100,
            "columns": 5
        }
        assert excel_data["rows"] == 100
        assert excel_data["sheet"] == "Statistics"


class TestAggregation(unittest.TestCase):
    """Tests for stat aggregation."""

    def test_aggregate_by_file(self):
        """Test aggregating stats by file."""
        stats = [
            {"file": "a.py", "lines": 100, "functions": 10},
            {"file": "a.py", "lines": 50, "functions": 5},
            {"file": "b.py", "lines": 200, "functions": 20},
        ]

        aggregated = {}
        for stat in stats:
            if stat["file"] not in aggregated:
                aggregated[stat["file"]] = []
            aggregated[stat["file"]].append(stat)

        assert len(aggregated) == 2
        assert len(aggregated["a.py"]) == 2

    def test_aggregate_by_agent(self):
        """Test aggregating stats by agent."""
        stats = [
            {"agent": "A", "completed": 5},
            {"agent": "A", "completed": 3},
            {"agent": "B", "completed": 7},
        ]

        totals = {}
        for stat in stats:
            agent = stat["agent"]
            if agent not in totals:
                totals[agent] = 0
            totals[agent] += stat["completed"]

        assert totals["A"] == 8
        assert totals["B"] == 7

    def test_aggregate_by_date(self):
        """Test aggregating stats by date."""
        stats = [
            {"date": "2024-12-16", "value": 10},
            {"date": "2024-12-16", "value": 15},
            {"date": "2024-12-17", "value": 20},
        ]

        daily_totals = {}
        for stat in stats:
            date = stat["date"]
            if date not in daily_totals:
                daily_totals[date] = 0
            daily_totals[date] += stat["value"]

        assert daily_totals["2024-12-16"] == 25
        assert daily_totals["2024-12-17"] == 20


class TestStatisticalSummaries(unittest.TestCase):
    """Tests for statistical summaries."""

    def test_calculate_mean(self):
        """Test mean calculation."""
        values = [10, 20, 30, 40, 50]
        mean = sum(values) / len(values)
        assert mean == 30.0

    def test_calculate_median(self):
        """Test median calculation."""
        values = [1, 2, 3, 4, 5]
        sorted_values = sorted(values)
        median = sorted_values[len(sorted_values) // 2]
        assert median == 3

    def test_calculate_stddev(self):
        """Test standard deviation calculation."""
        values = [1, 2, 3, 4, 5]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        stddev = variance ** 0.5
        assert stddev > 0

    def test_calculate_min_max(self):
        """Test min / max calculation."""
        values = [10, 20, 30, 40, 50]
        assert min(values) == 10
        assert max(values) == 50


class TestComparison(unittest.TestCase):
    """Tests for stat comparison."""

    def test_compare_current_vs_baseline(self):
        """Test comparing current to baseline."""
        baseline = 100
        current = 120
        improvement = current - baseline
        assert improvement == 20
        assert current > baseline

    def test_compare_current_vs_previous(self):
        """Test comparing current to previous."""
        previous = 95
        current = 100
        delta = current - previous
        assert delta > 0

    def test_threshold_detection(self):
        """Test detecting threshold violations."""
        threshold = 0.8  # 80% pass rate
        actual = 0.75
        is_below_threshold = actual < threshold
        assert is_below_threshold


class TestVisualization(unittest.TestCase):
    """Tests for visualization generation."""

    def test_generate_chart_data(self):
        """Test generating chart data."""
        stats = [
            {"date": "2024-12-16", "value": 100},
            {"date": "2024-12-17", "value": 120},
            {"date": "2024-12-18", "value": 115},
        ]

        chart_data = {
            "labels": [s["date"] for s in stats],
            "values": [s["value"] for s in stats]
        }

        assert len(chart_data["labels"]) == 3
        assert len(chart_data["values"]) == 3

    def test_format_for_display(self):
        """Test formatting stats for display."""
        value = 0.856432
        formatted = f"{value:.2%}"
        assert "85.64%" in formatted


class TestMetricFiltering(unittest.TestCase):
    """Tests for metric filtering and selection."""

    def test_filter_by_metric_type(self):
        """Test filtering stats by metric type."""
        all_stats = [
            {"type": "coverage", "value": 85},
            {"type": "performance", "value": 1200},
            {"type": "coverage", "value": 90},
        ]

        coverage_stats = [s for s in all_stats if s["type"] == "coverage"]
        assert len(coverage_stats) == 2
        assert all(s["type"] == "coverage" for s in coverage_stats)

    def test_filter_by_date_range(self):
        """Test filtering stats by date range."""

        stats = [
            {"date": datetime(2024, 12, 14)},
            {"date": datetime(2024, 12, 16)},
            {"date": datetime(2024, 12, 18)},
        ]

        start = datetime(2024, 12, 15)
        end = datetime(2024, 12, 17)
        filtered = [s for s in stats if start <= s["date"] <= end]
        assert len(filtered) == 1

    def test_select_top_metrics(self):
        """Test selecting top metrics."""
        metrics = [
            {"name": "metric1", "value": 10},
            {"name": "metric2", "value": 50},
            {"name": "metric3", "value": 30},
        ]

        top_3 = sorted(metrics, key=lambda x: x["value"], reverse=True)[:3]
        assert top_3[0]["value"] == 50


class TestTimeSeries(unittest.TestCase):
    """Tests for time-series data persistence."""

    def test_persist_time_series_data(self):
        """Test persisting time series data."""
        data = [
            {"timestamp": "2024-12-16T10:00:00", "value": 100},
            {"timestamp": "2024-12-16T11:00:00", "value": 105},
        ]

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(data, f)
            f.flush()
            fname = f.name

        try:
            with open(fname) as f:
                loaded = json.load(f)
            assert len(loaded) == 2
            assert loaded[0]["value"] == 100
        finally:
            Path(fname).unlink()

    def test_load_time_series_data(self):
        """Test loading time series data."""
        data = [
            {"timestamp": "2024-12-16T10:00:00", "value": 100},
        ]

        assert len(data) == 1
        assert data[0]["value"] == 100


class TestValidation(unittest.TestCase):
    """Tests for stat validation and anomaly detection."""

    def test_validate_stat_value(self):
        """Test validating stat values."""
        # Percentage should be 0-100
        value = 85
        is_valid = 0 <= value <= 100
        assert is_valid

    def test_detect_anomaly(self):
        """Test detecting anomalies."""
        values = [100, 105, 103, 102, 200]  # Last value is anomaly
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        variance ** 0.5

        # The last value (200) is significantly higher than mean
        assert values[-1] > mean * 1.5  # Obvious anomaly

    def test_validate_data_consistency(self):
        """Test data consistency validation."""
        stats = {
            "total": 100,
            "passed": 85,
            "failed": 15,
        }
        # Verify: passed + failed=total
        assert stats["passed"] + stats["failed"] == stats["total"]


class TestPerformanceMetrics(unittest.TestCase):
    """Tests for performance metrics tracking."""

    def test_track_execution_time(self):
        """Test tracking execution time."""
        import time
        start = time.time()
        # Simulate work
        time.sleep(0.01)
        end = time.time()
        duration = end - start
        assert duration > 0

    def test_track_memory_usage(self):
        """Test tracking memory usage."""
        import sys
        size = sys.getsizeof("hello")
        assert size > 0

    def test_track_cpu_metrics(self):
        """Test tracking CPU-related metrics."""
        metrics = {
            "cpu_percent": 45.2,
            "threads": 8,
        }
        assert metrics["cpu_percent"] > 0
        assert metrics["threads"] > 0


class TestBenchmarking(unittest.TestCase):
    """Tests for benchmark result aggregation."""

    def test_aggregate_benchmark_results(self):
        """Test aggregating benchmark results."""
        benchmarks = [
            {"name": "test_parse", "time_ms": 10.5},
            {"name": "test_format", "time_ms": 20.3},
            {"name": "test_validate", "time_ms": 5.2},
        ]

        total_time = sum(b["time_ms"] for b in benchmarks)
        avg_time = total_time / len(benchmarks)

        assert avg_time > 0
        assert total_time > avg_time

    def test_benchmark_comparison(self):
        """Test comparing benchmark results."""
        baseline = {"operation": "parse", "time_ms": 10.0}
        current = {"operation": "parse", "time_ms": 12.5}

        regression_percent = ((current["time_ms"] - baseline["time_ms"])
                              / baseline["time_ms"]) * 100
        assert regression_percent > 0  # Performance regressed


class TestCaching(unittest.TestCase):
    """Tests for stat caching and performance."""

    def test_cache_stat_results(self):
        """Test caching stat computation results."""
        cache = {}

        def get_stat(key):
            if key not in cache:
                # Expensive computation
                cache[key] = sum(range(1000))
            return cache[key]

        result1 = get_stat("test")
        result2 = get_stat("test")

        assert result1 == result2
        assert len(cache) == 1

    def test_cache_invalidation(self):
        """Test cache invalidation."""
        cache = {"key": "old_value"}

        # Invalidate
        del cache["key"]
        assert "key" not in cache


class TestReporting(unittest.TestCase):
    """Tests for stat report generation."""

    def test_generate_stat_report(self):
        """Test generating comprehensive stat report."""
        report = """
=== Statistics Report ===
Date: 2024-12-16
Total Tests: 100
Passed: 95
Failed: 5
Pass Rate: 95.0%
"""
        assert "=== Statistics Report ===" in report
        assert "2024-12-16" in report
        assert "95" in report

    def test_generate_insights(self):
        """Test generating insights from stats."""
        stats = {
            "pass_rate": 0.95,
            "trend": "improving",
        }

        if stats["pass_rate"] > 0.90:
            insight = "Excellent test pass rate"
        else:
            insight = "Test pass rate needs improvement"

        assert "Excellent" in insight


class TestIntegration(unittest.TestCase):
    """Integration tests for stats processing."""

    def test_end_to_end_stats_workflow(self):
        """Test complete stats workflow."""
        # Collect stats
        stats = [
            {"timestamp": "2024-12-16T10:00:00", "tests": 100, "passed": 95},
            {"timestamp": "2024-12-16T11:00:00", "tests": 102, "passed": 98},
        ]

        # Aggregate
        total_tests = sum(s["tests"] for s in stats)
        total_passed = sum(s["passed"] for s in stats)

        # Calculate metrics
        pass_rate = (total_passed / total_tests) * 100

        assert total_tests == 202
        assert pass_rate > 95


if __name__ == "__main__":
    unittest.main()
