"""
KV Transfer Connector - Base framework for disaggregated prefill-decode inference.

Refactored to modular package structure for Phase 317.
Decomposed into types, base, implementations, and factory modules.
"""

from src.infrastructure.storage.kv_transfer.connector.types import (
    KVConnectorRole, KVTransferMode, KVTransferConfig,
    KVConnectorMetadata, KVCacheBlocks, ForwardContext, Request
)
from src.infrastructure.storage.kv_transfer.connector.base import KVConnectorBase
from src.infrastructure.storage.kv_transfer.connector.decode_bench import DecodeBenchConnector
from src.infrastructure.storage.kv_transfer.connector.factory import (
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
