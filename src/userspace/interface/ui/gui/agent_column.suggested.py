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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent Column component for the PyAgent GUI."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class AgentColumn:
    """A vertical column representing a single agent's controls and logs."""

    def __init__(self, parent: tk.Widget, agent_name: str, callbacks: dict[str, Any]) -> None:
        self.agent_name = agent_name
        self.callbacks = callbacks

        # Unpack callbacks for convenience
        self.execute_callback = callbacks.get("execute")
        self.stop_callback = callbacks.get("stop")
        self.browse_file_callback = callbacks.get("browse_file")
        self.voice_callback = callbacks.get("voice")
        self.remove_callback = callbacks.get("remove")
        self.diff_callback = callbacks.get("diff")
        self.show_settings_callback = callbacks.get("show_settings")

        self.is_running = False
        self.instance = None
        self.phase_var = tk.StringVar(value="None")
        self.is_minimized = False

        self.frame = ttk.LabelFrame(parent, text=f"Agent: {agent_name}", style="Agent.TLabelframe")
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.setup_ui()

    def setup_ui(self) -> None:
        # Header
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=2, pady=2)

        # Minimize Toggle
        self.min_btn = ttk.Button(header_frame, text="▼", width=3, command=self.toggle_minimize)
        self.min_btn.pack(side=tk.LEFT, padx=(0, 5))

        ttk.Label(header_frame, text=self.agent_name, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)

        # Phase Indicator
        phase_lbl = tk.Label(
            header_frame,
            textvariable=self.phase_var,
            font=("Segoe UI", 8, "bold"),
            fg="white",
            bg="#007acc",
            padx=5,
        )
        phase_lbl.pack(side=tk.LEFT, padx=10)

        # Actions in Header
        close_btn = ttk.Button(
            header_frame,
            text="✕",
            width=3,
            command=lambda: self.remove_callback(self.frame, self.agent_name),
        )
        close_btn.pack(side=tk.RIGHT)

        dup_btn = ttk.Button(
            header_frame,
            text="📑",
            width=3,
            command=lambda: self.callbacks.get("duplicate")(self.get_data()),
        )
        dup_btn.pack(side=tk.RIGHT, padx=2)

        # Content Container (so we can hide it easily)
        self.content_frame = ttk.Frame(self.frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # File
        path_frame = ttk.Frame(self.content_frame)
        path_frame.pack(fill=tk.X, padx=2, pady=2)
        ttk.Label(path_frame, text="Target File:").pack(anchor=tk.W)
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(path_frame, textvariable=self.file_var)
        self.file_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        ttk.Button(
            path_frame,
            text="...",
            width=2,
            command=lambda: self.browse_file_callback(self.file_var),
        ).pack(side=tk.RIGHT)

        # Context
        self.ctx_toggle = ttk.Button(self.content_frame, text="Toggle Local Context", command=self.toggle_context)
        self.ctx_toggle.pack(fill=tk.X, padx=2, pady=2)

        self.local_context = tk.Text(self.content_frame, height=4, font=("Consolas", 9), bg="#f9f9f9")
        self.local_context.insert("1.0", f"Specific instructions for {self.agent_name}...")

        # Log
        log_header = ttk.Frame(self.content_frame)
        log_header.pack(fill=tk.X, padx=2)
        ttk.Label(log_header, text="Log & Memory:").pack(side=tk.LEFT)
        ttk.Button(
            log_header,
            text="Diff",
            width=5,
            command=lambda: self.diff_callback(self.agent_name),
        ).pack(side=tk.RIGHT)
        ttk.Button(
            log_header,
            text="ClrLog",
            width=6,
            command=lambda: self.log_text.delete("1.0", tk.END),
        ).pack(side=tk.RIGHT)
        ttk.Button(
            log_header,
            text="Memory",
            width=8,
            command=lambda: self.callbacks.get("show_memory")(self.agent_name),
        ).pack(side=tk.RIGHT)
        ttk.Button(log_header, text="Delegate", width=8, command=self.show_delegate_menu).pack(side=tk.RIGHT)

        self.log_text = tk.Text(
            self.content_frame,
            height=15,
            bg="#1e1e1e",
            fg="#d4d4d4",
            font=("Consolas", 9),
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.progress = ttk.Progressbar(self.content_frame, mode="indeterminate")

        # Prompt Area (Consolidated at bottom, Copilot-style)
        control_area = ttk.Frame(self.content_frame)
        control_area.pack(fill=tk.X, side=tk.BOTTOM, padx=4, pady=4)

        # Mini Toolbar for settings/model
        mini_toolbar = ttk.Frame(control_area)
        mini_toolbar.pack(fill=tk.X, pady=(0, 2))

        self.model_cb = ttk.Combobox(
            mini_toolbar,
            values=["default", "gpt-4.1", "gpt-3.5-turbo", "claude-3-5-sonnet"],
            width=12,
            font=("Segoe UI", 8),
        )
        self.model_cb.set("default")
        self.model_cb.pack(side=tk.LEFT, padx=1)

        self.backend_cb = ttk.Combobox(
            mini_toolbar,
            values=["auto", "copilot", "gh", "github-models"],
            width=8,
            font=("Segoe UI", 8),
        )
        self.backend_cb.set("auto")
        self.backend_cb.pack(side=tk.LEFT, padx=1)

        ttk.Button(mini_toolbar, text="⚙️", width=3, command=self.show_settings_callback).pack(side=tk.LEFT, padx=1)

        # Task Prompt
        prompt_container = ttk.Frame(control_area)
        prompt_container.pack(fill=tk.X)

        self.prompt_text = tk.Text(prompt_container, height=3, font=("Consolas", 10), undo=True)
        self.prompt_text.pack(fill=tk.X, side=tk.TOP)

        # Actions at bottom right
        action_bar = ttk.Frame(control_area)
        action_bar.pack(fill=tk.X, pady=2)

        self.run_btn = ttk.Button(
            action_bar,
            text="▶️",
            width=5,
            command=lambda: self.execute_callback(self.agent_name),
        )
        self.run_btn.pack(side=tk.RIGHT, padx=1)

        self.stop_btn = ttk.Button(
            action_bar,
            text="⏹️",
            width=3,
            state=tk.DISABLED,
            command=lambda: self.stop_callback(self.agent_name),
        )
        self.stop_btn.pack(side=tk.RIGHT, padx=1)

        self.voice_btn = ttk.Button(
            action_bar,
            text="🎤",
            width=3,
            command=lambda: self.voice_callback(self.prompt_text),
        )
        self.voice_btn.pack(side=tk.RIGHT, padx=1)

    def toggle_minimize(self) -> None:
        """Collapses or expands the agent's content."""
        if self.is_minimized:
            self.content_frame.pack(fill=tk.BOTH, expand=True)
            self.min_btn.config(text="▼")
        else:
            self.content_frame.pack_forget()
            self.min_btn.config(text="▶")
        self.is_minimized = not self.is_minimized

    def remove_placeholder(self, frame: tk.Widget, name: str) -> None:
        """Standard remove method."""

    def reset_memory(self) -> None:
        """Clears the conversation history for this agent."""
        if messagebox.askyesno("Reset Memory", "Clear conversation history for this agent?"):
            self.stop_callback(self.agent_name, reset_history=True)
            self.log_text.insert(tk.END, "\n[Memory Reset]\n")

    def show_delegate_menu(self) -> None:
        """Shows a menu to delegate the current result to another agent."""
        from .constants import BMAD_AGENTS

        menu = tk.Menu(self.frame, tearoff=0)
        for agent in BMAD_AGENTS:
            if agent != self.agent_name:
                menu.add_command(
                    label=f"Delegate to {agent}",
                    command=lambda a=agent: self.delegate_to(a),
                )

        try:
            menu.tk_popup(self.frame.winfo_pointerx(), self.frame.winfo_pointery())
        finally:
            menu.grab_release()

    def delegate_to(self, target_agent: str) -> None:
        """Passes the current log output as context to a new agent."""
        content = self.log_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Log is empty. Nothing to delegate.")
            return

        # Create new agent column
        # We need to access agent_manager or use a callback
        self.log_text.insert(tk.END, f"\n[Delegating to {target_agent}...]\n")
        # In this implementation, the parent AgentDashboard or MainApp should handle this
        # For now, we'll try to use a callback if we have one, or just log the intent
        if hasattr(self, "delegate_callback") and self.delegate_callback:
            self.delegate_callback(target_agent, content, self.file_var.get())

    def toggle_context(self) -> None:
        """Toggle the visibility of the local context text area."""
        if self.local_context.winfo_viewable():
            self.local_context.pack_forget()
        else:
            self.local_context.pack(fill=tk.X, padx=2, pady=2, after=self.ctx_toggle)

    def get_data(self) -> dict:
        """Get the current UI state as a dictionary."""
        return {
            "name": self.agent_name,
            "file": self.file_var.get(),
            "backend": self.backend_cb.get(),
            "model": self.model_cb.get(),
            "local_context": self.local_context.get("1.0", tk.END).strip(),
            "prompt": self.prompt_text.get("1.0", tk.END).strip(),
        }

    def set_data(self, data: dict) -> None:
        """Set the UI state from a dictionary."""
        self.file_var.set(data.get("file", ""))
        self.backend_cb.set(data.get("backend", "auto"))
        self.model_cb.set(data.get("model", "default"))
        self.local_context.delete("1.0", tk.END)
        self.local_context.insert("1.0", data.get("local_context", ""))
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert("1.0", data.get("prompt", ""))

    def get_config(self) -> dict:
        """Get the configuration for persistent storage."""
        return {
            "type": self.agent_name,
            "backend": self.backend_cb.get(),
            "model": self.model_cb.get(),
            "file": self.file_var.get(),
        }

    def on_start(self) -> None:
        """Update UI state when agent starts processing."""
        self.is_running = True
        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.pack(fill=tk.X, padx=2, pady=2, after=self.log_text)
        self.progress.start()

    def on_finish(self) -> None:
        """Update UI state when agent finishes processing."""
        self.is_running = False
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress.stop()
        self.progress.pack_forget()
