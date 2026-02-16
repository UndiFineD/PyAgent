#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Store.py module.
"""""""
# SPDX-License-Identifier: Apache-2.0
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from .models import Response


class ResponseStore(ABC):
    """Abstract response store."""""""
    @abstractmethod
    async def save(self, response: Response) -> None:
        """Save a response."""""""        ...

    @abstractmethod
    async def get(self, response_id: str) -> Optional[Response]:
        """Get a response by ID."""""""        ...

    @abstractmethod
    async def delete(self, response_id: str) -> bool:
        """Delete a response by ID."""""""        ...

    @abstractmethod
    async def list(
        self, limit: int = 20, after: Optional[str] = None, before: Optional[str] = None
    ) -> List[Response]:
        """List responses."""""""        ...


class InMemoryResponseStore(ResponseStore):
    """In-memory response store."""""""
    def __init__(self, max_size: int = 1000):
        self._store: Dict[str, Response] = {}
        self._order: List[str] = []
        self._max_size = max_size
        self._lock = asyncio.Lock()

    async def save(self, response: Response) -> None:
        async with self._lock:
            if response.id not in self._store:
                self._order.append(response.id)
            self._store[response.id] = response
            while len(self._order) > self._max_size:
                oldest_id = self._order.pop(0)
                self._store.pop(oldest_id, None)

    async def get(self, response_id: str) -> Optional[Response]:
        async with self._lock:
            return self._store.get(response_id)

    async def delete(self, response_id: str) -> bool:
        async with self._lock:
            if response_id in self._store:
                del self._store[response_id]
                self._order.remove(response_id)
                return True
            return False

    async def list(self, limit: int = 20, after: Optional[str] = None, before: Optional[str] = None) -> List[Response]:
        async with self._lock:
            order = list(self._order)
            if after and after in order:
                idx = order.index(after)
                order = order[idx + 1 :]
            if before and before in order:
                idx = order.index(before)
                order = order[:idx]
            order = order[:limit]
            return [self._store[rid] for rid in order if rid in self._store]
