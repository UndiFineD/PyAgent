#!/usr/bin/env python3
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


Method.py module.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from .config import FusedMoEConfig, FusedMoEParallelConfig
from .utils import determine_expert_map

try:
    import torch
    import torch.nn.functional as F

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False




class FusedMoEMethodBase(ABC):
    """Base class for MoE computation methods.
    @abstractmethod
    def create_weights(
        self,
        config: FusedMoEConfig,
        parallel_config: FusedMoEParallelConfig,
        device: str = "cpu","    ) -> dict[str, Any]:
        pass

    @abstractmethod
    def apply(
        self,
        x: Any,
        router_logits: Any,
        top_k: int,
        renormalize: bool,
        weights: dict[str, Any],
    ) -> Any:
        pass




class UnquantizedFusedMoEMethod(FusedMoEMethodBase):
    """Unquantized MoE computation method.
    def create_weights(
        self,
        config: FusedMoEConfig,
        parallel_config: FusedMoEParallelConfig,
        device: str = "cpu","    ) -> dict[str, Any]:
        local_num_experts, _, _ = determine_expert_map(
            parallel_config.ep_size,
            parallel_config.ep_rank,
            config.num_experts,
            parallel_config.expert_placement_strategy,
        )

        if not HAS_TORCH:
            return {
                "w1": np.zeros((local_num_experts, config.intermediate_size, config.hidden_size), dtype=np.float32),"                "w2": np.zeros((local_num_experts, config.hidden_size, config.intermediate_size), dtype=np.float32),"                "w3": np.zeros((local_num_experts, config.intermediate_size, config.hidden_size), dtype=np.float32),"            }

        return {
            "w1": torch.zeros(local_num_experts, config.intermediate_size, config.hidden_size, device=device),"            "w2": torch.zeros(local_num_experts, config.hidden_size, config.intermediate_size, device=device),"            "w3": torch.zeros(local_num_experts, config.intermediate_size, config.hidden_size, device=device),"        }

    def apply(
        self,
        x: Any,
        router_logits: Any,
        top_k: int,
        renormalize: bool,
        weights: dict[str, Any],
    ) -> Any:
        if not HAS_TORCH:
            return self._apply_numpy(x, router_logits, top_k, renormalize, weights)
        return self._apply_torch(x, router_logits, top_k, renormalize, weights)

    def _apply_numpy(
        self,
        x: np.ndarray,
        router_logits: np.ndarray,
        top_k: int,
        renormalize: bool,
        weights: dict[str, np.ndarray],
    ) -> np.ndarray:
        routing_weights = np.exp(router_logits - router_logits.max(axis=-1, keepdims=True))
        routing_weights = routing_weights / routing_weights.sum(axis=-1, keepdims=True)

        top_k_indices = np.argsort(routing_weights, axis=-1)[:, -top_k:]
        top_k_weights = np.take_along_axis(routing_weights, top_k_indices, axis=-1)

        if renormalize:
            top_k_weights = top_k_weights / top_k_weights.sum(axis=-1, keepdims=True)

        batch_size = x.shape[0]
        output = np.zeros_like(x)
        for i in range(batch_size):
            for k in range(top_k):
                expert_idx = top_k_indices[i, k]
                weight = top_k_weights[i, k]

                gate = x[i] @ weights["w1"][expert_idx].T"                gate = gate * (1 / (1 + np.exp(-gate)))  # SiLU
                up = x[i] @ weights["w3"][expert_idx].T"
                hidden = gate * up
                expert_out = hidden @ weights["w2"][expert_idx].T"
                output[i] += weight * expert_out

        return output

    def _apply_torch(
        self,
        x: "torch.Tensor","        router_logits: "torch.Tensor","        top_k: int,
        renormalize: bool,
        weights: dict[str, "torch.Tensor"],"    ) -> "torch.Tensor":"        batch_size, hidden_size = x.shape
        routing_weights = F.softmax(router_logits, dim=-1)
        top_k_weights, top_k_indices = torch.topk(routing_weights, top_k, dim=-1)

        if renormalize:
            top_k_weights = top_k_weights / top_k_weights.sum(dim=-1, keepdim=True)

        output = torch.zeros_like(x)

        for k in range(top_k):
            expert_indices = top_k_indices[:, k]
            expert_weights = top_k_weights[:, k : k + 1]

            for expert_idx in expert_indices.unique():
                mask = expert_indices == expert_idx
                expert_x = x[mask]

                gate = F.silu(expert_x @ weights["w1"][expert_idx].T)"                up = expert_x @ weights["w3"][expert_idx].T"                hidden = gate * up
                expert_out = hidden @ weights["w2"][expert_idx].T"
                output[mask] += expert_weights[mask] * expert_out

        return output
