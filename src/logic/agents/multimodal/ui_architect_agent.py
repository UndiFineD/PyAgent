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
Ui architect agent.py module.
"""


from __future__ import annotations

from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


# pylint: disable=too-many-ancestors
class UiArchitectAgent(BaseAgent):
    """
    Phase 54: UI Architect Agent.
    Designs and generates dynamic UI layouts for the Fleet Dashboard.
    Uses the 'Tambo' pattern for generative UI.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.layouts: dict[str, Any] = {}

    def design_dashboard_layout(self, active_workflow: str, agent_list: list[str]) -> dict[str, Any]:
        """Creates a layout JSON based on active agents and workflow type."""
        layout = {
            "title": f"Live View: {active_workflow}",
            "grid": {"columns": 3, "rows": 2},
            "panels": [
                {
                    "title": "Fleet Topology",
                    "type": "graph",
                    "position": {"x": 0, "y": 0, "w": 2, "h": 2},
                },
                {
                    "title": "Recent Events",
                    "type": "list",
                    "position": {"x": 2, "y": 0, "w": 1, "h": 1},
                },
                {
                    "title": "Resource Allocation",
                    "type": "chart",
                    "position": {"x": 2, "y": 1, "w": 1, "h": 1},
                },
            ],
        }

        # Inject agent-specific stats panels if many agents
        if len(agent_list) > 5:
            layout["panels"].append(
                {
                    "title": "Agent Heatmap",
                    "type": "heatmap",
                    "position": {"x": 0, "y": 2, "w": 3, "h": 1},
                }
            )
            layout["grid"]["rows"] += 1

        return layout

    def generate_ui_manifest(self, task_context: str) -> dict[str, Any]:
        """Determines which dynamic components should be rendered based on context strings."""
        manifest = {"requested_plugins": [], "theme": "dark_mode"}

        if "sql" in task_context.lower():
            manifest["requested_plugins"].append("SQL_Explorer")
        if "chart" in task_context.lower() or "plot" in task_context.lower():
            manifest["requested_plugins"].append("Data_Visualizer")

        return manifest