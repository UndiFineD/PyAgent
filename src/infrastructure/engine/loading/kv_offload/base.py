# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Base classes for KV offloading backends and managers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Optional

from .models import (
    BlockHash,
    BlockStatus,
    LoadStoreSpec,
    PrepareStoreOutput,
)


class OffloadingBackend(ABC):
    """Abstract backend for block storage."""

    @property
    @abstractmethod
    def medium(self) -> str:
        """Return storage medium identifier."""
        pass

    @property
    @abstractmethod
    def block_size(self) -> int:
        """Return block size in bytes."""
        pass

    @abstractmethod
    def get_num_free_blocks(self) -> int:
        """Get number of available blocks."""
        pass

    @abstractmethod
    def allocate_blocks(self, block_hashes: List[BlockHash]) -> List[BlockStatus]:
        """Allocate storage for blocks."""
        pass

    @abstractmethod
    def free(self, block: BlockStatus) -> None:
        """Free a block's storage."""
        pass

    @abstractmethod
    def get_load_store_spec(
        self,
        block_hashes: Iterable[BlockHash],
        blocks: List[BlockStatus],
    ) -> LoadStoreSpec:
        """Create load/store specification."""
        pass


class OffloadingManager(ABC):
    """Abstract manager for KV cache offloading."""

    @abstractmethod
    def lookup(self, block_hashes: Iterable[BlockHash]) -> int:
        """Find length of maximal cached prefix."""
        pass

    @abstractmethod
    def prepare_load(self, block_hashes: Iterable[BlockHash]) -> LoadStoreSpec:
        """Prepare blocks for loading."""
        pass

    @abstractmethod
    def touch(self, block_hashes: Iterable[BlockHash]) -> None:
        """Mark blocks as recently used."""
        pass

    @abstractmethod
    def complete_load(self, block_hashes: Iterable[BlockHash]) -> None:
        """Mark load as complete."""
        pass

    @abstractmethod
    def prepare_store(
        self,
        block_hashes: Iterable[BlockHash],
    ) -> Optional[PrepareStoreOutput]:
        """Prepare to store blocks."""
        pass

    @abstractmethod
    def complete_store(
        self,
        block_hashes: Iterable[BlockHash],
        success: bool = True,
    ) -> None:
        """Mark store as complete."""
        pass
