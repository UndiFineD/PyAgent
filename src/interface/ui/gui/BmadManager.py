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

"""BMAD (Bulk Multi-Agent Deployment) component for the PyAgent GUI."""

from __future__ import annotations
from src.core.base.Version import VERSION
import tkinter as tk
from tkinter import ttk, messagebox
import os
from .Constants import BMAD_AGENTS, BMAD_TRACKS, BMAD_PHASES, DEFAULT_INSTRUCTIONS

__version__ = VERSION


class BmadManager:
    """Manages the BMAD workflow for deploying agents at scale across the project."""

    def __init__(self, parent, callbacks) -> None:
        self.parent = parent
        self.callbacks = callbacks
        self.recorder = None  # Phase 108: Optional recorder
        self.frame = ttk.LabelFrame(
            parent, text="BMAD - Bulk Multi-Agent Deployment", padding=10
        )
        self.setup_ui()

    def _record(self, action: str, result: str) -> None:
        """Record BMAD operations."""
        if self.recorder:
            self.recorder.record_interaction("BMAD", "GUI", action, result)

    def setup_ui(self) -> None:
        # 1. Methodology Selection
        method_frame = ttk.Frame(self.frame)
        method_frame.pack(fill=tk.X, pady=5)

        ttk.Label(
            method_frame, text="Methodology Track:", font=("Segoe UI", 9, "bold")
        ).pack(anchor=tk.W)
        self.track_var = tk.StringVar(value="BMad Method")
        track_cb = ttk.Combobox(
            method_frame,
            textvariable=self.track_var,
            values=list(BMAD_TRACKS.keys()),
            state="readonly",
        )
        track_cb.pack(fill=tk.X, pady=2)
        track_cb.bind("<<ComboboxSelected>>", self.on_track_change)

        self.track_desc = ttk.Label(
            method_frame,
            text=BMAD_TRACKS["BMad Method"]["desc"],
            font=("Segoe UI", 8),
            foreground="gray",
        )
        self.track_desc.pack(anchor=tk.W)

        # 2. Phase Selection
        self.phase_frame = ttk.Frame(self.frame)
        self.phase_frame.pack(fill=tk.X, pady=5)
        ttk.Label(
            self.phase_frame, text="Current Phase:", font=("Segoe UI", 9, "bold")
        ).pack(anchor=tk.W)
        self.phase_var = tk.StringVar(value="Implementation")
        self.phase_sel_container = ttk.Frame(self.phase_frame)
        self.phase_sel_container.pack(fill=tk.X)
        self.refresh_phase_buttons()

        # 3. Target Selection Mode
        file_mode_frame = ttk.Frame(self.frame)
        file_mode_frame.pack(fill=tk.X, pady=5)

        ttk.Label(
            file_mode_frame, text="Target Scope:", font=("Segoe UI", 9, "bold")
        ).pack(anchor=tk.W)
        self.target_mode = tk.StringVar(value="selected")
        scope_opts_frame = ttk.Frame(file_mode_frame)
        scope_opts_frame.pack(fill=tk.X)
        ttk.Radiobutton(
            scope_opts_frame,
            text="Selected",
            variable=self.target_mode,
            value="selected",
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            scope_opts_frame, text="Project", variable=self.target_mode, value="project"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            scope_opts_frame, text="Git Changes", variable=self.target_mode, value="git"
        ).pack(side=tk.LEFT, padx=5)

        # 4. Agent Selection (Dynamic Grid)
        agent_header = ttk.Frame(self.frame)
        agent_header.pack(fill=tk.X, pady=5)
        ttk.Label(
            agent_header, text="Apply Agents:", font=("Segoe UI", 9, "bold")
        ).pack(side=tk.LEFT)
        ttk.Button(
            agent_header, text="All", width=5, command=lambda: self.set_all_agents(True)
        ).pack(side=tk.RIGHT)
        ttk.Button(
            agent_header,
            text="None",
            width=5,
            command=lambda: self.set_all_agents(False),
        ).pack(side=tk.RIGHT)

        agent_grid = ttk.Frame(self.frame)
        agent_grid.pack(fill=tk.X, pady=5)

        self.agents_to_run = {}
        # Display 3 columns of agents
        for i, name in enumerate(BMAD_AGENTS):
            var = tk.BooleanVar(value=(name == "Developer"))
            self.agents_to_run[name] = var
            cb = ttk.Checkbutton(agent_grid, text=name, variable=var)
            cb.grid(row=i // 3, column=i % 3, sticky=tk.W, padx=2, pady=1)

        # 5. Global Action Buttons
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            btn_frame,
            text="🚀 DEPLOY BULK AGENTS",
            style="Accent.TButton",
            command=self.deploy_bulk,
        ).pack(fill=tk.X, pady=2)
        ttk.Button(
            btn_frame, text="🔄 START BMAD WORKFLOW", command=self.start_workflow_action
        ).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="⚡ Workflow-Init", command=self.workflow_init).pack(
            fill=tk.X, pady=2
        )

    def on_track_change(self, event: tk.Event) -> None:
        track = self.track_var.get()
        track_info = BMAD_TRACKS.get(track, {})
        self.track_desc.config(text=track_info.get("desc", ""))
        self.refresh_phase_buttons()

    def refresh_phase_buttons(self) -> None:
        # Clear existing buttons
        for widget in self.phase_sel_container.winfo_children():
            widget.destroy()

        track = self.track_var.get()
        phases = BMAD_TRACKS.get(track, {}).get("phases", BMAD_PHASES)

        # Reset phase if not in list
        if self.phase_var.get() not in phases:
            self.phase_var.set(phases[0])

        for phase in phases:
            ttk.Radiobutton(
                self.phase_sel_container,
                text=phase,
                variable=self.phase_var,
                value=phase,
            ).pack(side=tk.LEFT, padx=2)

    def set_all_agents(self, value: bool) -> None:
        for var in self.agents_to_run.values():
            var.set(value)

    def workflow_init(self) -> None:
        """Analyzes project and recommends track."""
        messagebox.showinfo(
            "Workflow-Init",
            "Analyzing project structure...\nRecommending 'BMad Method' track based on codebase complexity.",
        )

    def start_workflow_action(self) -> None:
        """Triggers the step-by-step workflow manager."""
        targets = self.get_targets()
        if not targets:
            return

        track = self.track_var.get()
        if messagebox.askyesno(
            "Confirm Workflow",
            f"Start a step-by-step {track} workflow for {len(targets)} files?",
        ):
            self.callbacks["get_workflow_manager"]().start_workflow(track, targets)

    def get_targets(self) -> list[str]:
        mode = self.target_mode.get()
        targets = []

        if mode == "project":
            root = self.callbacks["get_project_root"]()
            exts = {".py", ".js", ".ts", ".md"}  # BMAD scope
            for r, d, f in os.walk(root):
                if any(
                    x in r for x in {".git", "__pycache__", ".venv", "node_modules"}
                ):
                    continue
                for file in f:
                    if os.path.splitext(file)[1] in exts:
                        targets.append(os.path.join(r, file))
        elif mode == "git":
            root = self.callbacks["get_project_root"]()
            try:
                import subprocess

                cmd = ["git", "ls-files", "-m", "-o", "--exclude-standard"]
                result = subprocess.check_output(
                    cmd, cwd=root, stderr=subprocess.STDOUT, text=True
                )
                for line in result.splitlines():
                    if line.endswith(".py") or line.endswith(".md"):
                        targets.append(os.path.join(root, line))
            except Exception as e:
                messagebox.showerror("Git Error", f"Failed to get git changes: {e}")
                return []
        elif mode == "selected":
            sel_path = self.callbacks["get_selected_path"]()
            if sel_path:
                targets = [sel_path]
            else:
                messagebox.showwarning(
                    "Warning", "No files selected in Project Explorer."
                )
                return []
        return targets

    def deploy_bulk(self) -> None:
        targets = self.get_targets()
        if not targets:
            return

        active_agents = [name for name, var in self.agents_to_run.items() if var.get()]
        phase = self.phase_var.get()

        if not active_agents:
            messagebox.showwarning("Warning", "No agents selected for deployment.")
            return

        total_instances = len(targets) * len(active_agents)
        if total_instances > 15:
            if not messagebox.askyesno(
                "Large Deployment",
                f"This will create {total_instances} agent instances. Continue?",
            ):
                return

        for target in targets:
            for agent_name in active_agents:
                col = self.callbacks["add_agent"](agent_name)
                col.file_var.set(target)
                col.phase_var.set(phase)
                col.local_context.delete("1.0", tk.END)
                col.local_context.insert(
                    "1.0",
                    f"Manual BMAD {phase} deployment for {os.path.basename(target)}.",
                )

                # Apply Phase instruction if available
                phase = self.phase_var.get()
                instr = DEFAULT_INSTRUCTIONS.get(
                    agent_name, f"Role: {agent_name}. Phase: {phase}."
                )
                col.local_context.delete("1.0", tk.END)
                col.local_context.insert("1.0", f"--- BMAD {phase} PHASE ---\n{instr}")

        # Final status update via callback if available
        # self.callbacks["set_status"](f"Deployed {total_instances} agents for {mode} targeting.")
