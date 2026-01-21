# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
TensorParallelGroup - Tensor parallel coordination for distributed inference.

This module is now a facade for the modular sub-package in ./tp/.
"""

from .tp import (
    ParallelConfig,
    RankInfo,
    ParallelMode,
    GroupCoordinator,
    TensorParallelGroup,
    init_distributed,
    get_tp_group,
    get_tp_size,
    get_tp_rank,
)

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
