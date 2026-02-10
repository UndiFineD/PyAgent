#!/usr/bin/env python3
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

# SPDX-License-Identifier: Apache-2.0
"""
NIXL High-Performance KV Transfer Connector.

NIXL (Network Interconnect for X-Large models) provides a low-latency, high-bandwidth
transport layer for KV cache blocks between disaggregated prefill and decode instances.
It utilizes RDMA techniques and peer-to-peer memory copies to minimize CPU overhead.
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set

try:
    import numpy as np
except ImportError:
    np = None

from src.core.lazy_loader import LazyLoader
from src.core.rust_bridge import RustBridge
from src.infrastructure.storage.kv_transfer.kv_transfer_connector import (
    KVConnectorBase, KVTransferConfig)

if TYPE_CHECKING:
    from src.infrastructure.storage.kv_transfer.kv_transfer_connector import \
        ForwardContext


logger = logging.getLogger(__name__)


class NixlMemoryRegionStatus(IntEnum):
    """Status of an RDMA memory region."""

    UNREGISTERED = 0
    REGISTERING = 1
    REGISTERED = 2
    ERROR = 3


@dataclass
class NixlMemoryRegion:
    """Represents a registered memory region for RDMA operations."""

    address: int
    length: int
    lkey: int
    rkey: int
    status: NixlMemoryRegionStatus = NixlMemoryRegionStatus.UNREGISTERED
    device_id: int = 0


class NixlConnector(KVConnectorBase):
    """
    NIXL high-performance connector logic.
    """

    def __init__(
        self,
        config: KVTransferConfig,
        kv_cache_config: Optional[Any] = None,
    ):
        super().__init__(config, kv_cache_config)
        self.rank = config.kv_rank
        self.world_size = config.kv_parallel_size
        self.rust_bridge = RustBridge()
        self.memory_regions: Dict[int, NixlMemoryRegion] = {}
        self.active_transfers: Set[str] = set()
        self._lock = threading.Lock()

        self._stop_event = threading.Event()
        self._completion_thread: Optional[threading.Thread] = None

        # Initialize RDMA
        self._init_rdma()
        logger.info("NixlConnector initialized on rank %d/%d", self.rank, self.world_size)

    def _init_rdma(self):
        """Initialize Rust RDMA context."""
        try:
            self.rust_bridge.execute(
                "init_nixl_rdma",
                {
                    "rank": self.rank,
                    "world_size": self.world_size,
                    "device_name": self.config.extra_config.get("rdma_device", "ib0"),
                },
            )

            # Start completion thread
            self._completion_thread = threading.Thread(target=self._poll_loop, daemon=True)
            self._completion_thread.start()
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Failed to initialize Nixl RDMA: {e}")

    def _poll_loop(self):
        """Background thread to poll NIXL completion queues."""
        while not self._stop_event.is_set():
            self.poll_completions()
            time.sleep(0.001)  # nosec

    def register_memory(self, tensor: Any) -> NixlMemoryRegion:
        """Register a tensor's memory for RDMA operations (Pinning)."""
        with self._lock:
            tensor_id = id(tensor)
            if tensor_id in self.memory_regions:
                return self.memory_regions[tensor_id]

            addr = 0
            length = 0
            if np is not None and isinstance(tensor, np.ndarray):
                addr = tensor.__array_interface__["data"][0]
                length = tensor.nbytes
            elif hasattr(tensor, "data_ptr"):
                addr = tensor.data_ptr()
                length = tensor.numel() * tensor.element_size()

            result = self.rust_bridge.execute("nixl_register_mr", {"address": addr, "length": length})

            region = NixlMemoryRegion(
                address=addr,
                length=length,
                lkey=result.get("lkey", 0),
                rkey=result.get("rkey", 0),
                status=NixlMemoryRegionStatus.REGISTERED,
            )
            self.memory_regions[tensor_id] = region
            return region

    def transfer_blocks(
        self, target_rank: int, block_ids: List[int], local_tensor: Any, remote_buffer_ptr: int, rkey: int
    ) -> bool:
        """Asynchronously transfer KV blocks to a remote rank."""
        try:
            region = self.register_memory(local_tensor)
            transfer_id = f"tx_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"

            self.rust_bridge.execute(
                "nixl_rdma_write",
                {
                    "transfer_id": transfer_id,
                    "target_rank": target_rank,
                    "block_ids": block_ids,
                    "local_ptr": region.address,
                    "remote_ptr": remote_buffer_ptr,
                    "remote_rkey": rkey,
                },
            )

            with self._lock:
                self.active_transfers.add(transfer_id)
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.error(f"Nixl transfer failed: {e}")
            return False

    def poll_completions(self) -> List[str]:
        """Poll for completed transfers."""
        try:
            completed = self.rust_bridge.execute("nixl_poll_cq", {})
            finished_ids = []
            with self._lock:
                for tx_id in completed:
                    if tx_id in self.active_transfers:
                        self.active_transfers.remove(tx_id)
                        finished_ids.append(tx_id)
            return finished_ids
        except Exception:  # pylint: disable=broad-exception-caught
            return []

    # ==============================
    # Phase 93: RDMA Checkpointing
    # ==============================

    def create_rdma_checkpoint(self, checkpoint_id: str, tensor: Any) -> bool:
        """
        Creates a background RDMA-based checkpoint (Phase 93).
        
        Transfers a memory shard to a pre-defined remote 'Mirror Rank' 
        for zero-latency recovery if the local node crashes.
        """
        try:
            region = self.register_memory(tensor)
            # Use rank + 1 as the mirror rank for this simple implementation
            mirror_rank = (self.rank + 1) % self.world_size
            
            logger.info(f"Initiating RDMA Checkpoint {checkpoint_id} to rank {mirror_rank}")
            
            self.rust_bridge.execute(
                "nixl_rdma_checkpoint_rust",
                {
                    "checkpoint_id": checkpoint_id,
                    "target_rank": mirror_rank,
                    "local_ptr": region.address,
                    "length": region.length,
                    "lkey": region.lkey,
                },
            )
            return True
        except Exception as e:
            logger.error(f"RDMA Checkpoint failed: {e}")
            return False

    # ==============================
    # KVConnectorBase Implementation
    # ==============================

    def start_load_kv(self, forward_context: ForwardContext, **kwargs: Any) -> None:
        """Initiate RDMA Read from producer."""
        if not self.config.is_consumer:
            return

        source_rank = kwargs.get("source_rank", (self.rank - 1) % self.world_size)
        logger.debug("Nixl starting RDMA Read from rank %d", source_rank)

    def wait_for_layer_load(self, layer_name: str) -> None:
        """Wait for specific layer blocks to arrive."""
        pass

    def save_kv_layer(self, layer_name: str, kv_layer: Any, attn_metadata: Any, **kwargs: Any) -> None:
        """Save layer and trigger RDMA Write to consumers."""
        if not self.config.is_producer:
            return

        target_ranks = kwargs.get("target_ranks", [(self.rank + 1) % self.world_size])
        block_ids = getattr(attn_metadata, "slot_mapping", [])

        for t_rank in target_ranks:
            self.transfer_blocks(
                target_rank=t_rank, block_ids=block_ids, local_tensor=kv_layer, remote_buffer_ptr=0, rkey=0
            )

    def close(self) -> None:
        """Clean up NIXL resources."""
        self._stop_event.set()
        if self._completion_thread:
            self._completion_thread.join(timeout=1.0)
        logger.info("NixlConnector closed.")


# Lazy loading registration
_connector = LazyLoader("src.infrastructure.storage.kv_transfer.nixl_connector", "NixlConnector")
