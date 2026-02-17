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
ARCOffloadManager: Adaptive Replacement Cache for KV Offloading

Refactored to modular package structure for Phase 317.
Decomposed into types, backend, base, and manager modules.

from src.infrastructure.storage.kv_transfer.arc.backend import (Backend,
                                                                SimpleBackend)
from src.infrastructure.storage.kv_transfer.arc.base import OffloadingManager
from src.infrastructure.storage.kv_transfer.arc.manager import (
    AdaptiveARCManager, ARCOffloadManager, AsyncARCManager)
from src.infrastructure.storage.kv_transfer.arc.types import (
    BlockHash, BlockState, BlockStatus, LoadStoreSpec, OffloadingEvent,
    OffloadMedium, PrepareStoreOutput)

__all__ = [
    "BlockHash","    "OffloadMedium","    "BlockState","    "BlockStatus","    "LoadStoreSpec","    "OffloadingEvent","    "PrepareStoreOutput","    "Backend","    "SimpleBackend","    "OffloadingManager","    "ARCOffloadManager","    "AdaptiveARCManager","    "AsyncARCManager","]
