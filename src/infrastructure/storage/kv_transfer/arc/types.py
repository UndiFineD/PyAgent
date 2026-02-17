#!/usr/bin/env python3

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
Phase 45: ARC Offload Types
Data structures and enums for ARC offloading.

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Union

# Type for block hash
BlockHash = Union[bytes, str, int]


class OffloadMedium(Enum):
    """Storage medium for offloaded blocks.
    GPU = auto()
    CPU = auto()
    DISK = auto()
    REMOTE = auto()


class BlockState(Enum):
    """State of an offloaded block.
    PENDING = auto()  # Store/load in progress
    READY = auto()  # Available for use
    EVICTING = auto()  # Being evicted
    INVALID = auto()  # Needs refresh


@dataclass(slots=True)
class BlockStatus:
    """Status of a cached block.
    block_id: int
    medium: OffloadMedium = OffloadMedium.GPU
    state: BlockState = BlockState.READY
    ref_cnt: int = 0
    size_bytes: int = 0
    compressed: bool = False
    last_access_time: float = 0.0
    importance_score: float = 1.0  # KVzap importance score (arXiv:2601.07891)

    @property
    def is_ready(self) -> bool:
        """Check if block is ready for reading.        return self.state == BlockState.READY

    @property
    def can_evict(self) -> bool:
        """Check if block can be evicted.        return self.ref_cnt == 0 and self.state == BlockState.READY


@dataclass(frozen=True, slots=True)
class LoadStoreSpec:
    """Specification for load/store operation.
    block_hashes: list[BlockHash]
    blocks: list[BlockStatus]
    source_medium: OffloadMedium = OffloadMedium.CPU
    target_medium: OffloadMedium = OffloadMedium.GPU


@dataclass(frozen=True, slots=True)
class OffloadingEvent:
    """Event representing offloading operation.
    block_hashes: list[BlockHash]
    block_size: int
    medium: OffloadMedium
    removed: bool  # True for eviction, False for addition
    timestamp: float = field(default_factory=time.time)


@dataclass(slots=True)
class PrepareStoreOutput:
    """Output from prepare_store operation.
    block_hashes_to_store: list[BlockHash]
    store_spec: LoadStoreSpec
    block_hashes_evicted: list[BlockHash]
