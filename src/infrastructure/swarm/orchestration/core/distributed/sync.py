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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
High-performance synchronization primitives using RDMA/Nixl.
"""

from __future__ import annotations

import logging
import threading
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.core.rust_bridge import RustBridge

logger = logging.getLogger(__name__)


class DistributedSyncProvider(ABC):
    """Base class for distributed synchronization providers."""

    @abstractmethod
    def barrier(self, name: str, timeout: float = 30.0) -> bool:
        """Global barrier across all participants."""
        ...

    @abstractmethod
    def broadcast_state(self, key: str, value: Any) -> None:
        """Broadcast state update to all participants."""
        ...

    @abstractmethod
    def get_remote_state(self, key: str, rank: int) -> Optional[Any]:
        """Fetch state from a specific remote rank."""
        ...


class NixlSyncProvider(DistributedSyncProvider):
    """Synchronization provider using NIXL RDMA primitives.

    Utilizes zero-copy memory mapping for low-latency synchronization.
    """

    def __init__(self, rank: int, world_size: int):
        self.rank = rank
        self.world_size = world_size
        self.rust_bridge = RustBridge()
        self._lock = threading.Lock()

        # Initialize NIXL RDMA stubs in Rust
        try:
            self.rust_bridge.execute(
                "nixl_zero_copy_map_rust",
                {
                    "rank": rank,
                    "world_size": world_size,
                    "map_size": 1024 * 1024,  # 1MB for control state
                },
            )
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logger.warning("Failed to initialize Nixl RDMA sync: %s. Falling back to TCP.", e)

    def barrier(self, name: str, timeout: float = 30.0) -> bool:
        """RDMA-accelerated barrier."""
        try:
            # nixl_rdma_send_rust can be used for fast signal pulses
            result = self.rust_bridge.execute(
                "nixl_rdma_send_rust",
                {
                    "type": "barrier",
                    "name": name,
                    "timeout": timeout,
                },
            )
            return result.get("success", False)
        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            return False

    def broadcast_state(self, key: str, value: Any) -> None:
        """Zero-copy broadcast via shared RDMA regions."""
        # Stub implementation
        pass

    def get_remote_state(self, key: str, rank: int) -> Optional[Any]:
        """Direct remote memory access (RDMA READ)."""
        # Stub implementation
        pass


class TCPSyncProvider(DistributedSyncProvider):
    """Fallback TCP-based synchronization."""

    def __init__(self, rank: int, world_size: int):
        self.rank = rank
        self.world_size = world_size
        self._state_store: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def barrier(self, name: str, timeout: float = 30.0) -> bool:
        # Standard socket barrier (placeholder)
        return True

    def broadcast_state(self, key: str, value: Any) -> None:
        with self._lock:
            self._state_store[key] = value
            # In a real implementation, send to all via sockets

    def get_remote_state(self, key: str, rank: int) -> Optional[Any]:
        return None
