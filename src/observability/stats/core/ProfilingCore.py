
from __future__ import annotations
from typing import Any
import pstats
from dataclasses import dataclass

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



class ProfilingCore:
    """Pure logic for cProfile aggregation and bottleneck analysis.
    Identifies slow methods and calculates optimization priority.
    """

    def analyze_stats(self, pstats_obj: pstats.Stats, limit: int = 10) -> list[ProfileStats]:
        """Converts raw pstats into a list of pure ProfileStats dataclasses."""
        results: list[Any] = []
        pstats_obj.sort_stats('cumulative')

        # pstats stores data in a complex tuple structure
        # (cc, nc, tt, ct, callers)
        for func, (cc, nc, tt, ct, callers) in pstats_obj.stats.items():
            if len(results) >= limit:
                break
            results.append(ProfileStats(
                function_name=str(func),
                call_count=cc,
                total_time=ct,
                per_call=ct / cc if cc > 0 else 0
            ))

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
                        "per_call": s.per_call
                    } for s in stats
                ]
                return rc.identify_bottlenecks(stats_list, threshold_ms)  # type: ignore[attr-defined]
            except Exception:
                pass
        return [s.function_name for s in stats if s.total_time > (threshold_ms / 1000.0)]

    def calculate_optimization_priority(self, stats: ProfileStats) -> float:
        """Heuristic for optimization: time * frequency."""
        return stats.total_time * stats.call_count
