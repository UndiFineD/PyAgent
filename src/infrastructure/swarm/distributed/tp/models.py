#!/usr/bin/env python3
# Refactored by copilot-placeholder
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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Models and configuration for tensor parallelism.
"""

import logging
import os
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class ParallelMode(Enum):
    """Parallelism modes."""

    DATA = auto()  # Data parallel
    TENSOR = auto()  # Tensor parallel
    PIPELINE = auto()  # Pipeline parallel
    EXPERT = auto()  # Expert parallel (MoE)
    CONTEXT = auto()  # Context parallel (sequence)


@dataclass
class ParallelConfig:
    """
    Configuration for distributed parallelism.

    Defines the parallelism strategy across dimensions.
    """

    world_size: int = 1
    tensor_parallel_size: int = 1
    pipeline_parallel_size: int = 1
    data_parallel_size: int = 1
    expert_parallel_size: int = 1
    context_parallel_size: int = 1

    # Process group settings
    backend: str = "nccl"  # nccl, gloo, mpi
    init_method: str | None = None

    def __post_init__(self):
        # Validate configuration
        expected_world = self.tensor_parallel_size * self.pipeline_parallel_size * self.data_parallel_size
        if self.world_size == 1 and expected_world > 1:
            self.world_size = expected_world
        elif self.world_size != expected_world and expected_world > 1:
            logger.warning(f"World size {self.world_size} != TP*PP*DP = {expected_world}")

    @classmethod
    def from_env(cls) -> "ParallelConfig":
        """Create configuration from environment variables."""
        return cls(
            world_size=int(os.environ.get("WORLD_SIZE", 1)),
            tensor_parallel_size=int(os.environ.get("TENSOR_PARALLEL_SIZE", 1)),
            pipeline_parallel_size=int(os.environ.get("PIPELINE_PARALLEL_SIZE", 1)),
            data_parallel_size=int(os.environ.get("DATA_PARALLEL_SIZE", 1)),
            backend=os.environ.get("DISTRIBUTED_BACKEND", "nccl"),
        )


@dataclass
class RankInfo:
    """
    Information about a rank's position in the parallel topology.
    """

    global_rank: int
    local_rank: int
    tp_rank: int  # Tensor parallel rank
    pp_rank: int  # Pipeline parallel rank
    dp_rank: int  # Data parallel rank
    node_rank: int = 0

    @classmethod
    def compute(
        cls,
        global_rank: int,
        config: ParallelConfig,
    ) -> "RankInfo":
        """Compute rank information from global rank and config."""
        tp_size = config.tensor_parallel_size
        pp_size = config.pipeline_parallel_size

        # Compute DP, PP, TP ranks from global rank
        # Layout: [DP][PP][TP]
        tp_rank = global_rank % tp_size
        pp_rank = (global_rank // tp_size) % pp_size
        dp_rank = global_rank // (tp_size * pp_size)

        # Local rank within node
        local_rank = int(os.environ.get("LOCAL_RANK", global_rank % 8))
        node_rank = global_rank // 8

        return cls(
            global_rank=global_rank,
            local_rank=local_rank,
            tp_rank=tp_rank,
            pp_rank=pp_rank,
            dp_rank=dp_rank,
            node_rank=node_rank,
        )
