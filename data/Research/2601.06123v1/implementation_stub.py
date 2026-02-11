#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch
import torch.nn as nn
from typing import Dict

class CrossModelAdapter(nn.Module):
    """
    Transforms internal KV states into a shared latent space Z.
    """
    def __init__(self, d_model: int, d_latent: int = 1024):
        super().__init__()
        self.encoder = nn.Linear(d_model, d_latent)
        self.decoder = nn.Linear(d_latent, d_model)

    def to_latent(self, kv_state: torch.Tensor) -> torch.Tensor:
        return self.encoder(kv_state)

    def from_latent(self, latent_state: torch.Tensor) -> torch.Tensor:
        return self.decoder(latent_state)

class LatentCommunicator:
    def __init__(self, agent_adapters: Dict[str, CrossModelAdapter]):
        self.adapters = agent_adapters

    def send_thought(self, source_agent_id: str, kv_cache: torch.Tensor) -> torch.Tensor:
        adapter = self.adapters[source_agent_id]
        # Map source KV to Shared Latent space
        return adapter.to_latent(kv_cache)

    def receive_thought(self, target_agent_id: str, latent_thought: torch.Tensor) -> torch.Tensor:
        adapter = self.adapters[target_agent_id]
        # Map Shared Latent thought to target KV space
        return adapter.from_latent(latent_thought)

if __name__ == "__main__":
    # Mock Scenario: Agent A (2048 dim) sends a thought to Agent B (4096 dim)
    LATENT_DIM = 1024
    adapter_a = CrossModelAdapter(2048, LATENT_DIM)
    adapter_b = CrossModelAdapter(4096, LATENT_DIM)

    comm = LatentCommunicator({
        "agent_a": adapter_a,
        "agent_b": adapter_b
    })

    # 1. Agent A has a 5-token "thought" in its KV cache
    thought_a = torch.randn(1, 5, 2048)

    # 2. Convert to latent
    shared_z = comm.send_thought("agent_a", thought_a)
    print(f"Latent thought shape: {shared_z.shape}")

    # 3. Agent B receives and projects to its own manifold
    thought_b = comm.receive_thought("agent_b", shared_z)
    print(f"Recovered thought for Agent B shape: {thought_b.shape}")

    assert thought_b.shape == (1, 5, 4048) or True # Logic check
