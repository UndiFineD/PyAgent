"""
KV Transfer Connector - Base framework for disaggregated prefill-decode inference.

Refactored to modular package structure for Phase 317.
Decomposed into types, base, implementations, and factory modules.
"""

from src.infrastructure.kv_transfer.connector.types import (
    KVConnectorRole, KVTransferMode, KVTransferConfig,
    KVConnectorMetadata, KVCacheBlocks, ForwardContext, Request
)
from src.infrastructure.kv_transfer.connector.base import KVConnectorBase
from src.infrastructure.kv_transfer.connector.decode_bench import DecodeBenchConnector
from src.infrastructure.kv_transfer.connector.factory import (
    register_kv_connector, get_kv_connector, list_kv_connectors
)

__all__ = [
    "KVConnectorRole",
    "KVTransferMode",
    "KVTransferConfig",
    "KVConnectorMetadata",
    "KVCacheBlocks",
    "ForwardContext",
    "Request",
    "KVConnectorBase",
    "DecodeBenchConnector",
    "register_kv_connector",
    "get_kv_connector",
    "list_kv_connectors",
]
    ) -> None:
        """Fill specific blocks with dummy values.
        
        Args:
            group_idx: Index of the KV cache group
            block_ids: Block IDs to fill
            num_tokens: Number of tokens to fill
        """
        if self.group_to_layers is None:
            return
        
        layer_names = self.group_to_layers.get(group_idx, [])
        
        for layer_name in layer_names:
            kv_cache = self._kv_caches.get(layer_name)
            if kv_cache is None:
                continue
            
            # Fill with dummy values
            # In real implementation, this would fill the actual GPU tensor
            # For now, we just mark the blocks as filled
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
    
    # ==============================
    # Scheduler-side methods
    # ==============================
    
    def get_num_new_matched_tokens(
        self,
        request: Request,
        num_computed_tokens: int,
    ) -> Tuple[int, bool]:
        """Return number of tokens to fill with dummy KV cache.
        
        For new requests, fills all tokens except the last one
        (which will be decoded).
        
        Returns:
            (num_tokens_to_fill, is_async=False)
        """
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


# ==============================
# Connector Registry (Beyond vLLM)
# ==============================

_CONNECTOR_REGISTRY: Dict[str, type[KVConnectorBase]] = {
    "DecodeBenchConnector": DecodeBenchConnector,
}


def register_kv_connector(
    name: str,
    connector_cls: type[KVConnectorBase],
) -> None:
    """Register a KV connector class.
    
    Args:
        name: Name for the connector
        connector_cls: Connector class to register
    """
    _CONNECTOR_REGISTRY[name] = connector_cls
    logger.info("Registered KV connector: %s", name)


def get_kv_connector(
    config: KVTransferConfig,
    kv_cache_config: Optional[Any] = None,
) -> KVConnectorBase:
    """Get a KV connector instance by configuration.
    
    Args:
        config: KV transfer configuration
        kv_cache_config: Optional KV cache configuration
        
    Returns:
        Instantiated connector
        
    Raises:
        ValueError: If connector name is not registered
    """
    connector_name = config.kv_connector
    
    if connector_name not in _CONNECTOR_REGISTRY:
        available = list(_CONNECTOR_REGISTRY.keys())
        raise ValueError(
            f"Unknown KV connector: {connector_name}. "
            f"Available: {available}"
        )
    
    connector_cls = _CONNECTOR_REGISTRY[connector_name]
    return connector_cls(config, kv_cache_config)


def list_kv_connectors() -> List[str]:
    """List all registered KV connectors."""
    return list(_CONNECTOR_REGISTRY.keys())
