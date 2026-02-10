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
Generic Registry for dynamic class/function registration and lookup.

Provides a thread-safe registry pattern for plugins, factories, and dynamic dispatch.
"""

import threading
from typing import Any, Dict, TypeVar

T = TypeVar("T")


class Registry:
    """
    Thread-safe registry for mapping string keys to callables or classes.
    Useful for plugin systems, factories, and dynamic dispatch.
    """
    def __init__(self):
        self._lock = threading.RLock()
        self._registry: Dict[str, Any] = {}

    def register(self, name: str, obj: Any) -> None:
        with self._lock:
            if name in self._registry:
                raise KeyError(f"'{name}' is already registered.")
            self._registry[name] = obj

    def unregister(self, name: str) -> None:
        with self._lock:
            if name in self._registry:
                del self._registry[name]

    def get(self, name: str) -> Any:
        with self._lock:
            if name not in self._registry:
                raise KeyError(f"'{name}' is not registered.")
            return self._registry[name]

    def has(self, name: str) -> bool:
        with self._lock:
            return name in self._registry

    def all(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._registry)


__all__ = ["Registry"]
