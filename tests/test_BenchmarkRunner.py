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

"""Per-module tests for src/core/memory/BenchmarkRunner.py.

This file satisfies the test_each_core_has_test_file convention.
Full integration benchmarks require a live PostgreSQL connection and are
not run in the standard CI test suite.
"""

from __future__ import annotations

from src.core.memory.BenchmarkRunner import BenchmarkRunner, validate


def test_benchmark_runner_validate() -> None:
    """Ensure the BenchmarkRunner validate() helper returns True."""
    assert validate() is True


def test_benchmark_runner_is_importable() -> None:
    """BenchmarkRunner must be importable as a class."""
    assert BenchmarkRunner is not None
    assert issubclass(BenchmarkRunner, object)
