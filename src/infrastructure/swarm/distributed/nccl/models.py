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
Models and configuration for NCCL communication.
"""

from dataclasses import dataclass
from enum import Enum, auto


class ReduceOp(Enum):
    """NCCL reduction operations."""

    SUM = auto()
    PROD = auto()
    MAX = auto()
    MIN = auto()
    AVG = auto()  # Average (sum / world_size)


@dataclass
class NCCLConfig:
    """
    Configuration for NCCL communicator.
    """

    # Timeout settings
    timeout_seconds: float = 1800.0  # 30 minutes default
    timeout_per_step: float = 60.0  # Per-operation timeout

    # Retry settings (beyond vLLM)
    max_retries: int = 3
    retry_delay_seconds: float = 1.0
    retry_backoff_factor: float = 2.0

    # Performance settings
    use_custom_allreduce: bool = True
    custom_allreduce_threshold: int = 1 << 20  # 1MB

    # CUDA settings
    use_cuda_graphs: bool = True

    # Debug settings
    debug_mode: bool = False
    log_all_ops: bool = False


@dataclass
class NCCLStats:
    """Statistics for NCCL operations."""

    all_reduce_count: int = 0
    all_gather_count: int = 0
    reduce_scatter_count: int = 0
    send_count: int = 0
    recv_count: int = 0
    barrier_count: int = 0
    retry_count: int = 0
    total_bytes: int = 0
    total_time_ms: float = 0.0
    errors: int = 0
