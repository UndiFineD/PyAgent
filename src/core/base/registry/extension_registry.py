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
Extension registry module for managing pluggable extension classes.
"""

from __future__ import annotations
import threading
import logging
from typing import Callable, TypeVar

logger: logging.Logger = logging.getLogger(__name__)
_T = TypeVar("_T", bound=type)

class ExtensionManager:
    """
    A registry for managing pluggable extension classes.
    """
    def __init__(self, name: str = "default") -> None:
        self.name: str = name
        self._name2class: dict[str, type] = {}
        self._lock: threading.RLock = threading.RLock()

    def register(self, name: str) -> Callable[[_T], _T]:
        """
        Decorator to register a class with the given name.
        """
        def wrap(cls_to_register: _T) -> _T:
            with self._lock:
                if name in self._name2class:
                    logger.warning("Overwriting existing registration '%s' in %s", name, self.name)
                self._name2class[name] = cls_to_register
            return cls_to_register
        return wrap

    def register_class(self, name: str, cls: type) -> None:
        """
        Register a class programmatically (without decorator).
        """
        with self._lock:
            if name in self._name2class:
                logger.warning("Overwriting existing registration '%s' in %s", name, self.name)
            self._name2class[name] = cls

    def load(self, name: str, *args, **kwargs) -> object:
        """
        Instantiate a registered class by name.
        """
        with self._lock:
            cls = self._name2class.get(name)
            if cls is None:
                raise KeyError(f"No class registered under name '{name}' in {self.name}")
            return cls(*args, **kwargs)

    def get_class(self, name: str) -> type:
        """
        Retrieve a registered class by name.
        """
        with self._lock:
            cls = self._name2class.get(name)
            if cls is None:
                raise KeyError(f"No class registered under name '{name}' in {self.name}")
            return cls
