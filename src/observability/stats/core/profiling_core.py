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

"""
Profiling core.py module.
"""

from __future__ import annotations

import pstats
from dataclasses import dataclass
from typing import Any

try:
    import rust_core as rc
except ImportError:  # type: ignore[assignment]
    rc = None  # type: ignore[assignment]


@dataclass(frozen=True)
class ProfileStats:
    function_name: str
    call_count: int
    total_time: float
    per_call: float
    file_name: str | None = None
    line_number: int | None = None


class ProfilingCore:
    """Pure logic for cProfile aggregation and bottleneck analysis.
    Identifies slow methods and calculates optimization priority.
    """

    def analyze_stats(self, pstats_obj: pstats.Stats, limit: int = 10) -> list[ProfileStats]:
        """Converts raw pstats into a list of pure ProfileStats dataclasses."""
        results: list[Any] = []
        pstats_obj.sort_stats("cumulative")

        # pstats stores data in a complex tuple structure
        # (cc, nc, tt, ct, callers)
        for func, (cc, nc, tt, ct, callers) in pstats_obj.stats.items():
            if len(results) >= limit:
                break
            results.append(
                ProfileStats(
                    function_name=str(func),
                    call_count=cc,
                    total_time=ct,
                    per_call=ct / cc if cc > 0 else 0,
                )
            )

        return results

    def identify_bottlenecks(self, stats: list[ProfileStats], threshold_ms: float = 100.0) -> list[str]:
        """Identifies functions exceeding the time threshold."""
        if rc:
            try:
                # Convert list of dataclasses to list of dicts for Rust
                stats_list = [
                    {
                        "function_name": s.function_name,
                        "call_count": s.call_count,
                        "total_time": s.total_time,
                        "per_call": s.per_call,
                    }
                    for s in stats
                ]
                return rc.identify_bottlenecks(stats_list, threshold_ms)  # type: ignore[attr-defined]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                pass
        return [s.function_name for s in stats if s.total_time > (threshold_ms / 1000.0)]

    def calculate_optimization_priority(self, stats: ProfileStats) -> float:
        """Heuristic for optimization: time * frequency."""
        return stats.total_time * stats.call_count
