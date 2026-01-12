from __future__ import annotations
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass(frozen=True)
class BenchmarkResult:
    agent_id: str
    latency_ms: float
    token_count: int
    success: bool

class BenchmarkCore:
    """Pure logic for agent performance benchmarking and regression gating.
    Calculates baselines and validates performance constraints.
    """
    
    def calculate_baseline(self, results: List[BenchmarkResult]) -> float:
        """Calculates the mean latency from a set of benchmark results."""
        if not results: return 0.0
        return sum(r.latency_ms for r in results) / len(results)

    def check_regression(self, current_latency: float, baseline: float, threshold: float = 0.1) -> Dict[str, Any]:
        """Checks if current latency exceeds the baseline by the given threshold."""
        if baseline <= 0: return {"regression": False, "delta": 0.0}
        
        delta = (current_latency - baseline) / baseline
        return {
            "regression": delta > threshold,
            "delta_percentage": delta * 100,
            "limit": threshold * 100
        }

    def score_efficiency(self, result: BenchmarkResult) -> float:
        """Scores efficiency based on latency per token."""
        if result.token_count <= 0: return 0.0
        return result.latency_ms / result.token_count
