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


"""Engine for automated self-repair of agent tools and modules.
Detects runtime errors and orchestrates CoderAgents to apply fixes.
"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import logging
import traceback
from typing import Any
from src.core.base.lifecycle.base_agent import BaseAgent
from .self_healing_engine_core import SelfHealingEngineCore

__version__ = VERSION


class SelfHealingEngine:
    """
    Monitors tool execution and attempts automatic fixes for crashes.
    Shell for SelfHealingEngineCore.
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = workspace_root
        self.failure_history: list[dict[str, Any]] = []
        self.core = SelfHealingEngineCore()

    def handle_failure(
        self,
        agent: BaseAgent,
        tool_name: str,
        error: Exception,
        context: dict[str, Any],
    ) -> str:
        """Analyzes a failure and attempts to generate a fix."""
        tb = traceback.format_exc()
        agent_name = agent.__class__.__name__
        logging.error(f"SELF-HEAL: Failure in {agent_name}.{tool_name}: {error}\n{tb}")

        analysis = self.core.analyze_failure(agent_name, tool_name, str(error), tb)
        analysis["context"] = context
        self.failure_history.append(analysis)

        # Fixed logic: communicate strategy
        return f"Self-Healing initiated: Strategy '{analysis['strategy']}' assigned to {tool_name}."

    def get_healing_stats(self) -> str:
        """Returns a summary of healing attempts."""
        return self.core.format_healing_report(self.failure_history)
