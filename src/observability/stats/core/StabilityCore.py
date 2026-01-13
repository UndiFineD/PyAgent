
from __future__ import annotations
from typing import List
from dataclasses import dataclass

@dataclass(frozen=True)
class FleetMetrics:
    avg_error_rate: float
    total_token_out: int
    active_agent_count: int
    latency_p95: float

class StabilityCore:
    """Pure logic for calculating fleet stability and reasoning coherence.
    Integrates SAE activation metrics and error trends into a unified score.
    """
    
    def calculate_stability_score(self, metrics: FleetMetrics, sae_anomalies: int) -> float:
        """Calculates a stability score from 0.0 to 1.0."""
        # Baseline: 1.0
        # Deductions: error_rate * 5.0, sae_anomalies * 0.05, latency_p95 overhead
        
        score = 1.0
        score -= (metrics.avg_error_rate * 5.0)
        score -= (sae_anomalies * 0.05)
        
        latency_penalty = max(0.0, (metrics.latency_p95 - 2000) / 10000)
        score -= latency_penalty
        
        return min(max(score, 0.0), 1.0)

    def is_in_stasis(self, score_history: List[float]) -> bool:
        """Determines if the swarm is in 'Digital Stasis' (too rigid)."""
        if len(score_history) < 10:
            return False
        variance = sum((x - sum(score_history)/len(score_history))**2 for x in score_history) / len(score_history)
        return variance < 0.0001 # Minimal change indicates stasis

    def get_healing_threshold(self, stability_score: float) -> float:
        """Returns the threshold for triggering self-healing subroutines."""
        if stability_score < 0.3:
            return 0.9 # Aggressive healing
        return 0.5