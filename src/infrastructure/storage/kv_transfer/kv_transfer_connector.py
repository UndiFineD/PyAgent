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

"""
KV Transfer Connector - Base framework for disaggregated prefill-decode inference.

Refactored to modular package structure for Phase 317.
Decomposed into types, base, implementations, and factory modules.
"""

from src.infrastructure.storage.kv_transfer.connector.base import \
    KVConnectorBase
from src.infrastructure.storage.kv_transfer.connector.decode_bench import \
    DecodeBenchConnector
from src.infrastructure.storage.kv_transfer.connector.factory import (
    get_kv_connector, list_kv_connectors, register_kv_connector)
from src.infrastructure.storage.kv_transfer.connector.types import (
    ForwardContext, KVCacheBlocks, KVConnectorMetadata, KVConnectorRole,
    KVTransferConfig, KVTransferMode, Request)

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
