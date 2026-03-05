# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Distributed infrastructure for parallel inference.

Phase 33 modules:
- TensorParallelGroup: Tensor parallel coordination
- NCCLCommunicator: NCCL collective operations
"""

from .TensorParallelGroup import (
    GroupCoordinator,
    ParallelConfig,
    ParallelMode,
    RankInfo,
    TensorParallelGroup,
)
from .NCCLCommunicator import (
    CustomAllReduce,
    NCCLCommunicator,
    NCCLConfig,
    ReduceOp,
)

__all__ = [
    # TensorParallelGroup
    "GroupCoordinator",
    "ParallelConfig",
    "ParallelMode",
    "RankInfo",
    "TensorParallelGroup",
    # NCCLCommunicator
    "CustomAllReduce",
    "NCCLCommunicator",
    "NCCLConfig",
    "ReduceOp",
]
