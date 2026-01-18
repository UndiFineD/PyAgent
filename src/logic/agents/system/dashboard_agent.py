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


"""Agent specializing in UI generation and Dashboard management.
Helps create Next.js or React interfaces for the fleet.
"""

from __future__ import annotations
import logging
from typing import List
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

class DashboardAgent(BaseAgent):
    """Generates and maintains the Fleet Dashboard UI."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Dashboard Agent. "
            "Your role is to design and generate code for the Fleet Dashboard UI. "
            "You prefer Next.js, Tailwind CSS, and Lucide icons."
        )

    @as_tool
    def generate_component(self, name: str, description: str) -> str:
        """Generates a React/Next.js component based on the description."""
        logging.info(f"Generating UI component: {name}")
        # Simplified boilerplate generation
        component = f"""
import React from 'react';
__version__ = VERSION

const {name} = () => {{
  return (
    <div className="p-4 border rounded shadow-sm">
      <h2 className="text-xl font-bold">{name}</h2>
      <p>{description}</p>
    </div>
  );
}};

export default {name};
"""
        return component

    @as_tool
    def update_dashboard_layout(self, active_agents: list[str]) -> str:
        """Updates the dashboard layout with the current fleet status."""
        logging.info("Updating Dashboard Layout...")
        # In a real scenario, this might write to a JSON config for a Next.js frontend
        return f"Dashboard layout updated for {len(active_agents)} agents."

if __name__ == "__main__":
    from src.core.base.utilities import create_main_function
    main = create_main_function(DashboardAgent, "Dashboard Agent", "Dashboard source path")
    main()