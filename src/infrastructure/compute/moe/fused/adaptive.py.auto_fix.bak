#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Adaptive.py module.
"""

import numpy as np

from .config import FusedMoEConfig
from .layer import FusedMoELayer



class AdaptiveMoELayer(FusedMoELayer):
    """Adaptive MoE layer with dynamic top-k selection and capacity management.
    def __init__(
        self,
        config: FusedMoEConfig,
        *args,
        min_top_k: int = 1,
        max_top_k: int = 4,
        capacity_factor: float = 1.0,
        **kwargs,
    ) -> None:
        super().__init__(config, *args, **kwargs)
        self.min_top_k = min_top_k
        self.max_top_k = max_top_k
        self.capacity_factor = capacity_factor
        self.expert_capacity = int((config.num_experts * capacity_factor) / config.num_experts)  # Simplistic

    def forward(
        self,
        x: np.ndarray,
        router_logits: np.ndarray | None = None,
        context_score: float = 1.0,
    ) -> np.ndarray:
        # Determine dynamic top_k based on context score
        current_top_k = int(np.clip(self.max_top_k * context_score, self.min_top_k, self.max_top_k))

        # Override top_k for this call
        original_top_k = self.config.top_k
        self.config.top_k = current_top_k

        try:
            return super().forward(x, router_logits)
        finally:
            self.config.top_k = original_top_k



class HierarchicalMoELayer:
    """Two-level hierarchical MoE for extreme scale.
    def __init__(
        self,
        config: FusedMoEConfig,
        num_clusters: int = 4,
        cluster_top_k: int = 1,
        *args,
        **kwargs,
    ) -> None:
        self.num_clusters = num_clusters
        self.cluster_top_k = cluster_top_k

        # Create clusters
        cluster_experts = config.num_experts // num_clusters
        self.clusters = [
            FusedMoELayer(
                FusedMoEConfig(
                    hidden_size=config.hidden_size,
                    intermediate_size=config.intermediate_size,
                    num_experts=cluster_experts,
                    top_k=config.top_k,
                ),
                *args,
                **kwargs,
            )
            for _ in range(num_clusters)
        ]

        # Cluster router
        self.cluster_router = np.random.randn(config.hidden_size, num_clusters).astype(np.float32) * 0.01

    def forward(self, x: np.ndarray) -> np.ndarray:
        # 1. Route to clusters
        cluster_logits = x @ self.cluster_router
        cluster_probs = self._softmax(cluster_logits)

        # 2. Select top clusters
        top_cluster_indices = np.argsort(cluster_probs, axis=-1)[:, -self.cluster_top_k :]

        # 3. Dispatch and aggregate
        # This is a simplified version of hierarchical dispatch
        out = np.zeros_like(x)
        for i in range(self.num_clusters):
            # Mask for tokens routed to this cluster
            mask = np.any(top_cluster_indices == i, axis=-1)
            if not np.any(mask):
                continue

            cluster_out = self.clusters[i].forward(x[mask])

            # Weighted addition based on cluster prob
            # Note: in real impl this is more complex
            probs = cluster_probs[mask, i : i + 1]
            out[mask] += cluster_out * probs

        return out

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / e_x.sum(axis=-1, keepdims=True)
