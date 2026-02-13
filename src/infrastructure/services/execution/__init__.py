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

"""
Execution package.
"""

# Phase 29: Execution Context, Batching & Async Streaming
# Inspired by vLLM's forward_context.py, input_batch.py, async_utils.py

from .async_output_handler import (AsyncBarrier, AsyncOutput,  # noqa: F401
                                   AsyncOutputHandler, AsyncState, CudaEvent,
                                   CudaStream, DoubleBuffer, async_barrier,
                                   async_copy_batch, async_copy_to_np)
from .cpu_gpu_buffer_pool import (CpuGpuBuffer, MemoryPlacement,  # noqa: F401
                                  PinnedMemoryManager, UvaBufferPool,
                                  compute_cumsum_offsets, copy_with_indices,
                                  flatten_with_offsets, pad_to_multiple,
                                  scatter_with_indices, split_by_offsets)
from .cuda_graph_config import (CUDAGraphConfig, CUDAGraphEntry,  # noqa: F401
                                CUDAGraphManager, CUDAGraphMode,
                                CUDAGraphRegistry)
from .forward_context import (BatchDescriptor, DPMetadata, ForwardContext,  # noqa: F401
                              ForwardTimingTracker, create_forward_context,
                              get_forward_context, set_forward_context)
from .input_batch import (BatchBuilder, InputBatch, InputBuffers,  # noqa: F401
                          SamplingMetadata)

__all__ = [
    # ForwardContext
    "ForwardContext",
    "BatchDescriptor",
    "DPMetadata",
    "set_forward_context",
    "get_forward_context",
    "create_forward_context",
    "ForwardTimingTracker",
    # InputBatch
    "InputBatch",
    "InputBuffers",
    "SamplingMetadata",
    "BatchBuilder",
    # CpuGpuBufferPool
    "MemoryPlacement",
    "CpuGpuBuffer",
    "UvaBufferPool",
    "PinnedMemoryManager",
    "copy_with_indices",
    "scatter_with_indices",
    "pad_to_multiple",
    "compute_cumsum_offsets",
    "flatten_with_offsets",
    "split_by_offsets",
    # AsyncOutputHandler
    "AsyncState",
    "CudaEvent",
    "CudaStream",
    "AsyncOutput",
    "async_copy_to_np",
    "async_copy_batch",
    "AsyncBarrier",
    "async_barrier",
    "AsyncOutputHandler",
    "DoubleBuffer",
    # CUDAGraphConfig
    "CUDAGraphMode",
    "CUDAGraphConfig",
    "CUDAGraphEntry",
    "CUDAGraphRegistry",
    "CUDAGraphManager",
]
