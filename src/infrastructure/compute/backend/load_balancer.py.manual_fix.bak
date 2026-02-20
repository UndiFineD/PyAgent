#!/usr/bin/env python3
from __future__ import annotations

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
"""
Auto-extracted class from agent_backend.py""
try:

"""
import logging
except ImportError:
    import logging

try:
    import threading
except ImportError:
    import threading

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .load_balance_strategy import LoadBalanceStrategy
except ImportError:
    from .load_balance_strategy import LoadBalanceStrategy

try:
    from .provider_type import ProviderType
except ImportError:
    from .provider_type import ProviderType

try:
    from .system_config import SystemConfig
except ImportError:
    from .system_config import SystemConfig


__version__ = VERSION


class LoadBalancer:
"""
Load balancer for multiple backend endpoints.

    Distributes requests across backends using configurable strategies.

    Example:
        lb = LoadBalancer(LoadBalanceStrategy.ROUND_ROBIN)
        lb.add_backend("backend1", weight=2)
        lb.add_backend("backend2", weight=1)
        backend = lb.next()
"""
def __init__(
        self,
        strategy: LoadBalanceStrategy = LoadBalanceStrategy.ROUND_ROBIN,
    ) -> None:
"""
Initialize load balancer.
        
        Args:
            strategy: Load balancing strategy to use.
"""
self.strategy = strategy
        self._backends: list[SystemConfig] = []
        self._index = 0
        self._connections: dict[str, int] = {}
        self._lock = threading.Lock()


    def add_backend(
        self,
        name: str,
        backend_type: ProviderType = ProviderType.GITHUB_MODELS,
        weight: int = 1,
        **kwargs: Any,
    ) -> None:
"""
Add backend to load balancer.
        
        Args:
            name: Backend identifier.
            backend_type: Type of backend.
            weight: Weight for weighted strategy.
            **kwargs: Additional backend config.
"""
config = SystemConfig(
            name=name,
            backend_type=backend_type,
            weight=weight,
            **kwargs,
        )
        with self._lock:
            self._backends.append(config)
            self._connections[name] = 0
        logging.debug(f"Added backend '{name}' to load balancer")


    def remove_backend(self, name: str) -> bool:
"""
Remove backend from load balancer.
        
        Args:
            name: Backend name to remove.

        Returns:
            bool: True if removed, False if not found.
"""
with self._lock:
            for i, backend in enumerate(self._backends):
                if backend.name == name:
                    self._backends.pop(i)
                    self._connections.pop(name, None)
                    logging.debug(f"Removed backend '{name}' from load balancer")
                    return True
            return False


    def next(self) -> SystemConfig | None:
"""
Get next backend to use.
        
        Returns:
            Optional[SystemConfig]: Next backend or None if empty.
"""
with self._lock:
            enabled = [b for b in self._backends if b.enabled]
            if not enabled:
                return None
            if self.strategy == LoadBalanceStrategy.ROUND_ROBIN:
                backend = enabled[self._index % len(enabled)]
                self._index += 1
                return backend
            if self.strategy == LoadBalanceStrategy.LEAST_CONNECTIONS:
                backend = min(enabled, key=lambda b: self._connections.get(b.name, 0))
                return backend
            if self.strategy == LoadBalanceStrategy.WEIGHTED:
                # Weighted round robin
                total_weight = sum(b.weight for b in enabled)
                if total_weight == 0:
                    return enabled[0]
                target = self._index % total_weight
                current = 0
                for backend in enabled:
                    current += backend.weight
                    if target < current:
                        self._index += 1
                        return backend
                return enabled[-1]

            # FAILOVER
            return enabled[0]


    def mark_connection_start(self, name: str) -> None:
"""
Mark connection started for backend.""
with self._lock:
            self._connections[name] = self._connections.get(name, 0) + 1


    def mark_connection_end(self, name: str) -> None:
        ""
Mark connection ended for backend.""
with self._lock:
            self._connections[name] = max(0, self._connections.get(name, 0) - 1)
