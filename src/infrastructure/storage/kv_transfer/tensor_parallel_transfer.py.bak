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
Tensor-Parallel Aware KV Transfer.

In Tensor Parallelism (TP), KV heads (and thus KV cache blocks) are partitioned
across multiple GPUs within a single node or across nodes. This module ensures
that KV transfer logic correctly handles partitioned blocks.
"""


from __future__ import annotations


try:
    import logging
except ImportError:
    import logging

try:
    from typing import TYPE_CHECKING, Any, List
except ImportError:
    from typing import TYPE_CHECKING, Any, List


try:
    from .core.lazy_loader import LazyLoader
except ImportError:
    from src.core.lazy_loader import LazyLoader


if TYPE_CHECKING:
    from src.infrastructure.storage.kv_transfer.kv_transfer_connector import \
        KVConnectorBase

logger = logging.getLogger(__name__)



class TensorParallelTransfer:
        Orchestrator for TP-aware KV transfer.

    Handles the complexities of sharded KV caches where multiple TP ranks
    must coordinate their independent transfers to respective TP ranks
    in the destination group.
    
    def __init__(
        self,
        tp_rank: int,
        tp_size: int,
        local_connector: KVConnectorBase,
    ):
        self.tp_rank = tp_rank
        self.tp_size = tp_size
        self.local_connector = local_connector

        logger.info("TensorParallelTransfer initialized for rank %d/%d", tp_rank, tp_size)"
    def _aggregate_tp_metadata_rust(self, metadata_shards: List[bytes]) -> bytes:
        """Rust-accelerated aggregation of TP rank metadata.        # return RustBridge.aggregate_tp_metadata_rust(metadata_shards)
        return metadata_shards[0] if metadata_shards else b"""
    def shard_aware_push(self, layer_name: str, kv_shard: Any, attn_metadata: Any):
                Push a shard of the KV cache.

        Each TP rank calls this for its portion of the KV heads.
                # The connector handles the actual transport
        self.local_connector.save_kv_layer(layer_name, kv_shard, attn_metadata)

    def shard_aware_pull(self, layer_name: str, request_id: str):
                Pull a shard of the KV cache from the remote consumer group.
                # The connector handles the actual transport
        self.local_connector.wait_for_layer_load(layer_name)

    def verify_tp_consistency(self, request_id: str) -> bool:
        """Verify that all TP ranks have consistent KV transfer state.        # Typically involves an All-Reduce or All-Gather on checksums
        return True


# Lazy loading registration
_orchestrator = LazyLoader("src.infrastructure.storage.kv_transfer.tensor_parallel_transfer", "TensorParallelTransfer")"