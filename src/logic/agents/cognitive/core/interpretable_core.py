from __future__ import annotations
from typing import Any
import logging

logger = logging.getLogger(__name__)

try:
    import rust_core as rc
    RUST_AVAILABLE = True
except ImportError:
    rc = None
    RUST_AVAILABLE = False


class InterpretableCore:
    """
    InterpretableCore implements a logic-bridge for Sparse Autoencoders (SAE).
    It simulates the decomposition of LLM activations into human-interpretable features.

    Phase 14 Rust Optimizations:
    - top_k_indices_rust: Fast top-K selection for activation sparsification
    - decompose_activations_rust: Vectorized activation decomposition
    """

    def __init__(self, feature_count: int = 4096) -> None:
        self.feature_count = feature_count

    def decompose_activations(self, mock_activations: list[float]) -> dict[str, Any]:
        """
        Simulates SAE decomposition.
        Identifies 'Active Neurons' and maps them to semantic labels.

        Uses Rust-accelerated top-K selection when available for O(n) instead of O(n log n).
        """
        # Simulated 'Top-K' sparsification
        k = 10

        # Rust-accelerated top-K selection using partial sort
        if RUST_AVAILABLE and hasattr(rc, 'top_k_indices_rust'):
            try:
                top_k = rc.top_k_indices_rust(mock_activations, k)
            except Exception as e:
                logger.debug(f"Rust top_k_indices failed: {e}, using Python fallback")
                sorted_indices = sorted(
                    range(len(mock_activations)),
                    key=lambda i: mock_activations[i],
                    reverse=True,
                )
                top_k = sorted_indices[:k]
        else:
            sorted_indices = sorted(
                range(len(mock_activations)),
                key=lambda i: mock_activations[i],
                reverse=True,
            )
            top_k = sorted_indices[:k]

        active_features = []
        for idx in top_k:
            active_features.append(
                {
                    "index": idx,
                    "activation": mock_activations[idx],
                    "semantic_label": self._get_label_for_index(idx),
                }
            )

        return {
            "reconstruction_error": 0.005,
            "sparsity_ratio": k / self.feature_count,
            "active_features": active_features,
        }

    def simulate_neural_trace(self, agent_name: str, decision: str) -> list[str]:
        """
        Generates a 'Neural Trace' trace-log explaining the logic path.
        """
        trace = [
            f"Node: {agent_name} triggered by decision '{decision}'",
            "Activation: HIGH for 'Safety_Guardrail_7'",
            "Activation: LOW for 'Hallucination_Risk_2'",
            "SAE Feature: Found 'Code_Quality_Check' alignment > 0.85",
        ]
        return trace

    def _get_label_for_index(self, index: int) -> str:
        """Simulated semantic mapping of latent SAE features."""
        labels = [
            "Logic_Flow",
            "Synax_Error_Detector",
            "Circular_Dependency",
            "Resource_Limit",
            "Security_Honeypot",
            "Byzantine_Suspect",
        ]
        return labels[index % len(labels)]
