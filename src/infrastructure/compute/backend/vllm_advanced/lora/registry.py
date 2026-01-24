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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
LoRA adapter registry.
"""

import logging
from typing import Dict, List, Optional

from .models import AdapterState, LoraAdapter

logger = logging.getLogger(__name__)


class LoraRegistry:
    """
    Registry for tracking available LoRA adapters.

    Maintains a catalog of adapters that can be loaded on demand.
    """

    def __init__(self):
        self._adapters: Dict[str, LoraAdapter] = {}
        self._id_counter = 1
        self._name_to_id: Dict[str, int] = {}

    def register(
        self,
        name: str,
        path: str,
        base_model: Optional[str] = None,
        rank: Optional[int] = None,
        alpha: Optional[float] = None,
        target_modules: Optional[List[str]] = None,
    ) -> LoraAdapter:
        """
        Register a new LoRA adapter.
        """
        if name in self._adapters:
            logger.warning(f"Adapter '{name}' already registered, updating")
            adapter = self._adapters[name]
            adapter.path = path
            adapter.base_model = base_model
            adapter.rank = rank
            adapter.alpha = alpha
            if target_modules:
                adapter.target_modules = target_modules
            return adapter

        adapter_id = self._id_counter
        self._id_counter += 1

        adapter = LoraAdapter(
            adapter_id=adapter_id,
            name=name,
            path=path,
            base_model=base_model,
            rank=rank,
            alpha=alpha,
            target_modules=target_modules or [],
        )

        self._adapters[name] = adapter
        self._name_to_id[name] = adapter_id

        logger.info(f"Registered LoRA adapter: {name} (ID: {adapter_id})")
        return adapter

    def unregister(self, name: str) -> bool:
        """Remove an adapter from the registry."""
        if name not in self._adapters:
            return False

        self._adapters.pop(name)
        self._name_to_id.pop(name, None)

        logger.info(f"Unregistered LoRA adapter: {name}")
        return True

    def get(self, name: str) -> Optional[LoraAdapter]:
        """Get adapter by name."""
        return self._adapters.get(name)

    def get_by_id(self, adapter_id: int) -> Optional[LoraAdapter]:
        """Get adapter by ID."""
        for adapter in self._adapters.values():
            if adapter.adapter_id == adapter_id:
                return adapter
        return None

    def list_adapters(self) -> List[LoraAdapter]:
        """List all registered adapters."""
        return list(self._adapters.values())

    def list_loaded(self) -> List[LoraAdapter]:
        """List adapters that are currently loaded."""
        return [a for a in self._adapters.values() if a.state in (AdapterState.LOADED, AdapterState.ACTIVE)]

    def find_by_base_model(self, base_model: str) -> List[LoraAdapter]:
        """Find adapters compatible with a base model."""
        return [a for a in self._adapters.values() if a.base_model == base_model]
