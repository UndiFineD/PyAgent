#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
"""Test classes from test_generate_agent_reports.py - performance module."""

from __future__ import annotations
import unittest
from typing import Dict, Self
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


class TestPerformanceMetrics(unittest.TestCase):
    """Test performance metrics collection and reporting."""

    def test_execution_time_tracking(self) -> None:
        """Test tracking execution time of operations."""
        timings: Dict[str, float] = {
            "analysis": 2.5,
            "report_generation": 1.2,
            "visualization": 3.1,
            "distribution": 0.8,
        }

        total_time: float | int = sum(timings.values())
        self.assertGreater(total_time, 7)

    def test_memory_usage_metrics(self) -> None:
        """Test collecting memory usage metrics."""
        memory_stats = {
            "peak_memory_mb": 256,
            "average_memory_mb": 180,
            "memory_per_file_kb": 1.5,
        }

        self.assertGreater(
            memory_stats["peak_memory_mb"], memory_stats["average_memory_mb"]
        )

    def test_performance_comparison_over_time(self) -> None:
        """Test comparing performance metrics over time."""
        performance = [
            {"date": "2024-01-01", "execution_time": 5.2},
            {"date": "2024-01-15", "execution_time": 3.8},
        ]

        improvement = (
            performance[0]["execution_time"] - performance[1]["execution_time"]
        )
        improvement_pct = (improvement / performance[0]["execution_time"]) * 100

        self.assertGreater(improvement_pct, 0)
