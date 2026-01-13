# -*- coding: utf-8 -*-
"""Test classes from test_agent_test_utils.py - performance module."""

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
    from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
except ImportError:
    # Fallback
    AGENT_DIR: Path = Path(__file__).parent.parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self) -> Self: 

            return self
        def __exit__(self, *args) -> None: 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed

class TestPerformanceMetricDataclass:
    """Tests for PerformanceMetric dataclass."""

    def test_creation(self, utils_module: Any) -> None:
        """Test creating PerformanceMetric."""
        PerformanceMetric = utils_module.PerformanceMetric
        PerformanceMetricType = utils_module.PerformanceMetricType

        metric = PerformanceMetric(
            metric_type=PerformanceMetricType.EXECUTION_TIME,
            value=100.5,
            unit="ms",
            test_name="test_example",
        )
        assert metric.value == 100.5
        assert metric.unit == "ms"



class TestPerformanceTracker:
    """Tests for PerformanceTracker class."""

    def test_initialization(self, utils_module: Any) -> None:
        """Test tracker initialization."""
        PerformanceTracker = utils_module.PerformanceTracker
        tracker = PerformanceTracker()
        assert tracker.get_metrics() == []

    def test_track_execution(self, utils_module: Any) -> None:
        """Test tracking execution time."""
        import time
        PerformanceTracker = utils_module.PerformanceTracker
        tracker = PerformanceTracker()

        with tracker.track("test_func"):
            time.sleep(0.01)  # 10ms

        metrics = tracker.get_metrics()
        assert len(metrics) == 1
        assert metrics[0].test_name == "test_func"
        assert metrics[0].value >= 10  # At least 10ms

    def test_get_summary(self, utils_module: Any) -> None:
        """Test getting performance summary."""
        PerformanceTracker = utils_module.PerformanceTracker
        tracker = PerformanceTracker()

        with tracker.track("test1"):
            pass
        with tracker.track("test2"):
            pass

        summary = tracker.get_summary()
        assert summary["total_metrics"] == 2


# =============================================================================
# Phase 6: SnapshotManager Tests
# =============================================================================



class TestTestTimingAndBenchmarkingUtilities:
    """Tests for test timing and benchmarking utilities."""

    def test_timer_measures_duration(self, utils_module: Any) -> None:
        """Test timer measures execution duration."""
        TestTimer = utils_module.TestTimer
        import time

        timer = TestTimer()
        timer.start()
        time.sleep(0.01)  # 10ms
        timer.stop()

        duration = timer.elapsed_ms
        assert duration >= 10

    def test_benchmarker_multiple_runs(self, utils_module: Any) -> None:
        """Test benchmarker runs multiple iterations."""
        Benchmarker = utils_module.Benchmarker

        benchmarker = Benchmarker()

        counter: Dict[str, int] = {"count": 0}

        def test_fn() -> int:
            counter["count"] += 1
            return counter["count"]

        results = benchmarker.run(test_fn, iterations=5)

        assert counter["count"] == 5
        assert "average_ms" in results
        assert "min_ms" in results
        assert "max_ms" in results

    def test_benchmarker_statistics(self, utils_module: Any) -> None:
        """Test benchmarker calculates statistics."""
        Benchmarker = utils_module.Benchmarker

        benchmarker = Benchmarker()
        results = benchmarker.run(lambda: 1 + 1, iterations=10)

        assert results["iterations"] == 10
        assert results["average_ms"] >= 0



