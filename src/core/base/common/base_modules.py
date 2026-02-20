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


"""Lifecycle definitions for core modules."""


from __future__ import annotations


try:
    from abc import ABC, abstractmethod
except ImportError:
    from abc import ABC, abstractmethod

try:
    from typing import Any
except ImportError:
    from typing import Any




class BaseModule(ABC):
    """Base class for all core modules in the swarm.
    Standardizes the lifecycle of global specialized logic.
    """
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}
        self.initialized = False


    def initialize(self) -> bool:
        """Sets up the module resources."""
        self.initialized = True
        return True


    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Main entry point for module logic."""
        raise NotImplementedError()


    def shutdown(self) -> bool:
        """Cleans up the module resources."""
        self.initialized = False
        return True
