#!/usr/bin/env python3
"""Registry core - parser-safe minimal implementation."""
from __future__ import annotations

from typing import Callable, Dict, Generic, List, Optional, TypeVar
import logging

T = TypeVar("T")

logger = logging.getLogger("pyagent.registry")


class RegistryCore(Generic[T]):
    """Small, well-formed registry for tests and fallbacks."""

    def __init__(self, name: str = "generic") -> None:
        self.name = name
        self._items: Dict[str, T] = {}
        self._hooks: Dict[str, List[Callable[[str, T], None]]] = {"on_register": [], "on_unregister": []}

    def register(self, key: str, item: Optional[T] = None) -> bool:
        if item is None:
            # If item omitted, store a simple sentinel
            self._items[key] = ""  # type: ignore
        else:
            self._items[key] = item
        for hook in self._hooks.get("on_register", []):
            try:
                hook(key, self._items[key])
            except Exception as e:
                logger.debug("on_register hook failed: %s", e)
        return True

    def unregister(self, key: str) -> Optional[T]:
        item = self._items.pop(key, None)
        if item:
            for hook in self._hooks.get("on_unregister", []):
                try:
                    hook(key, item)
                except Exception:
                    pass
        return item

    def get(self, key: str) -> Optional[T]:
        return self._items.get(key)

    def list_keys(self) -> List[str]:
        return list(self._items.keys())

    def list_items(self) -> List[T]:
        return list(self._items.values())

    def clear(self) -> None:
        self._items.clear()

    def add_hook(self, event: str, callback: Callable[[str, T], None]) -> None:
        if event in self._hooks:
            self._hooks[event].append(callback)
        else:
            raise ValueError(f"Unsupported registry event: {event}")

