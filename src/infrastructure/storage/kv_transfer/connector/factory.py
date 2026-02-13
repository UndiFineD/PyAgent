#!/usr/bin/env python3
# Refactored by copilot-placeholder
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

"""
Phase 45: KV Transfer Connector Factory
Registry and factory for KV transfer connectors.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from src.infrastructure.storage.kv_transfer.connector.decode_bench import \
    DecodeBenchConnector

if TYPE_CHECKING:
    from src.infrastructure.storage.kv_transfer.connector.base import \
        KVConnectorBase
    from src.infrastructure.storage.kv_transfer.connector.types import \
        KVTransferConfig

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
        raise ValueError(f"Unknown KV connector: {connector_name}. Available: {available}")

    connector_cls = _CONNECTOR_REGISTRY[connector_name]
    return connector_cls(config, kv_cache_config)


def list_kv_connectors() -> List[str]:
    """List all registered KV connectors."""
    return list(_CONNECTOR_REGISTRY.keys())
