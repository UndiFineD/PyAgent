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
"""Minimal Agent Registry core module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class AgentRegistry:
    """Simple registry for agent instances or definitions."""

    _registry: Optional[dict[str, Any]] = None

    def __post_init__(self) -> None:
        """Post-init to ensure the registry dict is created lazily."""
        if self._registry is None:
            self._registry = {}

    def register(self, name: str, obj: Any) -> None:
        """Register an object under a given name."""
        assert self._registry is not None
        self._registry[name] = obj

    def get(self, name: str) -> Optional[Any]:
        """Retrieve a registered object by name, or None if not found."""
        assert self._registry is not None
        return self._registry.get(name)


def validate() -> None:
    """Lightweight import-safe validation hook."""
    r = AgentRegistry()
    r.register("test-agent", object())
    assert r.get("test-agent") is not None
