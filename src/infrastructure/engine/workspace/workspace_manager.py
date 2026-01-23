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
High-performance memory workspace manager for Phase 52.
Handles DBO (Distributed Byte Object) allocation and 120fps sync channels.
"""

import logging
import threading
from typing import Dict, Optional, Any, List
import ctypes
import time
from .predictive_workspace import PredictiveWorkspace

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger(__name__)

class WorkspaceManager:
    """
    Manages Distributed Byte Objects (DBO) and synchronized memory workspaces.
    Part of Phase 52 Evolutionary Neuro-Optimization.
    """

    _instance: Optional['WorkspaceManager'] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(WorkspaceManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, size_mb: int = 2048):
        if self._initialized:
            return

        self.total_size = size_mb * 1024 * 1024
        self.allocated = 0
        self._workspaces: Dict[str, Any] = {}
        self._channels: Dict[int, Any] = {}
        self._magic_header = 0xDEADBEEF
        self.predictive = PredictiveWorkspace(self)

        # Performance metrics
        self.last_sync_time = time.time()
        self.sync_jitters: List[float] = []

        if rc and hasattr(rc, "workspace_init_rust"):
            try:
                self._handle = rc.workspace_init_rust(self.total_size)
                logger.info(f"Initialized Rust workspace of {size_mb}MB")
            except Exception as e:
                logger.error(f"Failed to initialize Rust workspace: {e}")
                self._handle = None
        else:
            self._handle = None

        self._initialized = True
        logger.info(f"WorkspaceManager initialized with {size_mb}MB total capacity")

    def allocate_dbo(self, name: str, size: int) -> Optional[memoryview]:
        """
        Allocates a named Distributed Byte Object in the workspace.
        Uses Predictive buffer if available, otherwise allocates new.
        """
        # Phase 58: Check predictive buffer first
        buffered = self.predictive.get_buffered_allocation(size)
        if buffered:
            logger.debug(f"Workspace: Reusing pre-warmed buffer for {name}")
            return buffered

        if self.allocated + size > self.total_size:
            logger.error(f"Workspace overflow: Attempted {size} bytes, {self.total_size - self.allocated} left")
            return None

        self.predictive.record_allocation(size)

        if rc and self._handle and hasattr(rc, "workspace_alloc_rust"):
            try:
                # In a real implementation, this returns a memory-mapped pointer
                ptr = rc.workspace_alloc_rust(self._handle, name, size)
                if ptr:
                    # Logic to wrap pointer in memoryview or similar
                    pass
            except Exception as e:
                logger.debug(f"Rust allocation fallback: {e}")

        # Standard memory allocation
        buf = bytearray(size)
        self._workspaces[name] = buf
        self.allocated += size
        return memoryview(buf)

    def register_dvd_channel(self, channel_id: int, buffer_size: int = 8192):
        """
        Registers a high-speed 120fps DVD-like channel.
        Channels are synchronized to the global inference clock.
        """
        with self._lock:
            name = f"dvd_ch_{channel_id:04d}"
            dbo = self.allocate_dbo(name, buffer_size)
            if dbo:
                self._channels[channel_id] = {
                    "buffer": dbo,
                    "name": name,
                    "last_beat": time.time()
                }
                logger.debug(f"Registered DVD-channel {channel_id} (DBO: {name})")
                return True
            return False

    def global_sync_beat(self):
        """
        Sends a synchronization beat across all active 120fps channels.
        Target jitter: < 1.0ms.
        """
        now = time.time()
        jitter = (now - self.last_sync_time) - (1.0/120.0)
        self.sync_jitters.append(jitter)
        if len(self.sync_jitters) > 120:
            self.sync_jitters.pop(0)

        if rc and hasattr(rc, "workspace_sync_beat_rust"):
            rc.workspace_sync_beat_rust(self._handle)

        self.last_sync_time = now

    def get_utilization(self) -> float:
        """Returns the current memory utilization percentage."""
        if self.total_size == 0:
            return 0.0
        return (self.allocated / self.total_size) * 100.0

    def purge(self):
        """Clears all allocations and resets the workspace."""
        with self._lock:
            self._workspaces.clear()
            self._channels.clear()
            self.allocated = 0
            if rc and self._handle and hasattr(rc, "workspace_purge_rust"):
                rc.workspace_purge_rust(self._handle)
            logger.info("WorkspaceManager purged and reset")
