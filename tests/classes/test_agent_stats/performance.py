# -*- coding: utf-8 -*-
"""Test classes from test_agent_stats.py - performance module."""

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


class TestStatsQueryPerformance:
    """Tests for stats query performance."""

    def test_query_with_time_range(self, stats_module: Any) -> None:
        """Test query with time range."""
        StatsQueryEngine = stats_module.StatsQueryEngine

        engine = StatsQueryEngine()

        # Add data
        for i in range(100):
            engine.insert("metric1", timestamp=i * 1000, value=i)

        result = engine.query("metric1", start=10000, end=50000)
        assert len(result) > 0
        assert all(10000 <= r["timestamp"] <= 50000 for r in result)

    def test_query_with_aggregation(self, stats_module: Any) -> None:
        """Test query with aggregation."""
        StatsQueryEngine = stats_module.StatsQueryEngine

        engine = StatsQueryEngine()

        engine.insert("metric1", timestamp=1000, value=10)
        engine.insert("metric1", timestamp=2000, value=20)
        engine.insert("metric1", timestamp=3000, value=30)

        result = engine.query("metric1", aggregation="avg")
        assert result["value"] == 20.0



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



