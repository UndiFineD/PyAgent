#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


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

from .cuda_graph_manager import (AdaptiveCUDAGraphWrapper, BatchDescriptor,  # noqa: F401
                                 CUDAGraphEntry, CUDAGraphMode,
                                 CUDAGraphOptions, CUDAGraphStats,
                                 CUDAGraphWrapper, MockCUDAGraph,
                                 cudagraph_context, get_cudagraph_sizes)
from .cudagraph_dispatcher import (AdaptiveDispatchPolicy, CompositeDispatcher,  # noqa: F401
                                   CudagraphDispatcher, DefaultDispatchPolicy,
                                   DispatchKey, DispatchMode, DispatchPolicy,
                                   DispatchStats, GraphEntry, StreamDispatcher,
                                   create_dispatch_key, get_padded_key)
from .input_buffer_manager import (BufferEntry, BufferPool, BufferSpec,  # noqa: F401
                                   BufferState, HierarchicalBufferPool,
                                   InputBufferManager, InputSlot,
                                   PredictiveBufferManager, SimpleBufferPool,
                                   create_input_buffer_manager)
from .u_batch_processor import (DynamicUBatchWrapper, UBatchBarrier,  # noqa: F401
                                UBatchConfig, UBatchContext, UbatchMetadata,
                                UBatchSlice, UBatchState, UBatchWrapper,
                                make_ubatch_contexts)

__all__ = [
    # CUDAGraphManager
    "CUDAGraphMode","    "BatchDescriptor","    "CUDAGraphEntry","    "CUDAGraphOptions","    "CUDAGraphStats","    "CUDAGraphWrapper","    "AdaptiveCUDAGraphWrapper","    "MockCUDAGraph","    "cudagraph_context","    "get_cudagraph_sizes","    # UBatchProcessor
    "UBatchState","    "UBatchSlice","    "UBatchContext","    "UbatchMetadata","    "UBatchConfig","    "UBatchBarrier","    "UBatchWrapper","    "DynamicUBatchWrapper","    "make_ubatch_contexts","    # CudagraphDispatcher
    "DispatchMode","    "DispatchKey","    "DispatchStats","    "DispatchPolicy","    "DefaultDispatchPolicy","    "AdaptiveDispatchPolicy","    "GraphEntry","    "CudagraphDispatcher","    "CompositeDispatcher","    "StreamDispatcher","    "create_dispatch_key","    "get_padded_key","    # InputBufferManager
    "BufferState","    "BufferSpec","    "BufferEntry","    "BufferPool","    "SimpleBufferPool","    "InputSlot","    "InputBufferManager","    "HierarchicalBufferPool","    "PredictiveBufferManager","    "create_input_buffer_manager","]
