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


from __future__ import annotations
from src.core.base.version import VERSION
import logging
import time
import random
from typing import Dict, List, Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

__version__ = VERSION

class HolographicContextAgent(BaseAgent):
    """
    Agent that manages multi-perspective context snapshots (Holograms).
    Allows agents to view the same project state from different architectural angles
    (e.g., Security, Performance, Maintainability, UX).
    """
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.holograms: dict[str, dict[str, Any]] = {}
        self._system_prompt = (
            "You are the Holographic Context Agent. "
            "Your role is to maintain multi-perspective snapshots of the project. "
            "You allow other agents to 'rotate' the project state to view it from different architectural angles."
        )

    @as_tool
    def create_hologram(self, name: str, state_data: dict[str, Any], angles: list[str] = ["security", "performance"]) -> str:
        """
        Creates a multi-angle 'hologram' of the provided state data.
        """
        hologram = {
            "timestamp": time.time(),
            "source_data": state_data,
            "perspectives": {}
        }
        
        for angle in angles:
            # In a real system, this would call specialized agents or use specific prompts to 're-view' the data
            hologram["perspectives"][angle] = {
                "summary": f"Perspective on {angle} for {name}",
                "metrics": {angle: random.uniform(0.1, 1.0) if 'random' in globals() else 0.5},
                "recommendations": [f"Improve {angle} by doing X."]
            }
            
        self.holograms[name] = hologram
        logging.info(f"Hologram created: {name} with {len(angles)} perspectives.")
        return f"Successfully created hologram '{name}'."

    @as_tool
    def view_perspective(self, name: str, angle: str) -> dict[str, Any]:
        """
        Returns a specific perspective from a named hologram.
        """
        if name in self.holograms:
            h = self.holograms[name]
            return h["perspectives"].get(angle, {"error": f"Angle '{angle}' not found in hologram '{name}'."})
        return {"error": f"Hologram '{name}' not found."}

    @as_tool
    def list_holograms(self) -> list[str]:
        """
        List all active context holograms.
        """
        return list(self.holograms.keys())