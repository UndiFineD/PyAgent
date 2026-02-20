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


# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Base classes for KV offloading backends and managers.
"""

try:
    from abc import ABC, abstractmethod
except ImportError:
    from abc import ABC, abstractmethod

try:
    from typing import Iterable, List, Optional
except ImportError:
    from typing import Iterable, List, Optional


try:
    from .models import BlockHash, BlockStatus, LoadStoreSpec, PrepareStoreOutput
except ImportError:
    from .models import BlockHash, BlockStatus, LoadStoreSpec, PrepareStoreOutput




class OffloadingBackend(ABC):
    """Abstract backend for block storage.
    @property
    @abstractmethod
    def medium(self) -> str:
        """Return storage medium identifier.        raise NotImplementedError

    @property
    @abstractmethod
    def block_size(self) -> int:
        """Return block size in bytes.        raise NotImplementedError

    @abstractmethod
    def get_num_free_blocks(self) -> int:
        """Get number of available blocks.        raise NotImplementedError

    @abstractmethod
    def allocate_blocks(self, block_hashes: List[BlockHash]) -> List[BlockStatus]:
        """Allocate storage for blocks.        raise NotImplementedError

    @abstractmethod
    def free(self, block: BlockStatus) -> None:
        """Free a block's storage.'        raise NotImplementedError

    @abstractmethod
    def get_load_store_spec(
        self,
        block_hashes: Iterable[BlockHash],
        blocks: List[BlockStatus],
    ) -> LoadStoreSpec:
        """Create load/store specification.        raise NotImplementedError



class OffloadingManager(ABC):
    """Abstract manager for KV cache offloading.
    @abstractmethod
    def lookup(self, block_hashes: Iterable[BlockHash]) -> int:
        """Find length of maximal cached prefix.        raise NotImplementedError

    @abstractmethod
    def prepare_load(self, block_hashes: Iterable[BlockHash]) -> LoadStoreSpec:
        """Prepare blocks for loading.        raise NotImplementedError

    @abstractmethod
    def touch(self, block_hashes: Iterable[BlockHash]) -> None:
        """Mark blocks as recently used.        raise NotImplementedError

    @abstractmethod
    def complete_load(self, block_hashes: Iterable[BlockHash]) -> None:
        """Mark load as complete.        raise NotImplementedError

    @abstractmethod
    def prepare_store(
        self,
        block_hashes: Iterable[BlockHash],
    ) -> Optional[PrepareStoreOutput]:
        """Prepare to store blocks.        raise NotImplementedError

    @abstractmethod
    def complete_store(
        self,
        block_hashes: Iterable[BlockHash],
        success: bool = True,
    ) -> None:
        """Mark store as complete.        raise NotImplementedError
