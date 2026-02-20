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
Phase 45: ARC Offload Backends
Backends for block storage in the ARC offloading system.
"""

try:
    import threading
except ImportError:
    import threading

try:
    from abc import ABC, abstractmethod
except ImportError:
    from abc import ABC, abstractmethod


try:
    from .infrastructure.storage.kv_transfer.arc.types import (BlockHash,
except ImportError:
    from src.infrastructure.storage.kv_transfer.arc.types import (BlockHash,

                                                              BlockState,
                                                              BlockStatus,
                                                              LoadStoreSpec,
                                                              OffloadMedium)



class Backend(ABC):
    """Abstract backend for block storage.
    @abstractmethod
    def get_num_free_blocks(self) -> int:
        """Get number of free blocks.        pass

    @abstractmethod
    def allocate_blocks(self, block_hashes: list[BlockHash]) -> list[BlockStatus]:
        """Allocate blocks for given hashes.        pass

    @abstractmethod
    def free(self, block: BlockStatus) -> None:
        """Free a block.        pass

    @abstractmethod
    def get_load_store_spec(self, block_hashes: list[BlockHash], blocks: list[BlockStatus]) -> LoadStoreSpec:
        """Get load/store specification.        pass

    @property
    @abstractmethod
    def block_size(self) -> int:
        """Get block size in tokens.        pass

    @property
    @abstractmethod
    def medium(self) -> OffloadMedium:
        """Get storage medium.        pass



class SimpleBackend(Backend):
    """Simple in-memory backend for testing.
    def __init__(self, num_blocks: int = 1000, block_size: int = 16, medium: OffloadMedium = OffloadMedium.CPU):
        self._num_blocks = num_blocks
        self._block_size = block_size
        self._medium = medium
        self._allocated: dict[BlockHash, BlockStatus] = {}
        self._next_id = 0
        self._lock = threading.Lock()

    def get_num_free_blocks(self) -> int:
        with self._lock:
            return self._num_blocks - len(self._allocated)

    def allocate_blocks(self, block_hashes: list[BlockHash]) -> list[BlockStatus]:
        blocks = []
        with self._lock:
            for h in block_hashes:
                if h not in self._allocated:
                    block = BlockStatus(block_id=self._next_id, medium=self._medium, state=BlockState.PENDING)
                    self._allocated[h] = block
                    self._next_id += 1
                blocks.append(self._allocated[h])
        return blocks

    def free(self, block: BlockStatus) -> None:
        with self._lock:
            # Find and remove block
            to_remove = None
            for h, b in self._allocated.items():
                if b.block_id == block.block_id:
                    to_remove = h
                    break
            if to_remove:
                del self._allocated[to_remove]

    def get_load_store_spec(self, block_hashes: list[BlockHash], blocks: list[BlockStatus]) -> LoadStoreSpec:
        return LoadStoreSpec(
            block_hashes=list(block_hashes),
            blocks=list(blocks),
            source_medium=self._medium,
            target_medium=OffloadMedium.GPU,
        )

    @property
    def block_size(self) -> int:
        return self._block_size

    @property
    def medium(self) -> OffloadMedium:
        return self._medium
