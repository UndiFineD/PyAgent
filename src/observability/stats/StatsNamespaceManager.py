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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_stats.py"""



from .StatsNamespace import StatsNamespace

from typing import Dict, Optional



































class StatsNamespaceManager:
    """Manages multiple namespaces."""
    def __init__(self) -> None:
        self.namespaces: Dict[str, StatsNamespace] = {}

    def create(self, name: str) -> StatsNamespace:
        """Create a new namespace."""
        ns = StatsNamespace(name)
        self.namespaces[name] = ns
        return ns

    def create_namespace(self, name: str) -> StatsNamespace:
        """Create a new namespace (backward compat)."""
        return self.create(name)

    def get_namespace(self, name: str) -> Optional[StatsNamespace]:
        """Get a namespace."""
        return self.namespaces.get(name)
