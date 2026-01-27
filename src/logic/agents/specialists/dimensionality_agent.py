#!/usr/bin/env python3

"""
Dimensionality agent.py module.
"""
# Copyright 2026 PyAgent Authors
# DimensionalityAgent: Feature Compression and Latent Space Mapping - Phase 319 Enhanced
# Phase 16: Rust acceleration for PCA reduction, embedding stats, k-means clustering

from __future__ import annotations

import contextlib
import json
import logging
import math
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

# Phase 16: Rust acceleration imports
try:
    import rust_core

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False
    logging.debug("rust_core not available, using Python fallback for DimensionalityAgent")


class ReductionMethod(Enum):
    """Supported dimensionality reduction methods."""
    PCA = "pca"
    TSNE = "tsne"
    UMAP = "umap"
    TRUNCATION = "truncation"
    RANDOM_PROJECTION = "random_projection"
    AUTOENCODER = "autoencoder"


@dataclass
class EmbeddingStats:
    """Statistics for an embedding."""

    dimension: int
    mean: float
    variance: float
    sparsity: float  # Fraction of near-zero values
    norm: float


# pylint: disable=too-many-ancestors
class DimensionalityAgent(BaseAgent):
    """
    Agent specializing in simplifying complex datasets and high-dimensional spaces.
    Focuses on PCA, t-SNE (simulated), UMAP, and semantic embedding compression.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._projection_cache: Dict[str, List[List[float]]] = {}
        self._concept_cache: Dict[str, List[str]] = {}
        self._system_prompt = (
            "You are the Dimensionality Reduction Agent. You find the essential "
            "components of complex data. You reduce noise while preserving meaning "
            "and structure. You excel at identifying latent patterns."
        )

    @as_tool
    async def reduce_embedding_dim(
        self, embedding: List[float], target_dim: int, method: str = "pca"
    ) -> Dict[str, Any]:
        """Reduces a vector's dimension using the specified method."""
        original_dim = len(embedding)

        if target_dim >= original_dim:
            return {
                "reduced": embedding,
                "original_dim": original_dim,
                "target_dim": target_dim,
                "method": "none",
                "message": "Target dimension >= original, no reduction needed",
            }

        reduction_method = (
            ReductionMethod(method) if method in [m.value for m in ReductionMethod] else ReductionMethod.PCA
        )

        if reduction_method == ReductionMethod.TRUNCATION:
            reduced = embedding[:target_dim]
        elif reduction_method == ReductionMethod.PCA:
            reduced = self._pca_reduce(embedding, target_dim)
        elif reduction_method == ReductionMethod.RANDOM_PROJECTION:
            reduced = self._random_projection(embedding, target_dim)
        else:
            # For complex methods, use truncation as fallback
            reduced = embedding[:target_dim]

        # Calculate reconstruction error estimate
        original_norm = math.sqrt(sum(x * x for x in embedding))
        reduced_norm = math.sqrt(sum(x * x for x in reduced))
        variance_retained = (reduced_norm / original_norm) ** 2 if original_norm > 0 else 0

        return {
            "reduced": reduced,
            "original_dim": original_dim,
            "target_dim": target_dim,
            "method": reduction_method.value,
            "variance_retained": round(variance_retained, 4),
            "compression_ratio": round(original_dim / target_dim, 2),
        }

    @as_tool
    async def batch_reduce(
        self, embeddings: List[List[float]], target_dim: int, method: str = "pca"
    ) -> Dict[str, Any]:
        """Reduces dimensions for a batch of embeddings."""
        reduced_all = []

        for emb in embeddings:
            result = await self.reduce_embedding_dim(emb, target_dim, method)
            reduced_all.append(result.get("reduced", emb[:target_dim]))

        return {
            "reduced_embeddings": reduced_all,
            "count": len(embeddings),
            "original_dim": len(embeddings[0]) if embeddings else 0,
            "target_dim": target_dim,
            "method": method,
        }

    @as_tool
    async def find_principal_concepts(
        self, text_list: List[str], n_concepts: int = 5, _include_weights: bool = True
    ) -> Dict[str, Any]:
        """Identifies the 'principal components' (top concepts) of a text corpus."""
        texts_preview = "\n".join([f"- {t[:200]}..." if len(t) > 200 else f"- {t}" for t in text_list[:20]])

        prompt = (
            f"Analyze this corpus and identify the top {n_concepts} principal themes/concepts:\n\n"
            f"{texts_preview}\n\n"
            "For each concept, provide:\n"
            "1. A concise label\n"
            "2. Weight/importance (0-1)\n"
            "3. Key terms associated with it\n"
            "4. Brief description\n\n"
            "Output JSON: {'concepts': [{'label': '...', 'weight': 0.X, 'terms': [...], 'description': '...'}]}"
        )

        res = await self.improve_content(prompt)

        with contextlib.suppress(Exception):
            match = re.search(r"(\{[\s\S]*\})", res)
            if match:
                data = json.loads(match.group(1))

                # Cache concepts
                cache_key = f"concepts_{hash(tuple(text_list[:5]))}"
                self._concept_cache[cache_key] = [c["label"] for c in data.get("concepts", [])]

                return data

        return {"raw": res}

    @as_tool
    async def compute_embedding_stats(self, embedding: List[float]) -> Dict[str, Any]:
        """Computes statistical properties of an embedding."""
        n = len(embedding)

        if n == 0:
            return {"error": "Empty embedding"}

        # Phase 16: Try Rust-accelerated embedding stats
        if _RUST_AVAILABLE and hasattr(rust_core, "compute_embedding_stats_rust"):
            try:
                result = rust_core.compute_embedding_stats_rust(embedding)
                if result:
                    return result
            except (AttributeError, RuntimeError, TypeError):
                pass  # Fall through to Python implementation

        mean = sum(embedding) / n
        variance = sum((x - mean) ** 2 for x in embedding) / n
        norm = math.sqrt(sum(x * x for x in embedding))

        # Sparsity (fraction of near-zero values)
        threshold = 0.01 * (max(abs(x) for x in embedding) if embedding else 1)
        sparsity = sum(1 for x in embedding if abs(x) < threshold) / n

        # Percentiles
        sorted_emb = sorted(embedding)
        p25 = sorted_emb[int(n * 0.25)]
        p50 = sorted_emb[int(n * 0.50)]
        p75 = sorted_emb[int(n * 0.75)]

        return {
            "dimension": n,
            "mean": round(mean, 6),
            "variance": round(variance, 6),
            "std_dev": round(math.sqrt(variance), 6),
            "norm": round(norm, 6),
            "sparsity": round(sparsity, 4),
            "min": round(min(embedding), 6),
            "max": round(max(embedding), 6),
            "percentiles": {"p25": round(p25, 6), "p50": round(p50, 6), "p75": round(p75, 6)},
        }

    @as_tool
    async def cluster_embeddings(self, embeddings: List[List[float]], n_clusters: int = 3) -> Dict[str, Any]:
        """Simple k-means clustering of embeddings."""
        n = len(embeddings)
        if n < n_clusters:
            return {"error": f"Need at least {n_clusters} embeddings for {n_clusters} clusters"}

        # Phase 16: Try Rust-accelerated k-means clustering
        if _RUST_AVAILABLE and hasattr(rust_core, "kmeans_cluster_rust"):
            try:
                result = rust_core.kmeans_cluster_rust(embeddings, n_clusters, 3)
                if result:
                    return result
            except (AttributeError, RuntimeError, TypeError):
                pass  # Fall through to Python implementation

        dim = len(embeddings[0])

        # Initialize centroids (first k embeddings)
        centroids = [list(embeddings[i]) for i in range(n_clusters)]

        # Simple k-means (3 iterations)
        assignments = [0] * n
        for _ in range(3):
            # Assign points to nearest centroid
            for i, emb in enumerate(embeddings):
                min_dist = float("inf")
                for c_idx, centroid in enumerate(centroids):
                    dist = sum((a - b) ** 2 for a, b in zip(emb, centroid))
                    if dist < min_dist:
                        min_dist = dist
                        assignments[i] = c_idx

            # Update centroids
            for c_idx in range(n_clusters):
                cluster_points = [embeddings[i] for i in range(n) if assignments[i] == c_idx]
                if cluster_points:
                    centroids[c_idx] = [sum(p[d] for p in cluster_points) / len(cluster_points) for d in range(dim)]

        # Count cluster sizes
        cluster_sizes = {i: assignments.count(i) for i in range(n_clusters)}

        return {
            "n_clusters": n_clusters,
            "assignments": assignments,
            "cluster_sizes": cluster_sizes,
            "centroid_norms": [round(math.sqrt(sum(x * x for x in c)), 4) for c in centroids],
        }

    @as_tool
    async def compute_similarity_matrix(self, embeddings: List[List[float]], top_k: int = 5) -> Dict[str, Any]:
        """Computes cosine similarity matrix for embeddings."""
        n = len(embeddings)

        # Phase 16: Try Rust-accelerated similarity matrix computation
        if _RUST_AVAILABLE and hasattr(rust_core, "compute_similarity_matrix_rust"):
            try:
                result = rust_core.compute_similarity_matrix_rust(embeddings, top_k)
                if result:
                    return result
            except (AttributeError, RuntimeError, TypeError):
                pass  # Fall through to Python implementation

        # Compute norms
        norms = [math.sqrt(sum(x * x for x in e)) for e in embeddings]

        # Compute similarity matrix (upper triangle)
        similarities = []
        for i in range(n):
            row_sims = []
            for j in range(n):
                if norms[i] > 0 and norms[j] > 0:
                    dot = sum(a * b for a, b in zip(embeddings[i], embeddings[j]))
                    sim = dot / (norms[i] * norms[j])
                else:
                    sim = 0.0
                row_sims.append(round(sim, 4))
            similarities.append(row_sims)

        # Find top-k similar pairs
        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                pairs.append((i, j, similarities[i][j]))
        pairs.sort(key=lambda x: x[2], reverse=True)

        return {
            "matrix_shape": (n, n),
            "top_similar_pairs": [{"i": p[0], "j": p[1], "similarity": p[2]} for p in pairs[:top_k]],
            "avg_similarity": round(sum(p[2] for p in pairs) / len(pairs), 4) if pairs else 0,
        }

    def _pca_reduce(self, embedding: List[float], target_dim: int) -> List[float]:
        """Simple PCA-like reduction (keeps components with largest variance contribution)."""
        # Phase 16: Try Rust-accelerated PCA reduction
        if _RUST_AVAILABLE and hasattr(rust_core, "pca_reduce_rust"):
            try:
                result = rust_core.pca_reduce_rust(embedding, target_dim)
                if result is not None:
                    return result
            except (AttributeError, RuntimeError, TypeError):
                pass

        # Sort by absolute value and keep top components
        indexed = [(i, abs(v), v) for i, v in enumerate(embedding)]
        indexed.sort(key=lambda x: x[1], reverse=True)

        # Take top target_dim components, preserve order
        top_indices = sorted([x[0] for x in indexed[:target_dim]])
        return [embedding[i] for i in top_indices]

    def _random_projection(self, embedding: List[float], target_dim: int) -> List[float]:
        """Random projection (simplified)."""
        # Phase 16: Try Rust-accelerated random projection
        if _RUST_AVAILABLE and hasattr(rust_core, "random_projection_rust"):
            try:
                result = rust_core.random_projection_rust(embedding, target_dim, 42)
                if result is not None:
                    return result
            except (AttributeError, RuntimeError, TypeError):
                pass

        import random

        random.seed(42)  # Reproducible

        n = len(embedding)
        result = []

        for _ in range(target_dim):
            # Random linear combination
            weights = [random.gauss(0, 1) for _ in range(n)]
            projected = sum(w * v for w, v in zip(weights, embedding))
            result.append(projected / math.sqrt(n))

        return result
