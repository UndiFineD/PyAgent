# Phase 29: Execution Context, Batching & Async Streaming
# Inspired by vLLM's forward_context.py, input_batch.py, async_utils.py

from .forward_context import (
    ForwardContext,
    BatchDescriptor,
    DPMetadata,
    set_forward_context,
    get_forward_context,
    create_forward_context,
    ForwardTimingTracker,
)

from .input_batch import (
    InputBatch,
    InputBuffers,
    SamplingMetadata,
    BatchBuilder,
)

from .cpu_gpu_buffer_pool import (
    CpuGpuBuffer,
    UvaBufferPool,
    MemoryPlacement,
    PinnedMemoryManager,
    copy_with_indices,
    scatter_with_indices,
    pad_to_multiple,
    compute_cumsum_offsets,
    flatten_with_offsets,
    split_by_offsets,
)

from .async_output_handler import (
    AsyncState,
    CudaEvent,
    CudaStream,
    AsyncOutput,
    async_copy_to_np,
    async_copy_batch,
    AsyncBarrier,
    async_barrier,
    AsyncOutputHandler,
    DoubleBuffer,
)

from .cuda_graph_config import (
    CUDAGraphMode,
    CUDAGraphConfig,
    CUDAGraphEntry,
    CUDAGraphRegistry,
    CUDAGraphManager,
)

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
