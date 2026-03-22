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
"""Minimal MemoryStore core module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class MemoryStore:
    """Simple in-memory key-value store."""

    _store: Optional[dict[str, Any]] = None

    def __post_init__(self) -> None:
        """Post-init to ensure the store dict is created lazily."""
        if self._store is None:
            self._store = {}

    def set(self, key: str, value: Any) -> None:
        """Set a value in the memory store."""
        assert self._store is not None
        self._store[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the memory store, or default if not found."""
        assert self._store is not None
        return self._store.get(key, default)


    def delete(self, key: str) -> bool:
        """Delete a key; returns True if the key existed."""
        assert self._store is not None
        if key in self._store:
            del self._store[key]
            return True
        return False

    def keys(self) -> list[str]:
        """Return all stored keys."""
        assert self._store is not None
        return list(self._store.keys())

    def __len__(self) -> int:
        """Return number of stored entries."""
        return len(self._store) if self._store is not None else 0


def validate() -> None:
    """Lightweight import-safe validation hook."""
    m = MemoryStore()
    m.set("k", 123)
    assert m.get("k") == 123
