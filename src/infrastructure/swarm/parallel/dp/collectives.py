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
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Async collective operations for data parallel coordination.
"""

from __future__ import annotations

import asyncio
import logging

try:
    import torch
    import torch.distributed as dist
    HAS_TORCH_DIST = True
except ImportError:
    HAS_TORCH_DIST = False

from src.infrastructure.swarm.parallel.dp.engine import DPEngineCoreProc

logger = logging.getLogger(__name__)


async def dp_collective_all_reduce(
    values: list[float], coordinator: DPEngineCoreProc, operation: str = "sum"
) -> list[float]:
    """
    Async all-reduce across DP ranks.

    Beyond vLLM: Async collective operations.
    """
    if not HAS_TORCH_DIST or not dist.is_initialized():
        # Fallback for non-distributed or local runs
        await asyncio.sleep(0)
        return values

    try:
        # Move to torch tensor for distributed operation
        tensor = torch.tensor(values, dtype=torch.float32)

        # Map operation
        reduce_op = dist.ReduceOp.SUM
        if operation.lower() == "min":
            reduce_op = dist.ReduceOp.MIN
        elif operation.lower() == "max":
            reduce_op = dist.ReduceOp.MAX
        elif operation.lower() == "product":
            reduce_op = dist.ReduceOp.PRODUCT

        # Run all-reduce in a thread to keep async loop responsive if needed,
        # but torch.distributed usually has async_op=True support
        dist.all_reduce(tensor, op=reduce_op)

        return tensor.tolist()
    except Exception as e:
        logger.error(f"DP all-reduce failed: {e}")
        return values
