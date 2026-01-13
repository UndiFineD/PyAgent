
import logging
import os
from typing import Any, Dict
from src.infrastructure.backend.RunnerBackends import BackendHandlers

class RoutingEngine:
    """
    Phase 248: PERFORMANCE-BASED ROUTING
    Phase 300: FEDERATED SOVEREIGNTY ROUTING
    Weights latency (TTFT/TPS) vs. quality to route tasks to the optimal provider.
    Now supports routing to external federated clusters.
    """

    def __init__(self) -> None:
        self.providers = ["github_models", "openai", "codex", "local", "federated_cluster"]
        logging.debug("RoutingEngine initialized")

    def select_provider(self, task_type: str = "general", priority: str = "balanced", federated: bool = False) -> str:
        """
        Selects the best provider based on task type and performance metrics.
        
        Args:
            task_type: "classification", "summarization", "coding", "reasoning"
            priority: "latency", "quality", "cost", "balanced"
            federated: If True, prioritizes external swarm cooperation (Phase 300)
        """
        if federated:
            logging.info("RoutingEngine: Redirecting to federated cluster for sovereign negotiation.")
            return "federated_cluster"

        report = BackendHandlers.get_performance_report()
        logging.debug(f"RoutingEngine: Performance Report: {report}")

        # Default fallback
        preferred = os.environ.get("DV_AGENT_BACKEND", "github_models")

        if priority == "latency":
            # Select provider with lowest TTFT or highest TPS
            best_provider = preferred
            min_ttft = float('inf')
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
            "default_backend": os.environ.get("DV_AGENT_BACKEND", "github_models")
        }