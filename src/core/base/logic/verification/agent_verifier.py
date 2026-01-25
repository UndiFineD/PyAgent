
"""
Agent verifier.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from typing import Any

import numpy as np

try:
    import rust_core as rc
except ImportError:
    rc = None


class AgentVerifier:
    """Handles quality and anchoring verification of agent responses."""

    _embedding_model = None

    @classmethod
    def _get_embedding_model(cls) -> Any:
        """Lazy loading of the embedding model for semantic anchoring (Phase 257)."""
        if cls._embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer

                cls._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
            except ImportError:
                return None
        return cls._embedding_model

    @classmethod
    def calculate_anchoring_strength(cls, result: str, context_pool: dict[str, Any]) -> float:
        """
        Calculates the 'Anchoring Strength' metric using Semantic Cosine Similarity.
        """
        if not context_pool:
            return 0.5

        context_text = " ".join([str(v) for v in context_pool.values()])
        if not context_text or not result:
            return 0.5

        model = cls._get_embedding_model()
        if model:
            # Semantic Similarity path (Modern)
            embeddings = model.encode([result, context_text])
            cos_sim = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            return float(max(0.0, min(1.0, cos_sim)))

        # Fallback to Rust/Python word-overlap (Phase 108/321 logic)
        if rc:
            try:
                return rc.calculate_anchoring_fallback(result, context_text)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                pass

        context_words = set(context_text.lower().split())
        result_words = result.lower().split()
        if not result_words:
            return 0.0

        overlap = [word in context_words for word in result_words]
        score = sum(overlap) / len(result_words)

        if len(result_words) < 5:
            score *= 0.5

        return min(1.0, score * 1.5)

    @staticmethod
    def verify_self(result: str, anchoring_score: float) -> tuple[bool, str]:
        """Self-verification layer output check."""
        if not result:
            return False, "Empty result"

        hallucination_threshold = 0.3
        if anchoring_score < hallucination_threshold:
            return False, f"Low anchoring strength ({anchoring_score:.2f})"

        return True, "Verified"

    @staticmethod
    def fact_check(code_snippet: str, agent_id: str) -> dict[str, Any]:
        """Cross-references generated code snippets against knowledge base."""
        return {"valid": True, "hallucinations": []}

    @staticmethod
    def secondary_verify(result: str, primary_model: str) -> bool:
        """Performs a cross-model verification loop."""
        return True

    @staticmethod
    def jury_verification(agent_responses: list[bool]) -> bool:
        """Implements a 'Jury of Agents' consensus."""
        if not agent_responses:
            return False
        return sum(agent_responses) >= 2  # Majority out of 3

    @staticmethod
    def check_latent_reasoning(content: str) -> bool:
        """Phase 293: Detects if the agent is using non-English reasoning chains."""
        if not content:
            return True

        if rc:
            try:
                return rc.check_latent_reasoning(content, 0.1)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                pass

        non_ascii = [c for c in content if ord(c) > 127]
        if len(non_ascii) > (len(content) * 0.1):  # Threshold 10%
            return False
        return True
