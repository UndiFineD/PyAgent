# Phase 29: Execution Context, Batching & Async Streaming
# Inspired by vLLM's forward_context.py, input_batch.py, async_utils.py

from .ForwardContext import (
    ForwardContext,
    BatchDescriptor,
    DPMetadata,
    set_forward_context,
    get_forward_context,
    create_forward_context,
    ForwardTimingTracker,
)

from .InputBatch import (
    InputBatch,
    InputBuffers,
    SamplingMetadata,
    BatchBuilder,
)

from .CpuGpuBufferPool import (
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

from .AsyncOutputHandler import (
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

from .CUDAGraphConfig import (
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
