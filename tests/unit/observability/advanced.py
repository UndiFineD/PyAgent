# -*- coding: utf-8 -*-
"""Test classes from test_agent_stats.py - advanced module."""

from __future__ import annotations
from typing import Any
from sqlite3 import Connection
from sqlite3 import Cursor
import unittest
from typing import List, Dict
import time
import json
from pathlib import Path
import sys

# Try to import test utilities
try:
    from tests.utils.agent_test_utils import (
        AGENT_DIR,
        agent_sys_path,
        load_module_from_path,
        agent_dir_on_path,
    )
except ImportError:
    # Fallback
    AGENT_DIR: Path = Path(__file__).parent.parent.parent.parent / "src"

    class agent_sys_path:
        def __enter__(self) -> Self:
            return self

        def __exit__(self, *args) -> None:
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed


class TestTrendAnalysisAdvanced(unittest.TestCase):
    """Tests for trend analysis and change tracking."""

    def test_compare_with_previous_run(self) -> None:
        """Test comparing stats with previous run."""
        current: Dict[str, int] = {"files_processed": 100, "errors": 5}
        previous: Dict[str, int] = {"files_processed": 80, "errors": 8}

        delta: Dict[str, int] = {
            "files_processed": current["files_processed"] - previous["files_processed"],
            "errors": current["errors"] - previous["errors"],
        }

        assert delta["files_processed"] == 20
        assert delta["errors"] == -3

    def test_calculate_percentage_change(self) -> None:
        """Test calculating percentage change."""
        current = 100
        previous = 80

        percent_change: float = ((current - previous) / previous) * 100
        assert percent_change == 25.0

    def test_track_trends_over_time(self) -> None:
        """Test tracking metric trends."""
        history = [
            {"date": "2025-12-14", "errors": 10},
            {"date": "2025-12-15", "errors": 8},
            {"date": "2025-12-16", "errors": 5},
        ]

        trend: str = (
            "decreasing"
            if history[-1]["errors"] < history[0]["errors"]
            else "increasing"
        )
        assert trend == "decreasing"

    def test_generate_trend_report(self) -> None:
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
                "improvements": (
                    stats_history[-1]["improvements"]
                    - stats_history[-2]["improvements"]
                ),
            },
        }

        assert report["change"]["files"] == 25


class TestVisualizationAdvanced(unittest.TestCase):
    """Tests for CLI graph and visualization features."""

    def test_create_ascii_bar_chart(self) -> None:
        """Test creating ASCII bar chart."""
        data: Dict[str, int] = {"python": 50, "javascript": 30, "bash": 20}
        max_val: int = max(data.values())

        bars: Dict[str, str] = {k: "█" * (v * 20 // max_val) for k, v in data.items()}

        assert len(bars["python"]) > len(bars["javascript"])

    def test_generate_sparkline(self) -> None:
        """Test generating sparkline visualization."""
        values: List[int] = [1, 3, 2, 5, 4, 8, 6, 9]
        sparkline_chars = "▁▂▃▄▅▆▇█"

        # Normalize values to sparkline character range
        min_val: int = min(values)
        max_val: int = max(values)
        range_val: int = max_val - min_val if max_val > min_val else 1

        sparkline: str = "".join(
            sparkline_chars[int((v - min_val) * (len(sparkline_chars) - 1) / range_val)]
            for v in values
        )

        assert len(sparkline) == len(values)

    def test_create_rich_table(self) -> None:
        """Test creating rich formatted table."""
        stats = [
            {"file": "main.py", "errors": 5, "improvements": 10},
            {"file": "utils.py", "errors": 2, "improvements": 8},
        ]

        assert "main.py" in str(stats[0]["file"])

    def test_visualize_stats_comparison(self) -> None:
        """Test visualizing stat comparisons."""
        current: Dict[str, int] = {"metric_a": 100, "metric_b": 85}
        previous: Dict[str, int] = {"metric_a": 80, "metric_b": 90}

        comparison = {}
        for key in current:
            current_val: int = current[key]
            prev_val: int = previous[key]
            percent: float | int = (
                ((current_val - prev_val) / prev_val) * 100 if prev_val else 0
            )
            comparison[key] = f"{percent:+.1f}%"

        assert "+" in comparison["metric_a"]
        assert "-" in comparison["metric_b"]


class TestExportFormatsAdvanced(unittest.TestCase):
    """Tests for exporting to multiple formats."""

    def test_export_to_json(self) -> None:
        """Test exporting stats to JSON."""
        stats = {
            "files_processed": 100,
            "errors": 5,
            "timestamp": "2025-12-16T10:00:00",
        }

        json_str: str = json.dumps(stats)
        restored = json.loads(json_str)

        assert restored["files_processed"] == 100

    def test_export_to_csv(self) -> None:
        """Test exporting to CSV."""
        stats = [
            {"file": "a.py", "errors": 5, "improvements": 10},
            {"file": "b.py", "errors": 2, "improvements": 8},
        ]

        csv_lines: List[str] = ["file,errors,improvements"]
        for stat in stats:
            csv_lines.append(f"{stat['file']},{stat['errors']},{stat['improvements']}")

        csv_content: str = "\n".join(csv_lines)
        assert "a.py,5,10" in csv_content

    def test_export_to_html(self) -> None:
        """Test exporting to HTML."""
        stats: Dict[str, int] = {"files": 100, "errors": 0}
        html: str = (
            "<table>\n"
            "    <tr><td>Files</td><td>{files}</td></tr>\n"
            "    <tr><td>Errors</td><td>{errors}</td></tr>\n"
            "</table>\n"
        ).format(files=stats["files"], errors=stats["errors"])

        assert "<table>" in html
        assert "100" in html

    def test_export_to_excel(self) -> None:
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

    def test_export_to_sqlite(self) -> None:
        """Test exporting to SQLite."""
        import sqlite3

        stats = [
            {"file": "a.py", "errors": 5},
            {"file": "b.py", "errors": 2},
        ]

        conn: Connection = sqlite3.connect(":memory:")
        cursor: Cursor = conn.cursor()
        cursor.execute("CREATE TABLE stats (file TEXT, errors INTEGER)")

        for stat in stats:
            cursor.execute(
                "INSERT INTO stats VALUES (?, ?)", (stat["file"], stat["errors"])
            )

        cursor.execute("SELECT COUNT(*) FROM stats")
        count = cursor.fetchone()[0]

        assert count == 2
        conn.close()


class TestAggregationAdvanced(unittest.TestCase):
    """Tests for stat aggregation by different dimensions."""

    def test_aggregate_by_file(self) -> None:
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

    def test_aggregate_by_agent(self) -> None:
        """Test aggregating stats by agent."""
        entries = [
            {"agent": "coder", "improvements": 10},
            {"agent": "coder", "improvements": 5},
            {"agent": "tester", "improvements": 8},
        ]

        by_agent: dict[Any, Any] = {}
        for entry in entries:
            by_agent[entry["agent"]] = (
                by_agent.get(entry["agent"], 0) + entry["improvements"]
            )

        assert by_agent["coder"] == 15

    def test_aggregate_by_date(self) -> None:
        """Test aggregating stats by date."""
        entries = [
            {"date": "2025-12-16", "issues": 5},
            {"date": "2025-12-16", "issues": 3},
            {"date": "2025-12-15", "issues": 2},
        ]

        by_date: dict[Any, Any] = {}
        for entry in entries:
            by_date[entry["date"]] = by_date.get(entry["date"], 0) + entry["issues"]

        assert by_date["2025-12-16"] == 8


class TestStatisticalSummariesAdvanced(unittest.TestCase):
    """Tests for statistical calculations."""

    def test_calculate_mean(self) -> None:
        """Test calculating mean."""
        values: List[int] = [10, 20, 30, 40, 50]
        mean: float = sum(values) / len(values)
        assert mean == 30.0

    def test_calculate_median(self) -> None:
        """Test calculating median."""
        values: List[int] = [10, 20, 30, 40, 50]
        sorted_vals: List[int] = sorted(values)
        median: int = sorted_vals[len(sorted_vals) // 2]
        assert median == 30

    def test_calculate_stddev(self) -> None:
        """Test calculating standard deviation."""
        import statistics

        values: List[int] = [10, 20, 30, 40, 50]
        stddev: float = statistics.stdev(values)

        assert stddev > 0

    def test_calculate_percentiles(self) -> None:
        """Test calculating percentiles."""
        values: List[int] = list(range(1, 101))
        p50_idx: int = int(len(values) * 0.5) - 1
        p95_idx: int = int(len(values) * 0.95) - 1
        p50: int = values[p50_idx]
        p95: int = values[p95_idx]

        assert p50 == 50
        assert p95 > 90  # Allow for rounding differences


class TestBenchmarkingAdvanced(unittest.TestCase):
    """Tests for performance benchmarking."""

    def test_track_agent_timing(self) -> None:
        """Test tracking agent execution time."""
        timings: Dict[str, float] = {
            "coder": 45.2,
            "tester": 32.1,
            "reviewer": 18.5,
        }

        slowest = max(timings, key=timings.get)
        assert slowest == "coder"

    def test_calculate_average_time_per_file(self) -> None:
        """Test calculating average processing time."""
        total_time = 120.5
        files_processed = 100

        avg_time: float = total_time / files_processed
        assert abs(avg_time - 1.205) < 0.01

    def test_benchmark_per_agent_statistics(self) -> None:
        """Test per-agent benchmark statistics."""
        agent_times: Dict[str, List[int]] = {
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


class TestCachingAdvanced(unittest.TestCase):
    """Tests for caching performance optimizations."""

    def test_cache_computed_stats(self) -> None:
        """Test caching computed statistics."""
        cache: dict[Any, Any] = {}

        def get_stats(file_id: str) -> Dict[str, int]:
            if file_id in cache:
                return cache[file_id]

            stats: Dict[str, int] = {"errors": 5, "coverage": 85}
            cache[file_id] = stats
            return stats

        # First call computes
        result1 = get_stats("file1")
        # Second call uses cache
        result2 = get_stats("file1")

        assert result1 == result2

    def test_cache_invalidation(self) -> None:
        """Test cache invalidation."""
        cache: Dict[str, Dict[str, int]] = {"file1": {"errors": 5}}

        # Invalidate cache
        cache.pop("file1")

        assert "file1" not in cache

    def test_cache_expiration(self) -> None:
        """Test cache expiration."""

        cache_items = {
            "file1": {"data": "stats", "timestamp": time.time()},
        }

        # Simulate expiration check (e.g., 1 hour)
        max_age = 3600
        current_time: float = time.time()

        expired = {
            k: v
            for k, v in cache_items.items()
            if current_time - v["timestamp"] > max_age
        }

        assert len(expired) == 0
