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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Workflow management for step-by-step BMAD project execution."""

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Any
from tkinter import messagebox

__version__ = VERSION




class WorkflowManager:
    """Manages the lifecycle of a complex development workflow."""
    def __init__(self, callbacks) -> None:
        self.callbacks: Any = callbacks
        self.current_step_index = 0
        self.workflow_active = False

    def start_workflow(self, track_name, targets) -> None:
        """Starts a predefined workflow based on the track."""
        from .Constants import BMAD_TRACKS
        track = BMAD_TRACKS.get(track_name)
        if not track:
            return

        self.phases = track["phases"]
        self.targets = targets
        self.current_step_index = 0
        self.workflow_active = True

        self.execute_current_phase()

    def execute_current_phase(self) -> None:
        """Executes the current phase of the workflow."""
        if self.current_step_index >= len(self.phases):
            self.finish_workflow()
            return

        phase = self.phases[self.current_step_index]
        self.callbacks["set_status"](f"Workflow: {phase} Phase starting...")

        # Decide which agents to deploy based on phase
        agents: list[str] = self.get_agents_for_phase(phase)

        for target in self.targets:
            for agent in agents:
                col = self.callbacks["add_agent"](agent)
                col.file_var.set(target)
                col.phase_var.set(phase)
                col.local_context.insert("1.0", f"--- BMAD {phase.upper()} PHASE ---\nExecute {phase} tasks for {target}.")

    def get_agents_for_phase(self, phase) -> list[str]:
        """Returns a list of agent names needed for a specific phase."""
        mapping: dict[str, list[str]] = {
            "Analysis": ["Analyst", "PM"],
            "Planning": ["PM", "Architect"],
            "Solutioning": ["Architect", "UX Designer"],
            "Implementation": ["Developer"],
            "Quality": ["Test Architect"],
            "Validation": ["Test Architect", "BMad Master"],
            "Governance": ["Scrum Master", "Security Auditor"]
        }
        return mapping.get(phase, ["Developer"])

    def next_phase(self) -> None:
        """Moves to the next phase in the workflow."""
        if not self.workflow_active:
            return
        self.current_step_index += 1
        self.execute_current_phase()

    def finish_workflow(self) -> None:
        """Clean up after workflow completion."""
        self.workflow_active = False
        self.callbacks["set_status"]("Workflow completed successfully.")
        messagebox.showinfo("Success", "The BMAD workflow has reached its final phase.")
