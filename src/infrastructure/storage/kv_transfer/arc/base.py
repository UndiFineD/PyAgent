"""
Phase 45: ARC Offload Base
Abstract base for offloading managers.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING
from src.infrastructure.storage.kv_transfer.arc.types import BlockHash, LoadStoreSpec, PrepareStoreOutput

if TYPE_CHECKING:
    pass


class OffloadingManager(ABC):
    """Abstract base for offloading managers."""
    
    @abstractmethod
    def lookup(self, block_hashes: list[BlockHash]) -> int:
        """Look up blocks, return hit count."""
        pass
    
    @abstractmethod
    def prepare_load(self, block_hashes: list[BlockHash]) -> LoadStoreSpec:
        """Prepare to load blocks."""
        pass
    
    @abstractmethod
    def touch(self, block_hashes: list[BlockHash]) -> None:
        """Update access recency for blocks."""
        pass
    
    @abstractmethod
    def complete_load(self, block_hashes: list[BlockHash]) -> None:
        """Complete load operation."""
        pass
    
    @abstractmethod
    def prepare_store(
        self,
        block_hashes: list[BlockHash]
    ) -> PrepareStoreOutput | None:
        """Prepare to store blocks, returns None if cannot make space."""
        pass
