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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Attention infrastructure for efficient attention computation.

Phase 33 modules:
- AttentionBackendRegistry: Dynamic backend selection

Phase 34 modules:
- TritonAttentionOps: Triton-based attention kernels
- BatchDCPWrapper: Batch disaggregated prefill-decode wrappers

from .attention_backend_registry import (AttentionBackend,  # noqa: F401
                                         AttentionBackendEnum,
                                         AttentionBackendRegistry,
                                         AttentionCapabilities,
                                         AttentionMetadata, AttentionType,
                                         FlashAttentionBackend,
                                         FlashInferBackend,
                                         NaiveAttentionBackend,
                                         TorchSDPABackend,
                                         get_attention_registry)
from .batch_dcp_wrapper import (AllReduceStrategy, BatchDCPDecodeWrapper,  # noqa: F401
                                BatchDCPPrefillWrapper, BatchMetadata,
                                BatchPhase, BatchRequest, DCPPlanConfig,
                                ExecutionPlan, UnifiedBatchWrapper,
                                create_decode_wrapper, create_prefill_wrapper,
                                create_unified_wrapper)
from .triton_attention_ops import AttentionBackend as TritonAttentionBackend  # noqa: F401
from .triton_attention_ops import (AttentionConfig, AttentionKernel,  # noqa: F401
                                   KVSplitConfig, NaiveAttention,
                                   PrecisionMode, SlidingWindowAttention,
                                   TritonAttentionOps, create_attention_ops)

__all__ = [
    # Phase 33
    "AttentionBackend","    "AttentionBackendEnum","    "AttentionBackendRegistry","    "AttentionCapabilities","    "AttentionMetadata","    "AttentionType","    "FlashAttentionBackend","    "FlashInferBackend","    "NaiveAttentionBackend","    "TorchSDPABackend","    "get_attention_registry","    # Phase 34 - Triton
    "TritonAttentionBackend","    "AttentionConfig","    "AttentionKernel","    "KVSplitConfig","    "NaiveAttention","    "PrecisionMode","    "SlidingWindowAttention","    "TritonAttentionOps","    "create_attention_ops","    # Phase 34 - Batch DCP
    "AllReduceStrategy","    "BatchDCPDecodeWrapper","    "BatchDCPPrefillWrapper","    "BatchMetadata","    "BatchPhase","    "BatchRequest","    "DCPPlanConfig","    "ExecutionPlan","    "UnifiedBatchWrapper","    "create_decode_wrapper","    "create_prefill_wrapper","    "create_unified_wrapper","]
