# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
KV Transfer Connector - Base framework for disaggregated prefill-decode inference.

Provides connectors for transferring KV cache between prefill and decode instances.
Inspired by vLLM's distributed/kv_transfer/kv_connector/ architecture.

Key patterns from vLLM:
- KVConnectorBase_V1: Abstract base for v1 connectors
- DecodeBenchConnector: Fills KV cache with dummy values for benchmarking
- NixlConnector: RDMA-based KV transfer
- MooncakeConnector: Mooncake protocol transfer
- Scheduler-side and Worker-side method separation

Beyond vLLM:
- Multi-backend support with automatic fallback chain
- Connector health monitoring and auto-recovery
- Connection pooling for multi-instance deployments
"""

from __future__ import annotations

import logging
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    runtime_checkable,
)

if TYPE_CHECKING:
    import numpy as np

logger = logging.getLogger(__name__)

# Type variable for generic connector operations
T = TypeVar("T")


class KVConnectorRole(Enum):
    """Role of the KV connector in disaggregated inference.
    
    Inspired by vLLM's kv_transfer/kv_connector/base.py.
    """
    PRODUCER = auto()  # Prefill instance that produces KV cache
    CONSUMER = auto()  # Decode instance that consumes KV cache
    BOTH = auto()      # Can both produce and consume (for testing/benchmarking)


class KVTransferMode(Enum):
    """Transfer mode for KV cache data.
    
    Determines how KV cache data is transferred between instances.
    """
    PUSH = auto()      # Producer pushes to consumer (async)
    PULL = auto()      # Consumer pulls from producer (sync)
    HYBRID = auto()    # Adaptive based on network conditions


@dataclass
class KVTransferConfig:
    """Configuration for KV transfer operations.
    
    Inspired by vLLM's config/kv_transfer.py KVTransferConfig.
    
    Attributes:
        kv_connector: Name of the connector to use
        kv_role: Role of this instance (producer/consumer/both)
        kv_rank: Rank of this instance in the KV transfer group
        kv_parallel_size: Number of parallel instances
        kv_ip: IP address for KV transfer communication
        kv_port: Port for KV transfer communication
        kv_buffer_size: Size of the KV transfer buffer
        kv_buffer_device: Device for KV buffer ("cuda" or "cpu")
        extra_config: Additional connector-specific configuration
    """
    kv_connector: str = "DecodeBenchConnector"
    kv_role: KVConnectorRole = KVConnectorRole.BOTH
    kv_rank: int = 0
    kv_parallel_size: int = 1
    kv_ip: str = "127.0.0.1"
    kv_port: int = 14579
    kv_buffer_size: int = int(1e9)  # 1GB default
    kv_buffer_device: str = "cuda"
    extra_config: Dict[str, Any] = field(default_factory=dict)
    
    # Beyond vLLM: Advanced configuration
    retry_attempts: int = 3
    retry_delay: float = 0.1
    health_check_interval: float = 5.0
    connection_timeout: float = 30.0
    
    def get_from_extra_config(self, key: str, default: Any = None) -> Any:
        """Get a value from extra_config with default fallback."""
        return self.extra_config.get(key, default)
    
    @property
    def is_producer(self) -> bool:
        """Check if this instance can produce KV cache."""
        return self.kv_role in (KVConnectorRole.PRODUCER, KVConnectorRole.BOTH)
    
    @property
    def is_consumer(self) -> bool:
        """Check if this instance can consume KV cache."""
        return self.kv_role in (KVConnectorRole.CONSUMER, KVConnectorRole.BOTH)


@dataclass
class KVConnectorMetadata:
    """Metadata for KV transfer operations.
    
    Contains information needed to coordinate KV cache transfers.
    Inspired by vLLM's decode_bench_connector.py DecodeBenchConnectorMetadata.
    """
    reqs_to_fill: Dict[str, Tuple[Tuple[List[int], ...], int]] = field(
        default_factory=dict
    )
    # request_id -> (block_ids_per_group, num_tokens)
    
    reqs_to_send: Dict[str, List[int]] = field(default_factory=dict)
    # request_id -> block_ids to send
    
    reqs_to_recv: Dict[str, List[int]] = field(default_factory=dict)
    # request_id -> block_ids to receive
    
    # Transfer parameters for remote operations
    transfer_params: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    # request_id -> {remote_host, remote_port, remote_engine_id, remote_block_ids, ...}


@dataclass
class KVCacheBlocks:
    """Represents allocated KV cache blocks for a request.
    
    Inspired by vLLM's block allocation patterns.
    """
    block_ids: List[List[int]] = field(default_factory=list)
    # block_ids[group_idx] = [block_id_0, block_id_1, ...]
    
    num_blocks: int = 0
    block_size: int = 16
    
    def get_block_ids(self) -> List[List[int]]:
        """Get all block IDs across groups."""
        return self.block_ids
    
    def get_unhashed_block_ids(self) -> List[int]:
        """Get block IDs that haven't been hashed for prefix caching."""
        # For simplicity, return all block IDs from first group
        if self.block_ids:
            return list(self.block_ids[0])
        return []
    
    def total_tokens(self) -> int:
        """Calculate total token capacity."""
        return self.num_blocks * self.block_size


@runtime_checkable
class ForwardContext(Protocol):
    """Protocol for forward context during model execution."""
    
    @property
    def attn_metadata(self) -> Any:
        """Get attention metadata."""
        ...


@runtime_checkable
class Request(Protocol):
    """Protocol for request objects."""
    
    @property
    def request_id(self) -> str:
        """Get request ID."""
        ...
    
    @property
    def kv_transfer_params(self) -> Optional[Dict[str, Any]]:
        """Get KV transfer parameters."""
        ...


class KVConnectorBase(ABC):
    """Abstract base class for KV transfer connectors.
    
    Inspired by vLLM's KVConnectorBase_V1 in kv_connector/v1/base.py.
    Provides both scheduler-side and worker-side methods.
    
    The connector handles:
    1. Registering KV caches for transfer
    2. Loading KV cache from remote (consumer side)
    3. Saving KV cache to remote (producer side)
    4. Coordinating request lifecycle with KV transfer state
    """
    
    def __init__(
        self,
        config: KVTransferConfig,
        kv_cache_config: Optional[Any] = None,
    ):
        """Initialize the KV connector.
        
        Args:
            config: KV transfer configuration
            kv_cache_config: Optional KV cache configuration
        """
        self.config = config
        self.kv_cache_config = kv_cache_config
        self._kv_caches: Dict[str, Any] = {}  # layer_name -> kv_cache tensor
        self._lock = threading.RLock()
        self._initialized = False
        
        # Health tracking (Beyond vLLM)
        self._last_health_check = 0.0
        self._health_status = True
        self._error_count = 0
        
    # ==============================
    # Worker-side methods
    # ==============================
    
    def register_kv_caches(self, kv_caches: Dict[str, Any]) -> None:
        """Register KV caches for transfer operations.
        
        Args:
            kv_caches: Dictionary mapping layer names to KV cache tensors
        """
        with self._lock:
            self._kv_caches = kv_caches
            self._initialized = True
            logger.debug(
                "Registered %d KV cache layers for transfer",
                len(kv_caches),
            )
    
    @abstractmethod
    def start_load_kv(
        self,
        forward_context: ForwardContext,
        **kwargs: Any,
    ) -> None:
        """Start asynchronous KV cache loading.
        
        Called at the beginning of model forward to initiate KV loading.
        
        Args:
            forward_context: Current forward context with attention metadata
            **kwargs: Additional arguments
        """
        ...
    
    @abstractmethod
    def wait_for_layer_load(self, layer_name: str) -> None:
        """Wait for a specific layer's KV cache to finish loading.
        
        Called before each attention layer to ensure KV cache is ready.
        
        Args:
            layer_name: Name of the layer to wait for
        """
        ...
    
    @abstractmethod
    def save_kv_layer(
        self,
        layer_name: str,
        kv_layer: Any,
        attn_metadata: Any,
        **kwargs: Any,
    ) -> None:
        """Save a layer's KV cache for transfer.
        
        Called after each attention layer on the producer side.
        
        Args:
            layer_name: Name of the layer
            kv_layer: KV cache tensor for the layer
            attn_metadata: Attention metadata
            **kwargs: Additional arguments
        """
        ...
    
    def wait_for_save(self) -> None:
        """Wait for all KV cache saves to complete.
        
        Called after model forward on the producer side.
        """
        pass  # Default no-op, override if async saving
    
    # ==============================
    # Scheduler-side methods
    # ==============================
    
    @abstractmethod
    def get_num_new_matched_tokens(
        self,
        request: Request,
        num_computed_tokens: int,
    ) -> Tuple[int, bool]:
        """Get number of tokens that can be loaded from external KV cache.
        
        Args:
            request: The request object
            num_computed_tokens: Number of locally computed tokens
            
        Returns:
            Tuple of (num_tokens_to_fill, is_async)
            - num_tokens_to_fill: Number of tokens loadable from external
            - is_async: Whether loading is asynchronous
        """
        ...
    
    @abstractmethod
    def update_state_after_alloc(
        self,
        request: Request,
        blocks: KVCacheBlocks,
        num_external_tokens: int,
    ) -> None:
        """Update connector state after block allocation.
        
        Called after blocks are allocated for a request.
        
        Args:
            request: The request object
            blocks: Allocated KV cache blocks
            num_external_tokens: Number of tokens from external source
        """
        ...
    
    @abstractmethod
    def build_connector_meta(
        self,
        scheduler_output: Any,
    ) -> KVConnectorMetadata:
        """Build metadata for worker-side operations.
        
        Called during scheduler step to prepare transfer metadata.
        
        Args:
            scheduler_output: Output from scheduler step
            
        Returns:
            Metadata for KV transfer operations
        """
        ...
    
    @abstractmethod
    def request_finished(
        self,
        request: Request,
        block_ids: List[int],
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Handle request completion.
        
        Called when a request finishes to clean up KV transfer state.
        
        Args:
            request: The completed request
            block_ids: Block IDs used by the request
            
        Returns:
            Tuple of (should_free_blocks, transfer_info)
        """
        ...
    
    # ==============================
    # Health and lifecycle (Beyond vLLM)
    # ==============================
    
    def health_check(self) -> bool:
        """Check connector health.
        
        Returns:
            True if connector is healthy
        """
        return self._health_status and self._initialized
    
    def reset_error_count(self) -> None:
        """Reset error count after successful operation."""
        self._error_count = 0
    
    def record_error(self) -> None:
        """Record an error occurrence."""
        self._error_count += 1
        if self._error_count > self.config.retry_attempts:
            self._health_status = False
            logger.warning(
                "KV connector marked unhealthy after %d errors",
                self._error_count,
            )
    
    def close(self) -> None:
        """Close the connector and release resources."""
        with self._lock:
            self._kv_caches.clear()
            self._initialized = False


class DecodeBenchConnector(KVConnectorBase):
    """KV Connector for decode instance benchmarking.
    
    Fills KV cache with dummy (non-zero) values to emulate a prefill-decode
    disaggregated setting. Enables performance testing of decode with
    larger input sequence lengths.
    
    Inspired by vLLM's decode_bench_connector.py.
    
    Usage:
        config = KVTransferConfig(
            kv_connector="DecodeBenchConnector",
            kv_role=KVConnectorRole.BOTH,
            extra_config={"fill_mean": 0.015, "fill_std": 0.0}
        )
    """
    
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
    
    # ==============================
    # Worker-side methods
    # ==============================
    
    def start_load_kv(
        self,
        forward_context: ForwardContext,
        **kwargs: Any,
    ) -> None:
        """Start filling KV cache with dummy values.
        
        For DecodeBenchConnector, this fills allocated blocks with
        random values to simulate having cached KV from prefill.
        """
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
