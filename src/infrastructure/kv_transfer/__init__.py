# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
KV Transfer module for disaggregated prefill-decode inference.

Provides connectors for transferring KV cache between prefill and decode instances.
Inspired by vLLM's distributed/kv_transfer/ architecture.
"""

from .kv_transfer_connector import (
    KVConnectorRole,
    KVTransferConfig,
    KVConnectorBase,
    KVConnectorMetadata,
    KVCacheBlocks,
    DecodeBenchConnector,
    get_kv_connector,
    register_kv_connector,
    list_kv_connectors,
)

__all__ = [
    "KVConnectorRole",
    "KVTransferConfig",
    "KVConnectorBase",
    "KVConnectorMetadata",
    "KVCacheBlocks",
    "DecodeBenchConnector",
    "get_kv_connector",
    "register_kv_connector",
    "list_kv_connectors",
]
