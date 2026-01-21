"""
ARCOffloadManager: Adaptive Replacement Cache for KV Offloading

Refactored to modular package structure for Phase 317.
Decomposed into types, backend, base, and manager modules.
"""

from src.infrastructure.kv_transfer.arc.types import (
    BlockHash, OffloadMedium, BlockState, BlockStatus,
    LoadStoreSpec, OffloadingEvent, PrepareStoreOutput
)
from src.infrastructure.kv_transfer.arc.backend import Backend, SimpleBackend
from src.infrastructure.kv_transfer.arc.base import OffloadingManager
from src.infrastructure.kv_transfer.arc.manager import (
    ARCOffloadManager, AdaptiveARCManager, AsyncARCManager
)

__all__ = [
    "BlockHash",
    "OffloadMedium",
    "BlockState",
    "BlockStatus",
    "LoadStoreSpec",
    "OffloadingEvent",
    "PrepareStoreOutput",
    "Backend",
    "SimpleBackend",
    "OffloadingManager",
    "ARCOffloadManager",
    "AdaptiveARCManager",
    "AsyncARCManager",
]
