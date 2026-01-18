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


"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .RollbackPoint import RollbackPoint
from typing import Any, Dict, List

__version__ = VERSION

class RollbackManager:
    """Stores rollback points and can restore the latest state."""

    def __init__(self) -> None:
        self.rollbacks: list[RollbackPoint] = []
        self._by_id: dict[str, list[RollbackPoint]] = {}

    def create_rollback_point(self, improvement_id: str, state: dict[str, Any]) -> RollbackPoint:
        point = RollbackPoint(improvement_id=improvement_id, state=dict(state))
        self.rollbacks.append(point)
        self._by_id.setdefault(improvement_id, []).append(point)
        return point

    def rollback(self, improvement_id: str) -> dict[str, Any]:
        points = self._by_id.get(improvement_id, [])
        if not points:
            return {}
        point = points[-1]
        return dict(point.state)