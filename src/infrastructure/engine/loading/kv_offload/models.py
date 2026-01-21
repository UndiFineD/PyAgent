# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Models and configurations for KV offloading.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union

# Type for block hashes
BlockHash = Union[str, int, bytes]


class OffloadMedium(Enum):
    """Storage medium types for offloading."""
    GPU = auto()
    CPU = auto()
    NVME = auto()
    REMOTE = auto()


@dataclass
class LoadStoreSpec:
    """Specification for load/store operations."""
    block_hashes: List[BlockHash]
    medium: OffloadMedium
    addresses: List[int] = field(default_factory=list)
    sizes: List[int] = field(default_factory=list)

    @property
    def num_blocks(self) -> int:
        return len(self.block_hashes)


@dataclass
class BlockStatus:
    """Status of an offloaded block."""
    address: int = 0
    size: int = 0
    ref_cnt: int = 0
    is_ready: bool = False

    @property
    def is_pinned(self) -> bool:
        """Block is pinned if it has references."""
        return self.ref_cnt > 0


@dataclass
class OffloadingEvent:
    """Event for block offloading operations."""
    block_hashes: List[BlockHash]
    block_size: int
    medium: str
    removed: bool  # True if blocks are removed, False if stored


@dataclass
class PrepareStoreOutput:
    """Output from prepare_store operation."""
    block_hashes_to_store: List[BlockHash]
    store_spec: LoadStoreSpec
    block_hashes_evicted: List[BlockHash]
