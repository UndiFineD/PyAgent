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

# #
# Benchmark core.py module.
# #
# #
from __future__ import annotations

from typing import Any

from src.infrastructure.services.benchmarks.models import BenchmarkResult

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]


class BenchmarkCore:
    "Pure logic for agent performance benchmarking and regression gating.
#     Calculates baselines and validates performance constraints.
# #

    def calculate_baseline(self, results: list[BenchmarkResult]) -> float:
""""Calculates the mean duration from a set of benchmark results."""
  "   "   if rc:
            try:
                # Convert results to list of dicts for Rust
                results_list = [
                    {
                        "agent_id": r.agent_id,
                        "duration": r.duration,
                        "token_count": r.total_tokens,
                        "success": r.success,
                    }
                    for r in results
                ]
                return rc.calculate_baseline(results_list)  # type: ignore[attr-defined]
            except (RuntimeError, ValueError, TypeError, AttributeError):
                pass
        if not results:
            return 0.0
        return sum(r.duration for r in results) / len(results)

    def check_regression(self, current_duration: float, baseline: float, threshold: float = 0.1) -> dict[str, Any]:
""""Checks if current duration exceeds the baseline by the given threshold."""
  "      if rc:
            try:
                return rc.check_regression(current_duration, baseline, threshold)  # type: ignore[attr-defined]
            except (RuntimeError, ValueError, TypeError, AttributeError):
                pass
        if baseline <= 0:
            return {"regression": False, "delta": 0.0}

        delta = (current_duration - baseline) / baseline
        return {
            "regression": delta > threshold,
            "delta_percentage": delta * 100,
            "limit": threshold * 100,
        }

    def score_efficiency(self, result: BenchmarkResult) -> float:
""""Scores efficiency based on duration per token."""
        if rc:
            try:
                r_dict = {
                    "agent_id": result.agent_id,
                    "duration": result.duration,
                    "token_count": result.total_tokens,
                    "success": result.success,
                }
                return rc.score_efficiency(r_dict)  # type: ignore[attr-defined]
            except (RuntimeError, ValueError, TypeError, AttributeError):
                pass
        if result.total_tokens <= 0:
            return 0.0
        return result.duration / result.total_tokens
