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
Profiling Core - cProfile aggregation and bottleneck analysis

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Import ProfilingCore and ProfileStats from profiling_core.
- Use ProfilingCore.analyze_stats(pstats_obj, limit=10) to convert a
  cProfile pstats.Stats into a list of ProfileStats.
- Call ProfilingCore.identify_bottlenecks(stats, threshold_ms=100.0) to
  get function names exceeding the threshold.
- Use ProfilingCore.calculate_optimization_priority(profile_stat) to
  rank optimization impact.

WHAT IT DOES:
- Parses pstats.Stats produced by cProfile and extracts top N functions
  sorted by cumulative time.
- Represents results as immutable ProfileStats dataclasses with function
  name, call count, total time, per-call time and optional source info.
- Identifies bottlenecks either via optional Rust acceleration
  (rust_core.identify_bottlenecks) or a fallback Python filter using a
  millisecond threshold.
- Provides a simple heuristic (time * frequency) to compute an
  optimization priority score.

WHAT IT SHOULD DO BETTER:
- Preserve and surface file_name and line_number values parsed from
  pstats keys (currently left as None), so callers can map hotspots to
  source locations.
- Improve parsing of pstats.Stats entries (the func tuple) to extract
  readable function names and module paths rather than str(func).
- Make threshold units and defaults explicit (threshold_ms is
  milliseconds but fallback compares seconds), and unify units across
  code and Rust FFI.
- Add robust error handling and logging around rust_core integration and
  pstats structure differences, and provide comprehensive unit tests.
- Consider richer aggregation (per-module summaries, percentiles,
  exclusive vs inclusive time) and better sorting options (by per-call,
  total, or call count).
- Return richer typed results from identify_bottlenecks
  (e.g., list[ProfileStats] or list[dict]) instead of only names for
  downstream tooling.
- Document and test interaction with optional Rust extension and ensure
  deterministic behavior when rc is unavailable.

FILE CONTENT SUMMARY:
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
        stats_dict: dict[Any, Any] = pstats_obj.stats  # type: ignore[attr-defined]
        for func, (cc, nc, tt, ct, callers) in stats_dict.items():
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
            except Exception:  # pylint: disable=broad-exception-caught
                pass
        return [s.function_name for s in stats if s.total_time > (threshold_ms / 1000.0)]

    def calculate_optimization_priority(self, stats: ProfileStats) -> float:
        """Heuristic for optimization: time * frequency."""
        return stats.total_time * stats.call_count
