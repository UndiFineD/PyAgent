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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Engine for dynamic task decomposition.
Breaks complex user requests into granular sub-tasks for the agent fleet.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import List, Dict, Any
from .TaskDecomposerCore import TaskDecomposerCore

__version__ = VERSION

class TaskDecomposer:
    """
    Analyzes high-level requests and generates a multi-step plan.
    Shell for TaskDecomposerCore.
    """

    def __init__(self, fleet_manager: Any) -> None:
        self.fleet = fleet_manager
        self.core = TaskDecomposerCore()

    def decompose(self, request: str) -> list[dict[str, Any]]:
        """Splits a request into a sequence of agent steps."""
        logging.info(f"Decomposing task: {request}")
        steps = self.core.generate_plan(request)
        logging.info(f"Generated {len(steps)} steps for task.")
        return steps

    def get_plan_summary(self, steps: list[dict[str, Any]]) -> str:
        return self.core.summarize_plan(steps)