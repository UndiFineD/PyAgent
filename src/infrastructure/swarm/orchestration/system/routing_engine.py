"""
Routing engine for task distribution.
(Facade for src.core.base.common.routing_core)
"""

from src.core.base.common.routing_core import RoutingCore as StandardRoutingCore

class RoutingEngine(StandardRoutingCore):
    """Facade for RoutingCore."""
    
    def select_provider(self, task_type="general", priority="balanced", federated=False):
        """Legacy compatibility wrapper."""
        if federated:
            return "federated_cluster"
        return self.select_best_provider(task_type, priority)

        if priority == "latency":
            # Select provider with lowest TTFT or highest TPS
            best_provider = preferred
            min_ttft = float("inf")
            for p, metrics in report.items():
                if metrics["ttft"] < min_ttft:
                    min_ttft = metrics["ttft"]
                    best_provider = p
            return best_provider

        if task_type == "classification" and not os.environ.get("DV_AGENT_BACKEND"):
            # Classification is often better on fast small models
            if "openai" in report and report["openai"]["ttft"] < 1.0:
                return "openai"

        if task_type == "reasoning":
            # Reasoning usually requires frontier models, prefer GitHub Models (defaulting to gpt-4o)
            return "github_models"

        return preferred

    @staticmethod
    def get_routing_stats() -> dict[str, Any]:
        """Returns statistics on routing decisions and provider health."""
        return {
            "active_metrics": BackendHandlers.get_performance_report(),
            "default_backend": os.environ.get("DV_AGENT_BACKEND", "github_models"),
        }
