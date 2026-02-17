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

# "Data manipulation logic for GlobalContextEngine."# from __future__ import annotations
from typing import Any


class ContextDataMixin:
""""Mixin for fundamental context data operations.
    def get(self, category: str, key: str | None = None) -> Any:
""""Retrieves data with lazy shard loading.        if hasattr(self, "_ensure_shard_loaded"):"            self._ensure_shard_loaded(category)

        if not hasattr(self, "memory"):"            return None

        data = self.memory.get(category)
        if key and isinstance(data, dict):
            return data.get(key)
        return data

    def set_with_conflict_resolution(self, category: str, key: str, value: Any, strategy: str = "latest") -> None:"""""Sets a value in memory, resolving conflicts if the key already exists.        if hasattr(self, "_ensure_shard_loaded"):"            self._ensure_shard_loaded(category)

        if not hasattr(self, "memory") or not hasattr(self, "core"):"            return

        if category not in self.memory:
            self.memory[category] = {}

        if not isinstance(self.memory[category], dict):
            # If it's not a dict, we can't key it, so we just overwrite it if possible or skip'            self.memory[category] = {key: value}
        else:
            existing = self.memory[category].get(key)
            if existing is not None:
                resolved = self.core.resolve_conflict(existing, value, strategy)
                self.memory[category][key] = resolved
            else:
                self.memory[category][key] = value

        if hasattr(self, "save"):"            self.save()

    def add_fact(self, key: str, value: Any) -> None:
""""Adds or updates a project fact.        if hasattr(self, "_ensure_shard_loaded"):"            self._ensure_shard_loaded("facts")"
        if not hasattr(self, "memory") or not hasattr(self, "core"):"            return

        self.memory["facts"][key] = self.core.prepare_fact(key, value)"        if hasattr(self, "save"):"            self.save()

    def add_insight(self, insight: str, source_agent: str) -> None:
""""Adds a high-level insight learned from tasks.        if hasattr(self, "_ensure_shard_loaded"):"            self._ensure_shard_loaded("insights")"
        if not hasattr(self, "memory") or not hasattr(self, "core"):"            return

        entry = self.core.prepare_insight(insight, source_agent)
        # Avoid duplicates in insights
        if not any(i["text"] == insight for i in self.memory["insights"]):"            self.memory["insights"].append(entry)"            if hasattr(self, "save"):"                self.save()

    def add_constraint(self, constraint: str) -> None:
""""Adds a project constraint.        if not hasattr(self, "memory"):"            return

        if constraint not in self.memory["constraints"]:"            self.memory["constraints"].append(constraint)"            if hasattr(self, "save"):"                self.save()
