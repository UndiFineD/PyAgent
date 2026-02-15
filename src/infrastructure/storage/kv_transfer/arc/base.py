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
Phase 45: ARC Offload Base
Abstract base for offloading managers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.infrastructure.storage.kv_transfer.arc.types import (
    BlockHash, LoadStoreSpec, PrepareStoreOutput)

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
    def prepare_store(self, block_hashes: list[BlockHash]) -> PrepareStoreOutput | None:
        """Prepare to store blocks, returns None if cannot make space."""
        pass
