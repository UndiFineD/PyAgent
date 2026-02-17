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


Dispatcher.py module.

from __future__ import annotations

from typing import Callable

import numpy as np


class SparseDispatcher:
    """Sparse dispatcher for token-to-expert assignment.
    def __init__(
        self,
        num_experts: int,
        top_k: int,
        capacity_factor: float = 1.25,
    ) -> None:
        self.num_experts = num_experts
        self.top_k = top_k
        self.capacity_factor = capacity_factor

    def dispatch(
        self,
        x: np.ndarray,
        expert_indices: np.ndarray,
        expert_weights: np.ndarray,
    ) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
        batch_size = x.shape[0]
        capacity = int(batch_size * self.top_k * self.capacity_factor / self.num_experts)

        expert_inputs = []
        expert_positions = []
        expert_weights_list = []

        for expert_idx in range(self.num_experts):
            mask = (expert_indices == expert_idx).any(axis=-1)
            positions = np.where(mask)[0]

            if len(positions) > capacity:
                positions = positions[:capacity]

            if positions.size > 0:
                expert_inputs.append(x[positions])
                expert_positions.append(positions)

                weights = []
                for pos in positions:
                    k_idx = np.where(expert_indices[pos] == expert_idx)[0]
                    if k_idx.size > 0:
                        weights.append(expert_weights[pos, k_idx[0]])
                    else:
                        weights.append(0.0)
                expert_weights_list.append(np.array(weights))
            else:
                expert_inputs.append(np.zeros((0, x.shape[-1]), dtype=x.dtype))
                expert_positions.append(np.array([], dtype=np.int64))
                expert_weights_list.append(np.array([]))

        return expert_inputs, expert_positions, expert_weights_list

    def combine(
        self,
        expert_outputs: list[np.ndarray],
        expert_positions: list[np.ndarray],
        expert_weights_list: list[np.ndarray],
        output_shape: tuple[int, ...],
    ) -> np.ndarray:
        output = np.zeros(output_shape, dtype=expert_outputs[0].dtype if expert_outputs else np.float32)

        for expert_idx, (outputs, positions, weights) in enumerate(
            zip(expert_outputs, expert_positions, expert_weights_list)
        ):
            if positions.size > 0:
                for i, pos in enumerate(positions):
                    output[pos] += weights[i] * outputs[i]

        return output


class DenseDispatcher:
    """Dense dispatcher using matrix operations.
    def __init__(self, num_experts: int, top_k: int) -> None:
        self.num_experts = num_experts
        self.top_k = top_k

    def dispatch_and_combine(
        self,
        x: np.ndarray,
        expert_indices: np.ndarray,
        expert_weights: np.ndarray,
        expert_fn: Callable[[int, np.ndarray], np.ndarray],
    ) -> np.ndarray:
        output = np.zeros_like(x)

        for k in range(self.top_k):
            for expert_idx in range(self.num_experts):
                mask = expert_indices[:, k] == expert_idx
                if mask.any():
                    expert_input = x[mask]
                    expert_output = expert_fn(expert_idx, expert_input)
                    output[mask] += expert_weights[mask, k : k + 1] * expert_output

        return output
