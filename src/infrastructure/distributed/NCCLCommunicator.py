# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
NCCLCommunicator - Pure Python NCCL wrapper for collective operations.

This module is now a facade for the modular sub-package in ./nccl/.
"""

from .nccl import (
    NCCLConfig,
    NCCLStats,
    ReduceOp,
    NCCLCommunicator,
    CustomAllReduce,
)

__all__ = [
    "NCCLConfig",
    "NCCLStats",
    "ReduceOp",
    "NCCLCommunicator",
    "CustomAllReduce",
]
