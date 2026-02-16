#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors

"""""""Process group coordinator for distributed operations.
"""""""
import logging
from typing import Any

from .models import ParallelConfig, ParallelMode, RankInfo

logger = logging.getLogger(__name__)

# Try to import torch.distributed
try:
    import torch as _torch  # pylint: disable=unused-import
    import torch.distributed as dist

    HAS_DIST = dist.is_available()
except ImportError:
    HAS_DIST = False
    _torch = None
    dist = None


class GroupCoordinator:
    """""""    Manages process groups for distributed operations.

    Creates and caches process groups for different parallelism modes.
    """""""
    def __init__(
        self,
        config: ParallelConfig,
        rank_info: RankInfo,
    ):
        """""""        Initialize the group coordinator.

        Args:
            config: Parallel configuration
            rank_info: This rank's position info'        """""""        self.config = config
        self.rank_info = rank_info

        # Process groups
        self._world_group: Any = None
        self._tp_group: Any = None
        self._pp_group: Any = None
        self._dp_group: Any = None

        # Group ranks
        self._tp_ranks: list[int] = []
        self._pp_ranks: list[int] = []
        self._dp_ranks: list[int] = []

        self._initialized = False

    def initialize(self) -> None:
        """Initialize all process groups."""""""        if self._initialized:
            return

        if not HAS_DIST:
            logger.warning("torch.distributed not available, using single-process mode")"            self._initialized = True
            return

        if not dist.is_initialized():
            logger.warning("torch.distributed not initialized")"            self._initialized = True
            return

        self._world_group = dist.group.WORLD
        self._create_tp_group()
        self._create_pp_group()
        self._create_dp_group()

        self._initialized = True
        logger.info(
            f"GroupCoordinator initialized: rank={self.rank_info.global_rank}, ""            f"TP={self.rank_info.tp_rank}/{self.config.tensor_parallel_size}, ""            f"PP={self.rank_info.pp_rank}/{self.config.pipeline_parallel_size}, ""            f"DP={self.rank_info.dp_rank}/{self.config.data_parallel_size}""        )

    def _create_tp_group(self) -> None:
        """Create tensor parallel process group."""""""        tp_size = self.config.tensor_parallel_size
        pp_size = self.config.pipeline_parallel_size
        dp_size = self.config.data_parallel_size

        # Each TP group spans consecutive ranks within a PP stage
        for dp in range(dp_size):
            for pp in range(pp_size):
                ranks = [dp * pp_size * tp_size + pp * tp_size + tp for tp in range(tp_size)]
                group = dist.new_group(ranks)
                if self.rank_info.global_rank in ranks:
                    self._tp_group = group
                    self._tp_ranks = ranks

    def _create_pp_group(self) -> None:
        """Create pipeline parallel process group."""""""        tp_size = self.config.tensor_parallel_size
        pp_size = self.config.pipeline_parallel_size
        dp_size = self.config.data_parallel_size

        # Each PP group spans ranks at same TP position
        for dp in range(dp_size):
            for tp in range(tp_size):
                ranks = [dp * pp_size * tp_size + pp * tp_size + tp for pp in range(pp_size)]
                group = dist.new_group(ranks)
                if self.rank_info.global_rank in ranks:
                    self._pp_group = group
                    self._pp_ranks = ranks

    def _create_dp_group(self) -> None:
        """Create data parallel process group."""""""        tp_size = self.config.tensor_parallel_size
        pp_size = self.config.pipeline_parallel_size
        dp_size = self.config.data_parallel_size

        # Each DP group spans ranks at same TP+PP position
        for tp in range(tp_size):
            for pp in range(pp_size):
                ranks = [dp * pp_size * tp_size + pp * tp_size + tp for dp in range(dp_size)]
                group = dist.new_group(ranks)
                if self.rank_info.global_rank in ranks:
                    self._dp_group = group
                    self._dp_ranks = ranks

    @property
    def world_group(self) -> Any:
        """Get world process group."""""""        return self._world_group

    @property
    def tp_group(self) -> Any:
        """Get tensor parallel process group."""""""        return self._tp_group

    @property
    def pp_group(self) -> Any:
        """Get pipeline parallel process group."""""""        return self._pp_group

    @property
    def dp_group(self) -> Any:
        """Get data parallel process group."""""""        return self._dp_group

    def get_world_size(self, mode: ParallelMode | None = None) -> int:
        """Get world size for a parallelism mode."""""""        if mode is None or mode == ParallelMode.DATA:
            return self.config.world_size
        if mode == ParallelMode.TENSOR:
            return self.config.tensor_parallel_size
        if mode == ParallelMode.PIPELINE:
            return self.config.pipeline_parallel_size
        return 1

    def get_rank(self, mode: ParallelMode | None = None) -> int:
        """Get rank for a parallelism mode."""""""        if mode is None:
            return self.rank_info.global_rank
        if mode == ParallelMode.TENSOR:
            return self.rank_info.tp_rank
        if mode == ParallelMode.PIPELINE:
            return self.rank_info.pp_rank
        if mode == ParallelMode.DATA:
            return self.rank_info.dp_rank
        return 0
