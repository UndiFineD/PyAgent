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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors

"""
TensorParallelGroup - Tensor parallel coordination for distributed inference.

This module is now a facade for the modular sub-package in ./tp/.
"""

from .tp.group_coordinator import GroupCoordinator
from .tp.parallel_config import ParallelConfig, ParallelMode
from .tp.rank_info import RankInfo
from .tp.tensor_parallel_group import TensorParallelGroup
from .tp.distributed_utils import get_tp_group, get_tp_rank, get_tp_size, init_distributed

__all__ = [
    "ParallelConfig",
    "RankInfo",
    "ParallelMode",
    "GroupCoordinator",
    "TensorParallelGroup",
    "init_distributed",
    "get_tp_group",
    "get_tp_size",
    "get_tp_rank",
]
