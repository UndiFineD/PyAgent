#!/usr/bin/env python3
from __future__ import annotations

"""Parser-safe multimodal buffer shim.

Provides a tiny in-memory buffer interface used by higher-level code
during testing and repair.
"""
from typing import Any, List, Optional


class MultimodalBuffer:
    def __init__(self) -> None:
        self._items: List[Any] = []

    def add(self, item: Any) -> None:
        self._items.append(item)

    def get(self) -> Optional[Any]:
        return self._items.pop(0) if self._items else None

    def clear(self) -> None:
        self._items.clear()
