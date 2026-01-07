#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Main application controller for PyAgent GUI."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

from .ProjectExplorer import ProjectExplorer
from .AgentColumn import AgentColumn
from .SessionManager import SessionManager
from .ThemeManager import ThemeManager
from .DiffViewer import DiffViewer
from .AgentRunner import AgentRunner
from .AppMenu import AppMenu
from .HeaderPanel import HeaderPanel
from .AgentDashboard import AgentDashboard
from .StatusBar import StatusBar
from .BmadManager import BmadManager
from .AgentManager import AgentManager
from .DialogManager import DialogManager
from .WorkflowManager import WorkflowManager
from .ConfigurationManager import ConfigurationManager
from .ProjectStatusPanel import ProjectStatusPanel

class PyAgentGUI:
    """The main application window and controller."""
    def __init__(self, root):
        self.root = root
        self.root.title("PyAgent Control Center - BMAD Enabled")
        self.root.geometry("1400x900")
        
        # UI State (Init before managers)
        self.project_root_var = tk.StringVar(value=os.getcwd())
        self.status_var = tk.StringVar(value="Ready")
        
        # Managers
        self.config_manager = ConfigurationManager()
        self.dialogs = DialogManager(self.root)
        self.workflow_manager = WorkflowManager({
            "set_status": self.status_var.set,
            "add_agent": lambda name: self.agent_manager.add_column(name)
        })
        
        # Backend components
        self.session_manager = SessionManager("gui_session.json")
        self.theme_manager = ThemeManager(self.root)
        self.diff_viewer = DiffViewer(self.root)
        self.agent_runner = AgentRunner({
            "set_status": self.status_var.set,
            "get_global_context": lambda: self.global_context.get("1.0", tk.END).strip()
        })
        
        self.setup_ui()
        
        # Agent Manager (requires container from setup_ui)
        self.agent_manager = AgentManager(self, self.columns_container)
        self.agent_columns = self.agent_manager.agent_columns
        self.theme_manager.apply_theme()

    def setup_ui(self):
        # Menu Bar
        menu_callbacks = {
            "new_session": self.new_session,
            "save_session": self.save_session,
            "load_session": self.load_session,
            "show_settings": lambda: self.dialogs.show_settings_dialog(self.config_manager),
            "exit": self.root.quit,
            "toggle_theme": self.theme_manager.toggle_theme,
            "add_agent": self.add_agent_column,
            "add_custom": self.add_custom_agent_dialog,
            "bmad_wizard": self.show_bmad_wizard,
            "set_track": lambda t: self.bmad.track_var.set(t)
        }
        self.menu = AppMenu(self.root, menu_callbacks)

        # Main PanedWindow (Vertical: Header | Center | Status)
        main_vpaned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_vpaned.pack(fill=tk.BOTH, expand=True)

        # 1. Selection & Header
        header_callbacks = {
            "browse_root": self.browse_root,
            "refresh_explorer": lambda: self.explorer.refresh_tree()
        }
        self.header = HeaderPanel(main_vpaned, self.project_root_var, header_callbacks)
        self.global_context = self.header.global_context
        main_vpaned.add(self.header.frame, weight=0)

        # 2. Main Horizontal PanedWindow (Explorer | Dashboard)
        main_hpaned = ttk.PanedWindow(main_vpaned, orient=tk.HORIZONTAL)
        main_vpaned.add(main_hpaned, weight=1)

        # Side Panel (Explorer + BMAD)
        side_panel = ttk.Frame(main_hpaned)
        main_hpaned.add(side_panel, weight=1)

        # Projects Tree
        self.explorer = ProjectExplorer(
            side_panel, 
            self.project_root_var,
            on_double_click_callback=self.on_file_double_click
        )
        self.explorer.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        # BMAD Manager
        bmad_callbacks = {
            "get_selected_path": self.explorer.get_selected_path,
            "get_project_root": self.project_root_var.get,
            "add_agent": self.add_agent_column,
            "get_workflow_manager": lambda: self.workflow_manager
        }
        self.bmad = BmadManager(side_panel, bmad_callbacks)
        self.bmad.frame.pack(fill=tk.X, padx=5, pady=5)

        # Progress Dashboard
        self.status_panel = ProjectStatusPanel(side_panel)
        self.status_panel.frame.pack(fill=tk.X, padx=5, pady=5)

        # Dashboard (Scrolled Content)
        self.dashboard = AgentDashboard(main_hpaned, {
            "add_agent": self.add_agent_column,
            "add_custom": self.add_custom_agent_dialog,
            "collapse_all": lambda: [a.toggle_minimize() for a in self.agent_manager.agent_columns if not a.is_minimized],
            "expand_all": lambda: [a.toggle_minimize() for a in self.agent_manager.agent_columns if a.is_minimized]
        })
        main_hpaned.add(self.dashboard.frame, weight=4)

        self.columns_container = self.dashboard.columns_container

        # 3. Status Bar
        self.status_bar = StatusBar(self.root, self.status_var)

    def browse_root(self):
        path = self.dialogs.browse_directory(initial_dir=self.project_root_var.get())
        if path:
            self.project_root_var.set(path)
            self.explorer.refresh_tree()

    def add_agent_column(self, name):
        return self.agent_manager.add_agent(name)

    def add_custom_agent_dialog(self):
        self.dialogs.show_custom_agent_dialog(self.add_agent_column)

    def show_memory_manager(self, agent_name):
        column = self.agent_manager.get_agent_by_name(agent_name)
        if column:
            history = self.agent_runner.get_history(column)
            
            def save_memory(new_history):
                self.agent_runner.set_history(column, new_history)
                self.status_var.set(f"Memory updated for {agent_name}.")

            self.dialogs.show_memory_dialog(agent_name, history, save_memory)

    def delegate_task(self, target_agent, context, target_file):
        """Creates a new agent and pre-fills it with context from another agent."""
        col = self.add_agent_column(target_agent)
        col.file_var.set(target_file)
        col.local_context.delete("1.0", tk.END)
        col.local_context.insert("1.0", f"--- Delegated Context ---\n{context}")
        self.status_var.set(f"Delegated task from active agent to {target_agent}.")

    def show_bmad_wizard(self):
        self.dialogs.show_bmad_wizard(self.apply_bmad_setup)

    def apply_bmad_setup(self, config):
        self.bmad.track_var.set(config["track"])
        self.status_var.set(f"BMAD: Applied {config['track']} setup.")
        
        # Mock file creation for wizard
        root = self.project_root_var.get()
        if config["prd"]:
            self.header.global_context.insert(tk.END, "\nInitializing BMAD PRD structure...\n")
        if config["tests"]:
            os.makedirs(os.path.join(root, "tests"), exist_ok=True)
            self.status_var.set("BMAD: Created tests directory.")

    def on_file_double_click(self, filepath):
        if self.agent_manager.assign_file_to_available_agent(filepath):
            self.status_var.set(f"Assigned {os.path.basename(filepath)} to agent.")

    def browse_file(self, var):
        f = self.dialogs.browse_file(initial_dir=self.project_root_var.get())
        if f:
            var.set(f)

    def voice_input(self, text_widget):
        self.dialogs.show_voice_input(text_widget)

    def run_process(self, agent_name):
        column = self.agent_manager.get_agent_by_name(agent_name)
        if column:
            self.agent_runner.run_agent(column)

    def stop_process(self, agent_name, reset_history=False):
        column = self.agent_manager.get_agent_by_name(agent_name)
        if column:
            self.agent_runner.stop_agent(column, reset_history=reset_history)

    def show_diff(self, agent_name):
        column = self.agent_manager.get_agent_by_name(agent_name)
        if column:
            original = column.file_var.get()
            mock_changed = f"# Changes by {agent_name}\n" + "import os\n\ndef main():\n    print('Refactored result')\n"
            self.diff_viewer.show_diff(original, mock_changed, title=f"Preview Changes - {agent_name}")

    def save_session(self):
        state = {
            "root": self.project_root_var.get(),
            "agents": self.agent_manager.save_state(),
            "global_context": self.global_context.get("1.0", tk.END)
        }
        if self.session_manager.save_session(state):
            self.status_var.set("Session saved.")

    def load_session(self):
        state = self.session_manager.load_session()
        if state:
            self.project_root_var.set(state.get("root", os.getcwd()))
            self.agent_manager.load_state(state.get("agents", []))
            self.global_context.delete("1.0", tk.END)
            self.global_context.insert("1.0", state.get("global_context", ""))
            self.explorer.refresh_tree()
            self.status_var.set("Session loaded.")

    def new_session(self):
        if self.dialogs.confirm_action("Confirm", "Discard current session?"):
            self.agent_manager.clear_all()
            self.global_context.delete("1.0", tk.END)
            self.status_var.set("New session started.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyAgentGUI(root)
    root.mainloop()

