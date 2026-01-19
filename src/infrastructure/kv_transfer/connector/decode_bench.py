"""
Phase 45: Decode Bench KV Connector
KV Connector for decode instance benchmarking.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING
from src.infrastructure.kv_transfer.connector.base import KVConnectorBase
from src.infrastructure.kv_transfer.connector.types import KVConnectorMetadata

if TYPE_CHECKING:
    from src.infrastructure.kv_transfer.connector.types import (
        KVTransferConfig, ForwardContext, Request, KVCacheBlocks
    )

logger = logging.getLogger(__name__)


class DecodeBenchConnector(KVConnectorBase):
    """KV Connector for decode instance benchmarking."""
    
    def __init__(
        self,
        config: KVTransferConfig,
        kv_cache_config: Optional[Any] = None,
    ):
        super().__init__(config, kv_cache_config)
        
        # Fill parameters from extra config
        self.fill_mean = config.get_from_extra_config("fill_mean", 0.015)
        self.fill_std = config.get_from_extra_config("fill_std", 0.0)
        self.block_size = 16  # Default block size
        
        # Scheduler-side state
        self._filled_requests: set[str] = set()
        self._pending_fills: Dict[str, Tuple[Tuple[List[int], ...], int]] = {}
        
        # Worker-side state
        self.group_to_layers: Optional[Dict[int, List[str]]] = None
        
    def _init_group_mapping(self) -> None:
        """Initialize mapping from KV cache groups to layer names."""
        if self._kv_caches and self.group_to_layers is None:
            # For standard attention, all layers are in group 0
            self.group_to_layers = {0: list(self._kv_caches.keys())}
    
    # Worker-side methods
    
    def start_load_kv(
        self,
        forward_context: ForwardContext,
        **kwargs: Any,
    ) -> None:
        """Start filling KV cache with dummy values."""
        metadata = kwargs.get("metadata")
        if metadata is not None and isinstance(metadata, KVConnectorMetadata):
            self._start_fill_kv(metadata)
    
    def _start_fill_kv(self, metadata: KVConnectorMetadata) -> None:
        """Fill the allocated KV cache blocks with dummy values."""
        if not metadata.reqs_to_fill:
            return
        
        self._init_group_mapping()
        
        if self._kv_caches is None or self.group_to_layers is None:
            logger.warning("KV caches not registered, cannot fill")
            return
        
        for req_id, (block_ids_per_group, num_tokens) in metadata.reqs_to_fill.items():
            for group_idx, block_ids in enumerate(block_ids_per_group):
                self._fill_blocks(group_idx, block_ids, num_tokens)
            
            logger.debug(
                "DecodeBenchConnector: Filled %d blocks (%d tokens) for request %s",
                len(block_ids_per_group[0]) if block_ids_per_group else 0,
                num_tokens,
                req_id,
            )
    
    def _fill_blocks(
        self,
        group_idx: int,
        block_ids: List[int],
        num_tokens: int,
    ) -> None:
        """Fill specific blocks with dummy values."""
        if self.group_to_layers is None:
            return
        
        layer_names = self.group_to_layers.get(group_idx, [])
        
        for layer_name in layer_names:
            kv_cache = self._kv_caches.get(layer_name)
            if kv_cache is None:
                continue
            
            # Fill with dummy values
            logger.debug(
                "Filling layer %s blocks %s with %d tokens",
                layer_name,
                block_ids[:3],  # Log first 3 for brevity
                num_tokens,
            )
    
    def wait_for_layer_load(self, layer_name: str) -> None:
        """No-op for benchmark connector - fills are synchronous."""
        pass
    
    def save_kv_layer(
        self,
        layer_name: str,
        kv_layer: Any,
        attn_metadata: Any,
        **kwargs: Any,
    ) -> None:
        """No-op for benchmark connector - no actual saving."""
        pass
    
    # Scheduler-side methods
    
    def get_num_new_matched_tokens(
        self,
        request: Request,
        num_computed_tokens: int,
    ) -> Tuple[int, bool]:
        """Return number of tokens to fill with dummy KV cache."""
        req_id = request.request_id
        
        # Only fill once per request on first scheduling
        if req_id in self._filled_requests:
            return 0, False
        
        # Get prompt length from request
        params = request.kv_transfer_params or {}
        prompt_len = params.get("prompt_length", 0)
        
        if prompt_len <= 1:
            return 0, False
        
        # Fill all tokens except the last one
        num_to_fill = prompt_len - num_computed_tokens - 1
        return max(0, num_to_fill), False
    
    def update_state_after_alloc(
        self,
        request: Request,
        blocks: KVCacheBlocks,
        num_external_tokens: int,
    ) -> None:
        """Track blocks to fill for the request."""
        if num_external_tokens <= 0:
            return
        
        req_id = request.request_id
        if req_id in self._filled_requests:
            return
        
        block_ids_tuple = tuple(tuple(ids) for ids in blocks.get_block_ids())
        self._pending_fills[req_id] = (block_ids_tuple, num_external_tokens)
        self._filled_requests.add(req_id)
    
    def build_connector_meta(
        self,
        scheduler_output: Any,
    ) -> KVConnectorMetadata:
        """Build metadata with pending fills."""
        metadata = KVConnectorMetadata()
        
        # Move pending fills to metadata and clear
        for req_id, (block_ids, num_tokens) in self._pending_fills.items():
            metadata.reqs_to_fill[req_id] = (
                tuple(list(ids) for ids in block_ids),
                num_tokens,
            )
        
        self._pending_fills.clear()
        return metadata
    
    def request_finished(
        self,
        request: Request,
        block_ids: List[int],
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Clean up state when request finishes."""
        req_id = request.request_id
        self._filled_requests.discard(req_id)
        self._pending_fills.pop(req_id, None)
        return True, None
