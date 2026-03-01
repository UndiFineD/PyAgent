# __init__

**File**: `src\infrastructure\cuda\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 41 imports  
**Lines**: 115  
**Complexity**: 0 (simple)

## Overview

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

## Dependencies

**Imports** (41):
- `CUDAGraphManager.AdaptiveCUDAGraphWrapper`
- `CUDAGraphManager.BatchDescriptor`
- `CUDAGraphManager.CUDAGraphEntry`
- `CUDAGraphManager.CUDAGraphMode`
- `CUDAGraphManager.CUDAGraphOptions`
- `CUDAGraphManager.CUDAGraphStats`
- `CUDAGraphManager.CUDAGraphWrapper`
- `CUDAGraphManager.MockCUDAGraph`
- `CUDAGraphManager.cudagraph_context`
- `CUDAGraphManager.get_cudagraph_sizes`
- `CudagraphDispatcher.AdaptiveDispatchPolicy`
- `CudagraphDispatcher.CompositeDispatcher`
- `CudagraphDispatcher.CudagraphDispatcher`
- `CudagraphDispatcher.DefaultDispatchPolicy`
- `CudagraphDispatcher.DispatchKey`
- ... and 26 more

---
*Auto-generated documentation*
