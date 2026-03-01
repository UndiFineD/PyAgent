# __init__

**File**: `src\infrastructure\attention\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 32 imports  
**Lines**: 89  
**Complexity**: 0 (simple)

## Overview

Attention infrastructure for efficient attention computation.

Phase 33 modules:
- AttentionBackendRegistry: Dynamic backend selection

Phase 34 modules:
- TritonAttentionOps: Triton-based attention kernels
- BatchDCPWrapper: Batch disaggregated prefill-decode wrappers

## Dependencies

**Imports** (32):
- `AttentionBackendRegistry.AttentionBackend`
- `AttentionBackendRegistry.AttentionBackendEnum`
- `AttentionBackendRegistry.AttentionBackendRegistry`
- `AttentionBackendRegistry.AttentionCapabilities`
- `AttentionBackendRegistry.AttentionMetadata`
- `AttentionBackendRegistry.AttentionType`
- `AttentionBackendRegistry.FlashAttentionBackend`
- `AttentionBackendRegistry.FlashInferBackend`
- `AttentionBackendRegistry.NaiveAttentionBackend`
- `AttentionBackendRegistry.TorchSDPABackend`
- `AttentionBackendRegistry.get_attention_registry`
- `BatchDCPWrapper.AllReduceStrategy`
- `BatchDCPWrapper.BatchDCPDecodeWrapper`
- `BatchDCPWrapper.BatchDCPPrefillWrapper`
- `BatchDCPWrapper.BatchMetadata`
- ... and 17 more

---
*Auto-generated documentation*
