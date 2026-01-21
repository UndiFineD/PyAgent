from __future__ import annotations
from dataclasses import dataclass

try:
    import rust_core as rc
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


@dataclass(frozen=True)
class AgentMetrics:
    """Metrics for agent load and performance tracking."""

    token_pressure: float  # 0.0 to 1.0 (context used / context limit)
    queue_depth: int
    avg_latency_ms: float
    error_rate: float


class LoadBalancerCore:
    """Pure logic for cognitive load balancing across the agent fleet.
    Calculates cognitive pressure and suggests optimal task routing.
    """

    def calculate_cognitive_pressure(self, metrics: AgentMetrics) -> float:
        """Heuristic for 'Cognitive Pressure': (complexity * history_len)."""
        # score = (tokens * 0.4) + (queue * 0.4) + (latency * 0.2)
        score = (
            (metrics.token_pressure * 0.4)
            + (min(metrics.queue_depth / 10, 1.0) * 0.4)
            + (min(metrics.avg_latency_ms / 5000, 1.0) * 0.2)
        )

        return min(max(score, 0.0), 1.0)

    def select_best_agent(self, agents: dict[str, AgentMetrics]) -> str:
        """Returns the Agent ID with the lowest cognitive pressure."""
        if not agents:
            return ""
        # Rust-accelerated agent selection
        if HAS_RUST:
            try:
                agent_data = [
                    (aid, m.token_pressure, m.queue_depth, m.avg_latency_ms)
                    for aid, m in agents.items()
                ]
                best_id, _ = rc.select_best_agent_rust(agent_data)  # type: ignore[attr-defined]
                return best_id
            except Exception:
                pass

        scores = {
            aid: self.calculate_cognitive_pressure(m) for aid, m in agents.items()
        }
        return min(scores, key=scores.get)

    def suggest_scaling(self, fleet_pressure: float) -> str:
        """Suggests infrastructure scaling based on aggregate pressure."""
        if fleet_pressure > 0.8:
            return "SPAWN_NEW_INSTANCES"
        if fleet_pressure < 0.2:
            return "CONSOLIDATE_SHARDS"
        return "STABLE"
