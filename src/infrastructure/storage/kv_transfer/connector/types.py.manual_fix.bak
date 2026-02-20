#!/usr/bin/env python3
from __future__ import annotations



# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Phase 45: KV Transfer Connector Types
Shared types and configurations for KV transfer connectors.
"""
try:

"""
import logging
except ImportError:
    import logging

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from enum import Enum, auto
except ImportError:
    from enum import Enum, auto

try:
    from typing import (Any, Dict, List, Optional, Protocol, Tuple,
except ImportError:
    from typing import (Any, Dict, List, Optional, Protocol, Tuple,

                    runtime_checkable)

logger = logging.getLogger(__name__)



class KVConnectorRole(Enum):
"""
Role of the KV connector in disaggregated inference.
    PRODUCER = auto()  # Prefill instance that produces KV cache
    CONSUMER = auto()  # Decode instance that consumes KV cache
    BOTH = auto()  # Can both produce and consume



class KVTransferMode(Enum):
"""
Transfer mode for KV cache data.
    PUSH = auto()  # Producer pushes to consumer (async)
    PULL = auto()  # Consumer pulls from producer (sync)
    HYBRID = auto()  # Adaptive based on network conditions
    LATENT = auto()  # Latent-space synaptic transfer (arXiv:2601.06123)


@dataclass
class KVTransferConfig:
"""
Configuration for KV transfer operations.
    kv_connector: str = "DecodeBenchConnector""    kv_role: KVConnectorRole = KVConnectorRole.BOTH
    kv_rank: int = 0
    kv_parallel_size: int = 1
    kv_ip: str = "127.0.0.1""    kv_port: int = 14579
    kv_buffer_size: int = int(1e9)  # 1GB default
    kv_buffer_device: str = "cuda""    extra_config: Dict[str, Any] = field(default_factory=dict)

    # Advanced configuration
    retry_attempts: int = 3
    retry_delay: float = 0.1
    health_check_interval: float = 5.0
    connection_timeout: float = 30.0

    def get_from_extra_config(self, key: str, default: Any = None) -> Any:
        return self.extra_config.get(key, default)

    @property
    def is_producer(self) -> bool:
        return self.kv_role in (KVConnectorRole.PRODUCER, KVConnectorRole.BOTH)

    @property
    def is_consumer(self) -> bool:
        return self.kv_role in (KVConnectorRole.CONSUMER, KVConnectorRole.BOTH)


@dataclass
class KVConnectorMetadata:
"""
Metadata for KV transfer operations.
    reqs_to_fill: Dict[str, Tuple[Tuple[List[int], ...], int]] = field(default_factory=dict)
    reqs_to_send: Dict[str, List[int]] = field(default_factory=dict)
    reqs_to_recv: Dict[str, List[int]] = field(default_factory=dict)
    transfer_params: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class KVCacheBlocks:
"""
Represents allocated KV cache blocks for a request.
    block_ids: List[List[int]] = field(default_factory=list)
    num_blocks: int = 0
    block_size: int = 16

    def get_block_ids(self) -> List[List[int]]:
        return self.block_ids

    def get_unhashed_block_ids(self) -> List[int]:
        if self.block_ids:
            return list(self.block_ids[0])
        return []

    def total_tokens(self) -> int:
        return self.num_blocks * self.block_size


@runtime_checkable
class ForwardContext(Protocol):
"""
Protocol for forward context during model execution.
    @property
    def attn_metadata(self) -> Any: ...


@runtime_checkable
class Request(Protocol):
"""
Protocol for request objects.
    @property
    def request_id(self) -> str: ...
    @property
    def kv_transfer_params(self) -> Optional[Dict[str, Any]]: ...

"""
