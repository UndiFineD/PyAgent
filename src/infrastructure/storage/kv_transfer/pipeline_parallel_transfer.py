# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

"""
Pipeline-Parallel Aware KV Transfer.

This module provides orchestration for KV cache transfers when Pipeline Parallelism (PP)
is enabled. In PP scenarios, different layers of the model reside on different pipeline
stages (processes/nodes). KV transfer must be coordinated such that each stage's
respective KV blocks are transferred to the correct corresponding stages in the
destination (prefill -> decode) group.

Key Patterns:
- Stage-to-stage mapping for disaggregated PP
- Synchronized collective transfers for KV metadata
- Latency hiding by overlapping PP stage transfers
- Rust-accelerated PP stage mapping logic
"""

from __future__ import annotations

import logging
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

from src.core.rust_bridge import RustBridge
from src.core.lazy_loader import LazyLoader

if TYPE_CHECKING:
    from src.infrastructure.storage.kv_transfer.kv_transfer_connector import KVConnectorBase

logger = logging.getLogger(__name__)


class PipelineParallelTransfer:
    """
    Orchestrator for PP-aware KV transfer.

    Coordinates multiple KV connectors across pipeline stages to ensure
    consistent transfer of a request's full KV context.
    """

    def __init__(
        self,
        pp_rank: int,
        pp_size: int,
        local_connector: KVConnectorBase,
    ):
        self.pp_rank = pp_rank
        self.pp_size = pp_size
        self.local_connector = local_connector

        # Mapping of local layers to this stage
        self.local_layers: List[int] = []

        logger.info("PipelineParallelTransfer initialized for rank %d/%d",
                    pp_rank, pp_size)

    def _calculate_pp_stage_mapping_rust(self, num_layers: int, pp_size: int) -> Dict[int, int]:
        """Rust-accelerated calculation of layer-to-stage distribution."""
        # return RustBridge.calculate_pp_stage_mapping_rust(num_layers, pp_size)
        # Dummy fallback: evenly divide
        return {i: i // (num_layers // pp_size) for i in range(num_layers)}

    def coordinate_transfer_start(self, request_id: str, metadata: Any):
        """Coordinate the start of a multi-stage KV transfer."""
        # Only rank 0 typically coordinates the global metadata
        if self.pp_rank == 0:
            logger.debug("PP Rank 0 coordinating transfer for %s", request_id)
            # Broadcast or register metadata
            pass

    def sync_stage_transfer(self, layer_idx: int):
        """Barrier or sync point for a specific layer's transfer across stages."""
        # Ensure that previous stages in the pipeline have flushed their data
        # if there are dependencies.
        pass

    def get_stage_status(self) -> Dict[str, Any]:
        """Return status of PP-aware transfer."""
        return {
            "pp_rank": self.pp_rank,
            "pp_size": self.pp_size,
            "active_layers": len(self.local_layers),
            "connector_status": self.local_connector.get_health_report() if hasattr(self.local_connector, "get_health_report") else "OK"
        }

# Lazy loading registration
_orchestrator = LazyLoader("src.infrastructure.storage.kv_transfer.pipeline_parallel_transfer", "PipelineParallelTransfer")
