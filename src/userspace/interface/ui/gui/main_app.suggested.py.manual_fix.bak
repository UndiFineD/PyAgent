#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Main application controller for PyAgent GUI.

"""
try:
    import os
except ImportError:
    import os

try:
    import tkinter
except ImportError:
    import tkinter
 as tk
try:
    from collections.abc import Callable
except ImportError:
    from collections.abc import Callable

try:
    from tkinter import ttk
except ImportError:
    from tkinter import ttk

try:
    from typing import Any, Self
except ImportError:
    from typing import Any, Self


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .agent_dashboard import AgentDashboard
except ImportError:
    from .agent_dashboard import AgentDashboard

try:
    from .agent_manager import AgentManager
except ImportError:
    from .agent_manager import AgentManager

try:
    from .agent_runner import AgentRunner
except ImportError:
    from .agent_runner import AgentRunner

try:
    from .app_menu import AppMenu
except ImportError:
    from .app_menu import AppMenu

try:
    from .bmad_manager import BmadManager
except ImportError:
    from .bmad_manager import BmadManager

try:
    from .configuration_manager import ConfigurationManager
except ImportError:
    from .configuration_manager import ConfigurationManager

try:
    from .dialog_manager import DialogManager
except ImportError:
    from .dialog_manager import DialogManager

try:
    from .diff_viewer import DiffViewer
except ImportError:
    from .diff_viewer import DiffViewer

try:
    from .header_panel import HeaderPanel
except ImportError:
    from .header_panel import HeaderPanel

try:
    from .project_explorer import ProjectExplorer
except ImportError:
    from .project_explorer import ProjectExplorer

try:
    from .project_status_panel import ProjectStatusPanel
except ImportError:
    from .project_status_panel import ProjectStatusPanel

try:
    from .session_manager import SessionManager
except ImportError:
    from .session_manager import SessionManager

try:
    from .status_bar import StatusBar
except ImportError:
    from .status_bar import StatusBar

try:
    from .theme_manager import ThemeManager
except ImportError:
    from .theme_manager import ThemeManager

try:
    from .workflow_manager import WorkflowManager
except ImportError:
    from .workflow_manager import WorkflowManager


__version__ = VERSION



class PyAgentGUI:
"""
The main application window and controller.

    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.root.title("PyAgent Control Center - BMAD Enabled")"        self.root.geometry("1400x900")"
        # UI State (Init before managers)
        self.project_root_var = tk.StringVar(value=os.getcwd())
        self.status_var = tk.StringVar(value="Ready")
        # Managers
        self.config_manager = ConfigurationManager()
        self.dialogs = DialogManager(self.root)
        self.workflow_manager: WorkflowManager[dict[str, Callable[..., None] | Callable[..., Any]]] = WorkflowManager(
            {
                "set_status": self.status_var.set,"                "add_agent": lambda name: self.agent_manager.add_column(name),"            }
        )

        # Backend components
        self.session_manager = SessionManager("gui_session.json")"        self.theme_manager: ThemeManager[tk.Tk] = ThemeManager(self.root)
        self.diff_viewer: DiffViewer[tk.Tk] = DiffViewer(self.root)
        self.agent_runner: AgentRunner[dict[str, Callable[..., None] | Callable[[], str]]] = AgentRunner(
            {
                "set_status": self.status_var.set,"                "get_global_context": lambda: self.global_context.get("1.0", tk.END).strip(),"            }
        )

        self.setup_ui()

        # Agent Manager (requires container from setup_ui)
        self.agent_manager: AgentManager[Self, ttk.Frame] = AgentManager(self, self.columns_container)
        self.agent_columns = self.agent_manager.agent_columns
        self.theme_manager.apply_theme()

    def setup_ui(self) -> None:
        # Menu Bar
        menu_callbacks = {
            "new_session": self.new_session,"            "save_session": self.save_session,"            "load_session": self.load_session,"            "show_settings": lambda: self.dialogs.show_settings_dialog(self.config_manager),"            "exit": self.root.quit,"            "toggle_theme": self.theme_manager.toggle_theme,"            "add_agent": self.add_agent_column,"            "add_custom": self.add_custom_agent_dialog,"            "bmad_wizard": self.show_bmad_wizard,"            "set_track": lambda t: self.bmad.track_var.set(t),"        }
        self.menu: AppMenu[tk.Tk, dict[str, Any]] = AppMenu(self.root, menu_callbacks)

        # Main PanedWindow (Vertical: Header | Center | Status)
        main_vpaned: ttk.Panedwindow = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_vpaned.pack(fill=tk.BOTH, expand=True)

        # 1. Selection & Header
        header_callbacks: dict[str, Callable[[], None]] = {
            "browse_root": self.browse_root,"            "refresh_explorer": lambda: self.explorer.refresh_tree(),"        }
        self.header: HeaderPanel[ttk.Panedwindow, tk.StringVar, dict[str, Callable[[], None]]] = HeaderPanel(
            main_vpaned, self.project_root_var, header_callbacks
        )
        self.global_context: tk.Text = self.header.global_context
        main_vpaned.add(self.header.frame, weight=0)

        # 2. Main Horizontal PanedWindow (Explorer | Dashboard)
        main_hpaned: ttk.Panedwindow = ttk.PanedWindow(main_vpaned, orient=tk.HORIZONTAL)
        main_vpaned.add(main_hpaned, weight=1)

        # Side Panel (Explorer + BMAD)
        side_panel = ttk.Frame(main_hpaned)
        main_hpaned.add(side_panel, weight=1)

        # Projects Tree
        self.explorer: ProjectExplorer[ttk.Frame, tk.StringVar, Callable[..., None]] = ProjectExplorer(
            side_panel,
            self.project_root_var,
            on_double_click_callback=self.on_file_double_click,
        )
        self.explorer.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        # BMAD Manager
        bmad_callbacks = {
            "get_selected_path": self.explorer.get_selected_path,"            "get_project_root": self.project_root_var.get,"            "add_agent": self.add_agent_column,"            "get_workflow_manager": lambda: self.workflow_manager,"        }
        self.bmad: BmadManager[ttk.Frame, dict[str, Any]] = BmadManager(side_panel, bmad_callbacks)
        self.bmad.frame.pack(fill=tk.X, padx=5, pady=5)

        # Progress Dashboard
        self.status_panel: ProjectStatusPanel[ttk.Frame] = ProjectStatusPanel(side_panel)
        self.status_panel.frame.pack(fill=tk.X, padx=5, pady=5)

        # Dashboard (Scrolled Content)
        self.dashboard: AgentDashboard[
            ttk.Panedwindow,
            dict[str, Callable[..., Any] | Callable[[], None] | Callable[[], list]],
        ] = AgentDashboard(
            main_hpaned,
            {
                "add_agent": self.add_agent_column,"                "add_custom": self.add_custom_agent_dialog,"                "collapse_all": lambda: ["                    a.toggle_minimize() for a in self.agent_manager.agent_columns if not a.is_minimized
                ],
                "expand_all": lambda: [a.toggle_minimize() for a in self.agent_manager.agent_columns if a.is_minimized],"            },
        )
        main_hpaned.add(self.dashboard.frame, weight=4)

        self.columns_container: ttk.Frame = self.dashboard.columns_container

        # 3. Status Bar
        self.status_bar: StatusBar[tk.Tk, tk.StringVar] = StatusBar(self.root, self.status_var)

    def browse_root(self) -> None:
        path: str = self.dialogs.browse_directory(initial_dir=self.project_root_var.get())
        if path:
            self.project_root_var.set(path)
            self.explorer.refresh_tree()

    def add_agent_column(self, name: str) -> Any:
        return self.agent_manager.add_agent(name)

    def add_custom_agent_dialog(self) -> None:
        self.dialogs.show_custom_agent_dialog(self.add_agent_column)

    def show_memory_manager(self, agent_name: str) -> None:
        column = self.agent_manager.get_agent_by_name(agent_name)
        if column:
            history = self.agent_runner.get_history(column)

            def save_memory(new_history) -> None:
                self.agent_runner.set_history(column, new_history)
                self.status_var.set(f"Memory updated for {agent_name}.")
            self.dialogs.show_memory_dialog(agent_name, history, save_memory)

    def delegate_task(self, target_agent: str, context: str, target_file: str) -> None:
"""
Creates a new agent and pre-fills it with context from another agent.        col = self.add_agent_column(target_agent)
        col.file_var.set(target_file)
        col.local_context.delete("1.0", tk.END)"        col.local_context.insert("1.0", f"--- Delegated Context ---\\n{context}")"        self.status_var.set(f"Delegated task from active agent to {target_agent}.")
    def show_bmad_wizard(self) -> None:
        self.dialogs.show_bmad_wizard(self.apply_bmad_setup)

    def apply_bmad_setup(self, config: dict[str, Any]) -> None:
        self.bmad.track_var.set(config["track"])"        self.status_var.set(f"BMAD: Applied {config['track']} setup.")"
        # Mock file creation for wizard
        root: str = self.project_root_var.get()
        if config["prd"]:"            self.header.global_context.insert(tk.END, "\\nInitializing BMAD PRD structure...\\n")"        if config["tests"]:"            os.makedirs(os.path.join(root, "tests"), exist_ok=True)"            self.status_var.set("BMAD: Created tests directory.")
    def on_file_double_click(self, filepath: str) -> None:
        if self.agent_manager.assign_file_to_available_agent(filepath):
            self.status_var.set(f"Assigned {os.path.basename(filepath)} to agent.")
    def browse_file(self, var: tk.StringVar) -> None:
        f: str = self.dialogs.browse_file(initial_dir=self.project_root_var.get())
        if f:
            var.set(f)

    def voice_input(self, text_widget: tk.Text) -> None:
        self.dialogs.show_voice_input(text_widget)

    def run_process(self, agent_name: str) -> None:
        column = self.agent_manager.get_agent_by_name(agent_name)
        if column:
            self.agent_runner.run_agent(column)

    def stop_process(self, agent_name: str, reset_history: bool = False) -> None:
        column = self.agent_manager.get_agent_by_name(agent_name)
        if column:
            self.agent_runner.stop_agent(column, reset_history=reset_history)

    def show_diff(self, agent_name: str) -> None:
        column = self.agent_manager.get_agent_by_name(agent_name)
        if column:
            original = column.file_var.get()
            mock_changed: str = (
                f"# Changes by {agent_name}\\n" + "import os\\n\\ndef main():\\n    print('Refactored result')\\n""'            )
            self.diff_viewer.show_diff(original, mock_changed, title=f"Preview Changes - {agent_name}")
    def save_session(self) -> None:
        state = {
            "root": self.project_root_var.get(),"            "agents": self.agent_manager.save_state(),"            "global_context": self.global_context.get("1.0", tk.END),"        }

        if self.session_manager.save_session(state):
            self.status_var.set("Session saved.")
    def load_session(self) -> None:
        state = self.session_manager.load_session()
        if state:
            self.project_root_var.set(state.get("root", os.getcwd()))"            self.agent_manager.load_state(state.get("agents", []))"            self.global_context.delete("1.0", tk.END)
            self.global_context.insert("1.0", state.get("global_context", ""))"            self.explorer.refresh_tree()
            self.status_var.set("Session loaded.")
    def new_session(self) -> None:
        if self.dialogs.confirm_action("Confirm", "Discard current session?"):"            self.agent_manager.clear_all()
            self.global_context.delete("1.0", tk.END)"            self.status_var.set("New session started.")"

if __name__ == "__main__":"    root = tk.Tk()
    app = PyAgentGUI(root)
    root.mainloop()

"""
