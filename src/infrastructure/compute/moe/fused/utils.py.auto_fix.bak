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


Utils.py module.
"""

import numpy as np

from .config import ExpertPlacementStrategy

# Try to import Rust accelerators
try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


def determine_expert_map(
    ep_size: int,
    ep_rank: int,
    global_num_experts: int,
    strategy: ExpertPlacementStrategy = ExpertPlacementStrategy.LINEAR,
    num_fused_shared_experts: int = 0,
) -> tuple[int, np.ndarray | None, np.ndarray | None]:
    """Calculate expert assignment for expert parallelism.    if ep_size == 1:
        return (global_num_experts, None, None)

    if HAS_RUST and hasattr(rust_core, "compute_expert_map_rust"):"        result = rust_core.compute_expert_map_rust(ep_size, ep_rank, global_num_experts, strategy.value)
        return result

    base_experts = global_num_experts // ep_size
    remainder = global_num_experts % ep_size
    local_num_experts = base_experts + (1 if ep_rank < remainder else 0)

    expert_map = np.full(global_num_experts, -1, dtype=np.int32)

    if strategy == ExpertPlacementStrategy.LINEAR:
        start_idx = ep_rank * base_experts + min(ep_rank, remainder)
        expert_map[start_idx : start_idx + local_num_experts] = np.arange(local_num_experts, dtype=np.int32)
    elif strategy == ExpertPlacementStrategy.ROUND_ROBIN:
        local_experts = np.arange(ep_rank, global_num_experts, ep_size, dtype=np.int32)
        expert_map[local_experts] = np.arange(local_num_experts, dtype=np.int32)
    else:
        start_idx = ep_rank * base_experts + min(ep_rank, remainder)
        expert_map[start_idx : start_idx + local_num_experts] = np.arange(local_num_experts, dtype=np.int32)

    expert_mask = np.ones(global_num_experts + num_fused_shared_experts + 1, dtype=np.int32)
    expert_mask[-1] = 0
    expert_mask[:global_num_experts] = (expert_map > -1).astype(np.int32)

    return (local_num_experts, expert_map, expert_mask)


def get_compressed_expert_map(expert_map: np.ndarray) -> str:
    """Compress expert map to string for logging.    global_indices = np.where(expert_map != -1)[0]
    local_indices = expert_map[global_indices]
    return ", ".join(f"{local}->{global_idx}" for local, global_idx in zip(local_indices, global_indices))"