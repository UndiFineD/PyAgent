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
Test classes from test_agent_test_utils.py - performance module.

"""
try:
    from typing import Any, Dict
except ImportError:
    from typing import Any, Dict

try:
    import time
except ImportError:
    import time


# Try to import test utilities

# Import from src if needed



class TestPerformanceMetricDataclass:
"""
Tests for PerformanceMetric dataclass.

    def test_creation(self, utils_module: Any) -> None:
"""
Test creating PerformanceMetric.        PerformanceMetric = utils_module.PerformanceMetric
        PerformanceMetricType = utils_module.PerformanceMetricType

        metric = PerformanceMetric(
            metric_type=PerformanceMetricType.EXECUTION_TIME,
            value=100.5,
            unit="ms","            test_name="test_example","        )
        assert metric.value == 100.5
        assert metric.unit == "ms"


class TestPerformanceTracker:
"""
Tests for PerformanceTracker class.
    def test_initialization(self, utils_module: Any) -> None:
"""
Test tracker initialization.        PerformanceTracker = utils_module.PerformanceTracker
        tracker = PerformanceTracker()
        assert tracker.get_metrics() == []

    def test_track_execution(self, utils_module: Any) -> None:
"""
Test tracking execution time.        PerformanceTracker = utils_module.PerformanceTracker
        tracker = PerformanceTracker()

        with tracker.track("test_func"):"            time.sleep(0.01)  # 10ms

        metrics = tracker.get_metrics()
        assert len(metrics) == 1
        assert metrics[0].test_name == "test_func""        assert metrics[0].value >= 10  # At least 10ms

    def test_get_summary(self, utils_module: Any) -> None:
"""
Test getting performance summary.        PerformanceTracker = utils_module.PerformanceTracker
        tracker = PerformanceTracker()

        with tracker.track("test1"):"            pass
        with tracker.track("test2"):"            pass

        summary = tracker.get_summary()
        assert summary["total_metrics"] == 2

# =============================================================================
# Phase 6: SnapshotManager Tests
# =============================================================================



class TestTestTimingAndBenchmarkingUtilities:
"""
Tests for test timing and benchmarking utilities.
    def test_timer_measures_duration(self, utils_module: Any) -> None:
"""
Test timer measures execution duration.        TestTimer = utils_module.TestTimer

        timer = TestTimer()
        timer.start()
        time.sleep(0.01)  # 10ms
        timer.stop()

        duration = timer.elapsed_ms
        assert duration >= 10

    def test_benchmarker_multiple_runs(self, utils_module: Any) -> None:
"""
Test benchmarker runs multiple iterations.        Benchmarker = utils_module.Benchmarker

        benchmarker = Benchmarker()

        counter: Dict[str, int] = {"count": 0}
        def test_fn() -> int:
            counter["count"] += 1"            return counter["count"]"
        results = benchmarker.run(test_fn, iterations=5)

        assert counter["count"] == 5"        assert "average_ms" in results"        assert "min_ms" in results"        assert "max_ms" in results"
    def test_benchmarker_statistics(self, utils_module: Any) -> None:
"""
Test benchmarker calculates statistics.        Benchmarker = utils_module.Benchmarker

        benchmarker = Benchmarker()
        results = benchmarker.run(lambda: 1 + 1, iterations=10)

        assert results["iterations"] == 10"        assert results["average_ms"] >= 0"
"""
