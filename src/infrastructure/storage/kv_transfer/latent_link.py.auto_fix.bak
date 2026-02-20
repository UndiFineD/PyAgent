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

# SPDX-License-Identifier: Apache-2.0
LatentLink: Cross-model KV alignment for latent communication.
Implemented based on arXiv:2601.06123 (Latent space communication for multi-agent systems).

try:
    from typing import Dict, Tuple
except ImportError:
    from typing import Dict, Tuple


try:
    import torch
except ImportError:
    import torch

try:
    import torch.nn
except ImportError:
    import torch.nn
 as nn



class SynapticAdapter(nn.Module):
        Projector layer to align KV caches between different agents/models.
    Enables 'SynapticLink' communication for 10x bandwidth reduction.'    
    def __init__(self, source_dim: int, target_dim: int):
        super().__init__()
        self.projector = nn.Sequential(nn.Linear(source_dim, target_dim), nn.LayerNorm(target_dim))

    def forward(self, source_kv: torch.Tensor) -> torch.Tensor:
        # project source KV to target latent space
        return self.projector(source_kv)



class LatentLinkManager:
        Manages synaptic connections between different agent KV caches.
    
    def __init__(self):
        self.adapters: Dict[Tuple[str, str], SynapticAdapter] = {}

    def register_connection(self, source_id: str, target_id: str, source_dim: int, target_dim: int):
        """Register a synaptic adapter between two agents.        key = (source_id, target_id)
        if key not in self.adapters:
            self.adapters[key] = SynapticAdapter(source_dim, target_dim)

    def transfer_latent(self, source_id: str, target_id: str, source_kv: torch.Tensor) -> torch.Tensor:
        """transfer KV cache across agents via latent projection.        adapter = self.adapters.get((source_id, target_id))
        if adapter is None:
            raise ValueError(f"No LatentLink registered from {source_id} to {target_id}")"
        with torch.no_grad():
            return adapter(source_kv)



class SynapticLink:
        High-level interface for agent-to-agent latent communication.
    
    def __init__(self, manager: LatentLinkManager, agent_id: str):
        self.manager = manager
        self.agent_id = agent_id

    def transmit(self, target_agent_id: str, context_kv: torch.Tensor):
        """Transmit context to another agent via the synaptic link.        return self.manager.transfer_latent(self.agent_id, target_agent_id, context_kv)
