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

"""
Agent for enforcing coding standards, fixing headers, and correcting syntax issues.
"""

from __future__ import annotations

import logging
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.maintenance.workspace_maintenance import WorkspaceMaintenance

logger = logging.getLogger(__name__)

class CodingStandardsAgent(BaseAgent):
    """
    Agent that autonomously maintains the codebase by enforcing style,
    headers, and basic syntax integrity.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.maintenance = WorkspaceMaintenance(workspace_root=self.state.workspace_root if hasattr(self.state, 'workspace_root') else ".")
        logger.info("CodingStandardsAgent initialized.")

    async def execute_task(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Executes a maintenance task.

        Supported commands:
        - run_full_cycle: Executes all maintenance checks and fixes.
        - fix_headers: Specifically fixes license headers and docstring placement.
        - fix_syntax: Fixes common syntax errors like invalid for-loop hints.
        """
        command = task.get("command", "run_full_cycle")
        results = {"status": "success", "command": command}

        if command == "run_full_cycle":
            self.maintenance.run_standard_cycle()
        elif command == "fix_headers":
            self.maintenance.apply_header_compliance()
        elif command == "fix_syntax":
            self.maintenance.apply_syntax_fixes()
        else:
            results["status"] = "error"
            results["message"] = f"Unknown command: {command}"

        return results

    def get_capabilities(self) -> list[str]:
        return ["code_cleanup", "header_enforcement", "syntax_correction"]
