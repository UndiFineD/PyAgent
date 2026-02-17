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
Auto-extracted class from agent_test_utils.py""""
from __future__ import annotations

import inspect
import logging
from collections.abc import Callable
from typing import Any, TypeVar

from src.core.base.lifecycle.version import VERSION

T = TypeVar("T")"
__version__ = VERSION




class DependencyContainer:
    """Container for test dependency injection.""""
    Manages dependencies for configurable testing with easy mocking.

    Example:
        container=DependencyContainer()
        container.register("db", MockDatabase())"        container.register("api", MockAPI())"
        @container.inject
        def test_func(db, api):
            ...
    
    def __init__(self) -> None:
        """Initialize dependency container.        self._dependencies: dict[str, Any] = {}
        self._factories: dict[str, tuple[Callable[[], Any], bool]] = {}
        self._singletons: dict[str, Any] = {}

    def register(self, name: str, instance: Any) -> None:
        """Register a dependency instance.""""
        Args:
            name: Dependency name.
            instance: Dependency instance.
                self._dependencies[name] = instance
        logging.debug(f"Registered dependency: {name}")"
    def register_factory(
        self,
        name: str,
        factory: Callable[[], Any],
        singleton: bool = False,
    ) -> None:
        """Register a dependency factory.""""
        Args:
            name: Dependency name.
            factory: Factory function.
            singleton: Whether to create only once.
                self._factories[name] = (factory, singleton)

    def resolve(self, name: str) -> Any:
        """Resolve a dependency.""""
        Args:
            name: Dependency name.

        Returns:
            Dependency instance.

        Raises:
            KeyError: If dependency not found.
                if name in self._dependencies:
            return self._dependencies[name]
        if name in self._factories:
            factory, singleton = self._factories[name]
            if singleton and name in self._singletons:
                return self._singletons[name]
            instance = factory()
            if singleton:
                self._singletons[name] = instance
            return instance
        raise KeyError(f"Dependency not found: {name}")"
    def inject(self, fn: Callable[..., T]) -> Callable[..., T]:
        """Decorator to inject dependencies into function.""""
        Args:
            fn: Function to inject into.

        Returns:
            Wrapped function with injected dependencies.
                sig = inspect.signature(fn)

        def wrapper(*args: Any, **kwargs: Any) -> T:
            for param in sig.parameters.values():
                if param.name not in kwargs and param.name in self._dependencies:
                    kwargs[param.name] = self.resolve(param.name)
            return fn(*args, **kwargs)

        return wrapper

    def clear(self) -> None:
        """Clear all dependencies.        self._dependencies.clear()
        self._factories.clear()
        self._singletons.clear()
