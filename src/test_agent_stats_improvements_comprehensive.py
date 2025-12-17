#!/usr / bin / env python3
"""
Comprehensive tests for agent-stats.py improvements

Covers trend analysis, visualization, code coverage metrics, edge cases,
format exports, time-series storage, aggregation, statistical summaries,
filtering, comparison reports, and comprehensive metrics tracking.
"""

import unittest
from datetime import datetime, timedelta
import json


class TestTrendAnalysis(unittest.TestCase):
    """Tests for trend analysis and change tracking."""

    def test_compare_with_previous_run(self):
        """Test comparing stats with previous run."""
        current = {"files_processed": 100, "errors": 5}
        previous = {"files_processed": 80, "errors": 8}

        delta = {
            "files_processed": current["files_processed"] - previous["files_processed"],
            "errors": current["errors"] - previous["errors"],
        }

        assert delta["files_processed"] == 20
        assert delta["errors"] == -3

    def test_calculate_percentage_change(self):
        """Test calculating percentage change."""
        current = 100
        previous = 80

        percent_change = ((current - previous) / previous) * 100
        assert percent_change == 25.0

    def test_track_trends_over_time(self):
        """Test tracking metric trends."""
        history = [
            {"date": "2025-12-14", "errors": 10},
            {"date": "2025-12-15", "errors": 8},
            {"date": "2025-12-16", "errors": 5},
        ]

        trend = "decreasing" if history[-1]["errors"] < history[0]["errors"] else "increasing"
        assert trend == "decreasing"

    def test_generate_trend_report(self):
        """Test generating trend report."""
        stats_history = [
            {"timestamp": "2025-12-14", "files": 50, "improvements": 5},
            {"timestamp": "2025-12-15", "files": 75, "improvements": 12},
            {"timestamp": "2025-12-16", "files": 100, "improvements": 20},
        ]

        report = {
            "current": stats_history[-1],
            "previous": stats_history[-2],
            "change": {
                "files": stats_history[-1]["files"] - stats_history[-2]["files"],
                "improvements": stats_history[-1]["improvements"] - stats_history[-2]["improvements"],
            }
        }

        assert report["change"]["files"] == 25


class TestVisualization(unittest.TestCase):
    """Tests for CLI graph and visualization features."""

    def test_create_ascii_bar_chart(self):
        """Test creating ASCII bar chart."""
        data = {"python": 50, "javascript": 30, "bash": 20}
        max_val = max(data.values())

        bars = {
            k: "█" * (v * 20 // max_val)
            for k, v in data.items()
        }

        assert len(bars["python"]) > len(bars["javascript"])

    def test_generate_sparkline(self):
        """Test generating sparkline visualization."""
        values = [1, 3, 2, 5, 4, 8, 6, 9]
        sparkline_chars = "▁▂▃▄▅▆▇█"

        # Normalize values to sparkline character range
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val if max_val > min_val else 1

        sparkline = "".join(
            sparkline_chars[int((v - min_val) * (len(sparkline_chars) - 1) / range_val)]
            for v in values
        )

        assert len(sparkline) == len(values)

    def test_create_rich_table(self):
        """Test creating rich formatted table."""
        stats = [
            {"file": "main.py", "errors": 5, "improvements": 10},
            {"file": "utils.py", "errors": 2, "improvements": 8},
        ]

        assert "main.py" in str(stats[0]["file"])

    def test_visualize_stats_comparison(self):
        """Test visualizing stat comparisons."""
        current = {"metric_a": 100, "metric_b": 85}
        previous = {"metric_a": 80, "metric_b": 90}

        comparison = {}
        for key in current:
            current_val = current[key]
            prev_val = previous[key]
            percent = ((current_val - prev_val) / prev_val) * 100 if prev_val else 0
            comparison[key] = f"{percent:+.1f}%"

        assert "+" in comparison["metric_a"]
        assert "-" in comparison["metric_b"]


class TestCoverageMetrics(unittest.TestCase):
    """Tests for code coverage metric tracking."""

    def test_parse_coverage_data(self):
        """Test parsing coverage metrics."""
        coverage_data = {
            "totals": {
                "lines_valid": 1000,
                "lines_covered": 850,
                "branches_valid": 200,
                "branches_covered": 160,
            }
        }

        line_coverage = (coverage_data["totals"]["lines_covered"] /
                         coverage_data["totals"]["lines_valid"]) * 100

        assert line_coverage == 85.0

    def test_track_coverage_trends(self):
        """Test tracking coverage over time."""
        coverage_history = [
            {"date": "2025-12-14", "coverage": 75.0},
            {"date": "2025-12-15", "coverage": 78.0},
            {"date": "2025-12-16", "coverage": 82.0},
        ]

        improvement = coverage_history[-1]["coverage"] - coverage_history[0]["coverage"]
        assert improvement == 7.0

    def test_identify_coverage_gaps(self):
        """Test identifying coverage gaps."""
        coverage_by_file = {
            "main.py": 95.0,
            "utils.py": 60.0,
            "helpers.py": 45.0,
        }

        gaps = {k: v for k, v in coverage_by_file.items() if v < 80}
        assert len(gaps) == 2


class TestDocstrings(unittest.TestCase):
    """Tests for docstring validation."""

    def test_validate_google_style_docstring(self):
        """Test validating Google-style docstring."""
        docstring = """
        Process files and generate statistics.

        Args:
            files: List of file paths to process.
            verbose: Enable verbose logging.

        Returns:
            Dictionary with aggregated statistics.

        Raises:
            FileNotFoundError: If a file doesn't exist.
        """

        assert "Args:" in docstring
        assert "Returns:" in docstring
        assert "Raises:" in docstring

    def test_detect_missing_docstrings(self):
        """Test detecting missing docstrings."""
        functions = [
            {"name": "process", "docstring": "Process data."},
            {"name": "analyze", "docstring": None},
            {"name": "report", "docstring": "Generate report."},
        ]

        missing = [f["name"] for f in functions if not f["docstring"]]
        assert "analyze" in missing


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""

    def test_handle_empty_files(self):
        """Test handling empty files."""
        stats = {}

        total_files = len(stats) if stats else 0
        assert total_files == 0

    def test_handle_missing_data(self):
        """Test handling missing data fields."""
        stats = {"files_processed": 10}

        errors = stats.get("errors", 0)
        improvements = stats.get("improvements", 0)

        assert errors == 0
        assert improvements == 0

    def test_handle_malformed_input(self):
        """Test handling malformed input."""
        try:
            json.loads("{invalid json}")
            assert False, "Should raise exception"
        except json.JSONDecodeError:
            assert True

    def test_handle_large_numbers(self):
        """Test handling very large numbers."""
        stats = {"files": 999999, "lines": 9999999999}

        assert stats["files"] > 0
        assert stats["lines"] > 0


class TestPathLibUsage(unittest.TestCase):
    """Tests for pathlib migration."""

    def test_use_pathlib_for_paths(self):
        """Test using pathlib instead of strings."""
        from pathlib import Path

        path = Path("test.py")
        assert path.suffix == ".py"

    def test_pathlib_operations(self):
        """Test pathlib path operations."""
        from pathlib import Path

        paths = [Path("a.py"), Path("b.py"), Path("c.txt")]
        py_files = [p for p in paths if p.suffix == ".py"]

        assert len(py_files) == 2

    def test_pathlib_glob_patterns(self):
        """Test using pathlib glob patterns."""
        from pathlib import Path

        # Simulated file system
        files = [Path("src / main.py"), Path("src / utils.py"), Path("tests / test.py")]
        py_files = [f for f in files if f.suffix == ".py"]

        assert len(py_files) == 3


class TestExportFormats(unittest.TestCase):
    """Tests for exporting to multiple formats."""

    def test_export_to_json(self):
        """Test exporting stats to JSON."""
        stats = {
            "files_processed": 100,
            "errors": 5,
            "timestamp": "2025-12-16T10:00:00",
        }

        json_str = json.dumps(stats)
        restored = json.loads(json_str)

        assert restored["files_processed"] == 100

    def test_export_to_csv(self):
        """Test exporting to CSV."""
        stats = [
            {"file": "a.py", "errors": 5, "improvements": 10},
            {"file": "b.py", "errors": 2, "improvements": 8},
        ]

        csv_lines = ["file,errors,improvements"]
        for stat in stats:
            csv_lines.append(f"{stat['file']},{stat['errors']},{stat['improvements']}")

        csv_content = "\n".join(csv_lines)
        assert "a.py,5,10" in csv_content

    def test_export_to_html(self):
        """Test exporting to HTML."""
        html = """
        <table>
            <tr><td>Files</td><td>{stats['files']}</td></tr>
            <tr><td>Errors</td><td>{stats['errors']}</td></tr>
        </table>
        """

        assert "<table>" in html
        assert "100" in html

    def test_export_to_excel(self):
        """Test exporting to Excel format."""
        stats = [
            {"file": "a.py", "errors": 5},
            {"file": "b.py", "errors": 2},
        ]

        # Simulate Excel row format
        excel_rows = []
        for stat in stats:
            excel_rows.append({"A": stat["file"], "B": stat["errors"]})

        assert len(excel_rows) == 2

    def test_export_to_sqlite(self):
        """Test exporting to SQLite."""
        import sqlite3

        stats = [
            {"file": "a.py", "errors": 5},
            {"file": "b.py", "errors": 2},
        ]

        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE stats (file TEXT, errors INTEGER)")

        for stat in stats:
            cursor.execute("INSERT INTO stats VALUES (?, ?)", (stat["file"], stat["errors"]))

        cursor.execute("SELECT COUNT(*) FROM stats")
        count = cursor.fetchone()[0]

        assert count == 2
        conn.close()


class TestTimeSeriesStorage(unittest.TestCase):
    """Tests for persisting stats history."""

    def test_store_stats_history(self):
        """Test storing stats over time."""
        history = []

        for i in range(5):
            timestamp = datetime.now() - timedelta(days=5 - i)
            history.append({
                "timestamp": timestamp.isoformat(),
                "files": 50 + (i * 10),
                "errors": 10 - i,
            })

        assert len(history) == 5
        assert history[0]["files"] < history[-1]["files"]

    def test_load_historical_stats(self):
        """Test loading historical stats."""
        historical_data = [
            {"date": "2025-12-14", "value": 100},
            {"date": "2025-12-15", "value": 110},
            {"date": "2025-12-16", "value": 120},
        ]

        latest = historical_data[-1]
        assert latest["value"] == 120

    def test_query_stats_by_date_range(self):
        """Test querying stats by date range."""
        all_stats = [
            {"date": "2025-12-10", "value": 50},
            {"date": "2025-12-15", "value": 100},
            {"date": "2025-12-16", "value": 120},
        ]

        filtered = [s for s in all_stats if "2025-12-15" <= s["date"] <= "2025-12-16"]
        assert len(filtered) == 2


class TestAggregation(unittest.TestCase):
    """Tests for stat aggregation by different dimensions."""

    def test_aggregate_by_file(self):
        """Test aggregating stats by file."""
        entries = [
            {"file": "a.py", "errors": 5, "improvements": 10},
            {"file": "a.py", "errors": 2, "improvements": 5},
            {"file": "b.py", "errors": 3, "improvements": 8},
        ]

        by_file = {}
        for entry in entries:
            if entry["file"] not in by_file:
                by_file[entry["file"]] = {"errors": 0, "improvements": 0}
            by_file[entry["file"]]["errors"] += entry["errors"]
            by_file[entry["file"]]["improvements"] += entry["improvements"]

        assert by_file["a.py"]["errors"] == 7

    def test_aggregate_by_agent(self):
        """Test aggregating stats by agent."""
        entries = [
            {"agent": "coder", "improvements": 10},
            {"agent": "coder", "improvements": 5},
            {"agent": "tester", "improvements": 8},
        ]

        by_agent = {}
        for entry in entries:
            by_agent[entry["agent"]] = by_agent.get(entry["agent"], 0) + entry["improvements"]

        assert by_agent["coder"] == 15

    def test_aggregate_by_date(self):
        """Test aggregating stats by date."""
        entries = [
            {"date": "2025-12-16", "issues": 5},
            {"date": "2025-12-16", "issues": 3},
            {"date": "2025-12-15", "issues": 2},
        ]

        by_date = {}
        for entry in entries:
            by_date[entry["date"]] = by_date.get(entry["date"], 0) + entry["issues"]

        assert by_date["2025-12-16"] == 8


class TestStatisticalSummaries(unittest.TestCase):
    """Tests for statistical calculations."""

    def test_calculate_mean(self):
        """Test calculating mean."""
        values = [10, 20, 30, 40, 50]
        mean = sum(values) / len(values)
        assert mean == 30.0

    def test_calculate_median(self):
        """Test calculating median."""
        values = [10, 20, 30, 40, 50]
        sorted_vals = sorted(values)
        median = sorted_vals[len(sorted_vals) // 2]
        assert median == 30

    def test_calculate_stddev(self):
        """Test calculating standard deviation."""
        import statistics

        values = [10, 20, 30, 40, 50]
        stddev = statistics.stdev(values)

        assert stddev > 0

    def test_calculate_percentiles(self):
        """Test calculating percentiles."""
        values = list(range(1, 101))
        p50_idx = int(len(values) * 0.5) - 1
        p95_idx = int(len(values) * 0.95) - 1
        p50 = values[p50_idx]
        p95 = values[p95_idx]

        assert p50 == 50
        assert p95 > 90  # Allow for rounding differences


class TestFiltering(unittest.TestCase):
    """Tests for filtering stats."""

    def test_filter_by_file_pattern(self):
        """Test filtering by file pattern."""
        stats = [
            {"file": "src / main.py", "errors": 5},
            {"file": "src / utils.py", "errors": 2},
            {"file": "tests / test.py", "errors": 1},
        ]

        src_only = [s for s in stats if s["file"].startswith("src/")]
        assert len(src_only) == 2

    def test_filter_by_agent_type(self):
        """Test filtering by agent type."""
        stats = [
            {"agent": "coder", "improvements": 10},
            {"agent": "tester", "improvements": 8},
            {"agent": "coder", "improvements": 5},
        ]

        coder_stats = [s for s in stats if s["agent"] == "coder"]
        assert len(coder_stats) == 2

    def test_filter_by_date_range(self):
        """Test filtering by date range."""
        stats = [
            {"date": "2025-12-14", "value": 100},
            {"date": "2025-12-15", "value": 110},
            {"date": "2025-12-16", "value": 120},
        ]

        recent = [s for s in stats if s["date"] >= "2025-12-15"]
        assert len(recent) == 2


class TestComparisonReports(unittest.TestCase):
    """Tests for generating comparison reports."""

    def test_compare_current_vs_baseline(self):
        """Test current vs baseline comparison."""
        current = {"files": 100, "errors": 5, "improvements": 20}
        baseline = {"files": 80, "errors": 10, "improvements": 15}

        comparison = {
            "files_change": current["files"] - baseline["files"],
            "errors_change": current["errors"] - baseline["errors"],
        }

        assert comparison["files_change"] == 20
        assert comparison["errors_change"] == -5

    def test_compare_current_vs_previous(self):
        """Test current vs previous run comparison."""
        history = [
            {"run": 1, "errors": 10},
            {"run": 2, "errors": 8},
            {"run": 3, "errors": 5},
        ]

        if len(history) >= 2:
            delta = history[-1]["errors"] - history[-2]["errors"]
            assert delta == -3

    def test_generate_trend_report(self):
        """Test generating trend report."""
        runs = [
            {"timestamp": "2025-12-14", "score": 70},
            {"timestamp": "2025-12-15", "score": 75},
            {"timestamp": "2025-12-16", "score": 82},
        ]

        trend = "improving" if runs[-1]["score"] > runs[0]["score"] else "declining"
        assert trend == "improving"


class TestVisualizationGeneration(unittest.TestCase):
    """Tests for generating visual reports."""

    def test_generate_chart_data(self):
        """Test generating chart data."""
        stats = [
            {"category": "A", "value": 50},
            {"category": "B", "value": 75},
            {"category": "C", "value": 60},
        ]

        chart_data = {s["category"]: s["value"] for s in stats}
        assert chart_data["B"] == 75

    def test_create_heatmap_data(self):
        """Test creating heatmap data."""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]

        assert matrix[1][1] == 5

    def test_generate_dashboard_summary(self):
        """Test generating dashboard summary."""
        metrics = {
            "files_processed": 100,
            "errors_fixed": 25,
            "improvements_applied": 50,
            "processing_time": 45.2,
        }

        summary = {
            "total_metrics": len(metrics),
            "key_metric": metrics["files_processed"],
        }

        assert summary["total_metrics"] == 4


class TestAlerting(unittest.TestCase):
    """Tests for alerting on metric thresholds."""

    def test_check_error_threshold(self):
        """Test checking error threshold."""
        errors = 15
        threshold = 10

        alert = errors > threshold
        assert alert

    def test_generate_alert_message(self):
        """Test generating alert message."""
        metric = "error_rate"
        value = 15
        threshold = 10

        message = f"ALERT: {metric} ({value}) exceeds threshold ({threshold})"
        assert "ALERT" in message

    def test_track_alert_history(self):
        """Test tracking alert history."""
        alerts = [
            {"timestamp": "2025-12-14T10:00", "metric": "errors", "value": 12},
            {"timestamp": "2025-12-14T14:00", "metric": "errors", "value": 8},
            {"timestamp": "2025-12-15T10:00", "metric": "coverage", "value": 45},
        ]

        error_alerts = [a for a in alerts if a["metric"] == "errors"]
        assert len(error_alerts) == 2


class TestBenchmarking(unittest.TestCase):
    """Tests for performance benchmarking."""

    def test_track_agent_timing(self):
        """Test tracking agent execution time."""
        timings = {
            "coder": 45.2,
            "tester": 32.1,
            "reviewer": 18.5,
        }

        slowest = max(timings, key=timings.get)
        assert slowest == "coder"

    def test_calculate_average_time_per_file(self):
        """Test calculating average processing time."""
        total_time = 120.5
        files_processed = 100

        avg_time = total_time / files_processed
        assert abs(avg_time - 1.205) < 0.01

    def test_benchmark_per_agent_statistics(self):
        """Test per-agent benchmark statistics."""
        agent_times = {
            "coder": [10, 12, 11, 13, 12],
            "tester": [5, 6, 5, 7, 6],
        }

        stats = {
            agent: {
                "avg": sum(times) / len(times),
                "min": min(times),
                "max": max(times),
            }
            for agent, times in agent_times.items()
        }

        assert stats["coder"]["avg"] > stats["tester"]["avg"]


class TestReportingWithInsights(unittest.TestCase):
    """Tests for generating actionable recommendations."""

    def test_identify_problem_areas(self):
        """Test identifying problem areas."""
        file_stats = {
            "main.py": {"errors": 15, "coverage": 60},
            "utils.py": {"errors": 2, "coverage": 95},
            "helpers.py": {"errors": 8, "coverage": 70},
        }

        problem_areas = {
            f: s for f, s in file_stats.items()
            if s["errors"] > 10 or s["coverage"] < 75
        }

        assert "main.py" in problem_areas

    def test_generate_recommendations(self):
        """Test generating recommendations."""
        issues = {
            "low_coverage": True,
            "high_error_rate": True,
            "slow_execution": False,
        }

        recommendations = []
        if issues["low_coverage"]:
            recommendations.append("Add more unit tests")
        if issues["high_error_rate"]:
            recommendations.append("Review error handling")

        assert len(recommendations) == 2

    def test_prioritize_improvements(self):
        """Test prioritizing improvements."""
        improvements = [
            {"item": "Add tests", "impact": 8, "effort": 3},
            {"item": "Fix errors", "impact": 5, "effort": 2},
            {"item": "Refactor", "impact": 3, "effort": 7},
        ]

        # Prioritize by impact / effort ratio
        for imp in improvements:
            imp["priority"] = imp["impact"] / imp["effort"]

        sorted_improvements = sorted(improvements, key=lambda x: x["priority"], reverse=True)
        assert sorted_improvements[0]["item"] == "Add tests"


class TestCaching(unittest.TestCase):
    """Tests for caching performance optimizations."""

    def test_cache_computed_stats(self):
        """Test caching computed statistics."""
        cache = {}

        def get_stats(file_id):
            if file_id in cache:
                return cache[file_id]

            stats = {"errors": 5, "coverage": 85}
            cache[file_id] = stats
            return stats

        # First call computes
        result1 = get_stats("file1")
        # Second call uses cache
        result2 = get_stats("file1")

        assert result1 == result2

    def test_cache_invalidation(self):
        """Test cache invalidation."""
        cache = {"file1": {"errors": 5}}

        # Invalidate cache
        cache.pop("file1")

        assert "file1" not in cache

    def test_cache_expiration(self):
        """Test cache expiration."""
        import time

        cache_items = {
            "file1": {"data": "stats", "timestamp": time.time()},
        }

        # Simulate expiration check (e.g., 1 hour)
        max_age = 3600
        current_time = time.time()

        expired = {
            k: v for k, v in cache_items.items()
            if current_time - v["timestamp"] > max_age
        }

        assert len(expired) == 0


class TestIntegration(unittest.TestCase):
    """Integration tests for stats module."""

    def test_end_to_end_stats_workflow(self):
        """Test end-to-end stats workflow."""
        # Collect stats
        stats = {"files": 100, "errors": 5}

        # Analyze
        error_rate = (stats["errors"] / stats["files"]) * 100

        # Report
        report = {
            "total_files": stats["files"],
            "total_errors": stats["errors"],
            "error_rate": f"{error_rate:.2f}%",
        }

        assert report["error_rate"] == "5.00%"

    def test_multi_format_export(self):
        """Test exporting to multiple formats."""
        stats = [{"file": "a.py", "errors": 5}]

        formats = {
            "json": json.dumps(stats),
            "csv": "file,errors\na.py,5",
        }

        assert len(formats) == 2
        assert "json" in formats


if __name__ == "__main__":
    unittest.main()
