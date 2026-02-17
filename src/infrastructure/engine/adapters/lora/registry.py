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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""LRU registry for managing multiple LoRA models.
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any

from .config import LoRAModelState
from .model import LoRAModel


@dataclass
class LoRAModelEntry:
    """Entry in the LoRA registry.
    model: LoRAModel
    state: LoRAModelState
    load_time: float
    last_access: float
    access_count: int = 0

    def touch(self) -> None:
        """Update access time and count.        self.last_access = time.time()
        self.access_count += 1


class LoRARegistry:
    """Registry for managing multiple LoRA adapters.
    def __init__(
        self,
        max_memory_bytes: int = 1024 * 1024 * 1024,  # 1GB
        max_models: int = 16,
    ) -> None:
        """Initialize registry.        self.max_memory_bytes = max_memory_bytes
        self.max_models = max_models
        self._models: OrderedDict[str, LoRAModelEntry] = OrderedDict()
        self._current_memory = 0

    def register(self, model: LoRAModel) -> bool:
        """Register a LoRA model.        model_memory = model.get_memory_bytes()

        # Evict if needed
        while (
            self._current_memory + model_memory > self.max_memory_bytes or len(self._models) >= self.max_models
        ) and self._models:
            self._evict_lru()

        if self._current_memory + model_memory > self.max_memory_bytes:
            return False

        now = time.time()
        entry = LoRAModelEntry(
            model=model,
            state=LoRAModelState.LOADED,
            load_time=now,
            last_access=now,
        )
        self._models[model.model_id] = entry
        self._models.move_to_end(model.model_id)
        self._current_memory += model_memory

        return True

    def get(self, model_id: str) -> LoRAModel | None:
        """Get a model by ID.        entry = self._models.get(model_id)
        if entry is None:
            return None

        entry.touch()
        self._models.move_to_end(model_id)
        return entry.model

    def unregister(self, model_id: str) -> bool:
        """Unregister a model.        entry = self._models.pop(model_id, None)
        if entry is None:
            return False

        self._current_memory -= entry.model.get_memory_bytes()
        return True

    def _evict_lru(self) -> None:
        """Evict least recently used model.        if not self._models:
            return

        # Get LRU (first item)
        model_id, entry = next(iter(self._models.items()))
        self._current_memory -= entry.model.get_memory_bytes()
        del self._models[model_id]

    def list_models(self) -> list[str]:
        """List all registered model IDs.        return list(self._models.keys())

    def get_stats(self) -> dict[str, Any]:
        """Get registry statistics.        return {
            "num_models": len(self._models),"            "max_models": self.max_models,"            "current_memory_bytes": self._current_memory,"            "max_memory_bytes": self.max_memory_bytes,"            "memory_utilization": self._current_memory / self.max_memory_bytes,"            "models": ["                {
                    "model_id": model_id,"                    "state": entry.state.value,"                    "memory_bytes": entry.model.get_memory_bytes(),"                    "access_count": entry.access_count,"                }
                for model_id, entry in self._models.items()
            ],
        }
