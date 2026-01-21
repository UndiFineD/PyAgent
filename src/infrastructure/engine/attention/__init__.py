# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Attention infrastructure for efficient attention computation.

Phase 33 modules:
- AttentionBackendRegistry: Dynamic backend selection

Phase 34 modules:
- TritonAttentionOps: Triton-based attention kernels
- BatchDCPWrapper: Batch disaggregated prefill-decode wrappers
"""

from .attention_backend_registry import (
    AttentionBackend,
    AttentionBackendEnum,
    AttentionBackendRegistry,
    AttentionCapabilities,
    AttentionMetadata,
    AttentionType,
    FlashAttentionBackend,
    FlashInferBackend,
    NaiveAttentionBackend,
    TorchSDPABackend,
    get_attention_registry,
)
from .triton_attention_ops import (
    AttentionBackend as TritonAttentionBackend,
    AttentionConfig,
    AttentionKernel,
    KVSplitConfig,
    NaiveAttention,
    PrecisionMode,
    SlidingWindowAttention,
    TritonAttentionOps,
    create_attention_ops,
)
from .batch_dcp_wrapper import (
    AllReduceStrategy,
    BatchDCPDecodeWrapper,
    BatchDCPPrefillWrapper,
    BatchMetadata,
    BatchPhase,
    BatchRequest,
    DCPPlanConfig,
    ExecutionPlan,
    UnifiedBatchWrapper,
    create_decode_wrapper,
    create_prefill_wrapper,
    create_unified_wrapper,
)

__all__ = [
    # Phase 33
    "AttentionBackend",
    "AttentionBackendEnum",
    "AttentionBackendRegistry",
    "AttentionCapabilities",
    "AttentionMetadata",
    "AttentionType",
    "FlashAttentionBackend",
    "FlashInferBackend",
    "NaiveAttentionBackend",
    "TorchSDPABackend",
    "get_attention_registry",
    # Phase 34 - Triton
    "TritonAttentionBackend",
    "AttentionConfig",
    "AttentionKernel",
    "KVSplitConfig",
    "NaiveAttention",
    "PrecisionMode",
    "SlidingWindowAttention",
    "TritonAttentionOps",
    "create_attention_ops",
    # Phase 34 - Batch DCP
    "AllReduceStrategy",
    "BatchDCPDecodeWrapper",
    "BatchDCPPrefillWrapper",
    "BatchMetadata",
    "BatchPhase",
    "BatchRequest",
    "DCPPlanConfig",
    "ExecutionPlan",
    "UnifiedBatchWrapper",
    "create_decode_wrapper",
    "create_prefill_wrapper",
    "create_unified_wrapper",
]
