"""
Phase 45: KV Transfer Connector Factory
Registry and factory for KV transfer connectors.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from src.infrastructure.kv_transfer.connector.decode_bench import DecodeBenchConnector

if TYPE_CHECKING:
    from src.infrastructure.kv_transfer.connector.base import KVConnectorBase
    from src.infrastructure.kv_transfer.connector.types import KVTransferConfig

logger = logging.getLogger(__name__)

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
    """Register a KV connector class."""
    _CONNECTOR_REGISTRY[name] = connector_cls
    logger.info("Registered KV connector: %s", name)


def get_kv_connector(
    config: KVTransferConfig,
    kv_cache_config: Optional[Any] = None,
) -> KVConnectorBase:
    """Get a KV connector instance by configuration."""
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
