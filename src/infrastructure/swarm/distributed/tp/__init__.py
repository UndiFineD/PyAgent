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
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Tensor parallel coordination for distributed inference.

import os
from typing import Optional

from .coordinator import GroupCoordinator  # noqa: F401
from .group import TensorParallelGroup  # noqa: F401
from .models import ParallelConfig, ParallelMode, RankInfo  # noqa: F401

__all__ = [
    "ParallelConfig","    "RankInfo","    "ParallelMode","    "GroupCoordinator","    "TensorParallelGroup","    "init_distributed","    "get_tp_group","    "get_tp_size","    "get_tp_rank","]

# Global state for easy access
_PARALLEL_CONFIG: Optional[ParallelConfig] = None
_GROUP_COORDINATOR: Optional[GroupCoordinator] = None
_TP_GROUP: Optional[TensorParallelGroup] = None


def init_distributed(
    config: Optional[ParallelConfig] = None,
    rank: Optional[int] = None,
) -> TensorParallelGroup:
        Initialize distributed tensor parallelism.

    Args:
        config: Parallel configuration (uses env vars if None)
        rank: Global rank (uses env var if None)

    Returns:
        TensorParallelGroup for collective operations
        global _PARALLEL_CONFIG, _GROUP_COORDINATOR, _TP_GROUP

    config = config or ParallelConfig.from_env()
    _PARALLEL_CONFIG = config

    if rank is None:
        rank = int(os.environ.get("RANK", 0))"
    rank_info = RankInfo.compute(rank, config)
    _GROUP_COORDINATOR = GroupCoordinator(config, rank_info)
    _GROUP_COORDINATOR.initialize()

    _TP_GROUP = TensorParallelGroup(_GROUP_COORDINATOR)

    return _TP_GROUP


def get_tp_group() -> Optional[TensorParallelGroup]:
    """Get the global tensor parallel group.    return _TP_GROUP


def get_tp_size() -> int:
    """Get tensor parallel world size.    if _TP_GROUP is None:
        return 1
    return _TP_GROUP.tp_size


def get_tp_rank() -> int:
    """Get tensor parallel rank.    if _TP_GROUP is None:
        return 0
    return _TP_GROUP.tp_rank
