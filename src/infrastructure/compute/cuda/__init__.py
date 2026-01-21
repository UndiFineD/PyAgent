"""
CUDA Graph and Compilation Infrastructure.

Phase 36: CUDA Graph & Compilation subsystem providing:
- CUDAGraphManager: Graph capture and replay
- UBatchProcessor: Micro-batch processing
- CudagraphDispatcher: Dispatch logic
- InputBufferManager: Buffer staging

Beyond vLLM:
- Adaptive graph selection
- Predictive pre-warming
- Multi-stream dispatch
"""

from .cuda_graph_manager import (
    CUDAGraphMode,
    BatchDescriptor,
    CUDAGraphEntry,
    CUDAGraphOptions,
    CUDAGraphStats,
    CUDAGraphWrapper,
    AdaptiveCUDAGraphWrapper,
    MockCUDAGraph,
    cudagraph_context,
    get_cudagraph_sizes,
)

from .u_batch_processor import (
    UBatchState,
    UBatchSlice,
    UBatchContext,
    UbatchMetadata,
    UBatchConfig,
    UBatchBarrier,
    UBatchWrapper,
    DynamicUBatchWrapper,
    make_ubatch_contexts,
)

from .cudagraph_dispatcher import (
    DispatchMode,
    DispatchKey,
    DispatchStats,
    DispatchPolicy,
    DefaultDispatchPolicy,
    AdaptiveDispatchPolicy,
    GraphEntry,
    CudagraphDispatcher,
    CompositeDispatcher,
    StreamDispatcher,
    create_dispatch_key,
    get_padded_key,
)

from .input_buffer_manager import (
    BufferState,
    BufferSpec,
    BufferEntry,
    BufferPool,
    SimpleBufferPool,
    InputSlot,
    InputBufferManager,
    HierarchicalBufferPool,
    PredictiveBufferManager,
    create_input_buffer_manager,
)

__all__ = [
    # CUDAGraphManager
    "CUDAGraphMode",
    "BatchDescriptor",
    "CUDAGraphEntry",
    "CUDAGraphOptions",
    "CUDAGraphStats",
    "CUDAGraphWrapper",
    "AdaptiveCUDAGraphWrapper",
    "MockCUDAGraph",
    "cudagraph_context",
    "get_cudagraph_sizes",
    # UBatchProcessor
    "UBatchState",
    "UBatchSlice",
    "UBatchContext",
    "UbatchMetadata",
    "UBatchConfig",
    "UBatchBarrier",
    "UBatchWrapper",
    "DynamicUBatchWrapper",
    "make_ubatch_contexts",
    # CudagraphDispatcher
    "DispatchMode",
    "DispatchKey",
    "DispatchStats",
    "DispatchPolicy",
    "DefaultDispatchPolicy",
    "AdaptiveDispatchPolicy",
    "GraphEntry",
    "CudagraphDispatcher",
    "CompositeDispatcher",
    "StreamDispatcher",
    "create_dispatch_key",
    "get_padded_key",
    # InputBufferManager
    "BufferState",
    "BufferSpec",
    "BufferEntry",
    "BufferPool",
    "SimpleBufferPool",
    "InputSlot",
    "InputBufferManager",
    "HierarchicalBufferPool",
    "PredictiveBufferManager",
    "create_input_buffer_manager",
]
