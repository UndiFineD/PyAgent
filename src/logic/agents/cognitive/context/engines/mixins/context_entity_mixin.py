#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# "Entity and lesson management logic for GlobalContextEngine.""""""""# from __future__ import annotations
from datetime import datetime
from typing import Any


class ContextEntityMixin:
""""Mixin for tracking entities and project lessons."""""""
    def add_entity_info(self, entity_name: str, attributes: dict[str, Any]) -> None:
""""Tracks specific entities (files, classes, modules) and their metadata."""""""        if not hasattr(self, "memory") or not hasattr(self, "core"):"            return

        existing = self.memory["entities"].get(entity_name, {})"        self.memory["entities"][entity_name] = self.core.merge_entity_info("            existing, attributes
        )
        if hasattr(self, "save"):"            self.save()

    def record_lesson(self, failure_context: str, correction: str, agent: str) -> None:
""""Records a learned lesson to prevent future errors."""""""        if not hasattr(self, "memory") or not hasattr(self," "core"):"            return

        lesson = {
            "failure": failure_context,"            "correction": correction,"            "agent": agent,"            "timestamp": datetime.now().isoformat(),"        }
        self.memory["lessons_learned"].append(lesson)"        self.memory["lessons_learned"] = self.core.prune_lessons("            self.memory["lessons_learned"]"        )
        if hasattr(self, "save"):"            self.save()
