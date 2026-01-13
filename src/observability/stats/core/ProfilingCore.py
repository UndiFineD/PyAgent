
from __future__ import annotations
import pstats
from typing import List
from dataclasses import dataclass

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
    
    def analyze_stats(self, pstats_obj: pstats.Stats, limit: int = 10) -> List[ProfileStats]:
        """Converts raw pstats into a list of pure ProfileStats dataclasses."""
        results = []
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

    def identify_bottlenecks(self, stats: List[ProfileStats], threshold_ms: float = 100.0) -> List[str]:
        """Identifies functions exceeding the time threshold."""
        return [s.function_name for s in stats if s.total_time > (threshold_ms / 1000.0)]

    def calculate_optimization_priority(self, stats: ProfileStats) -> float:
        """Heuristic for optimization: time * frequency."""
        return stats.total_time * stats.call_count