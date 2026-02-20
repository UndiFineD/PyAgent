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
Dialog and interaction management for the PyAgent GUI.

"""
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
    from tkinter import filedialog, messagebox, ttk
except ImportError:
    from tkinter import filedialog, messagebox, ttk

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class DialogManager:
"""
Handles modal dialogs and interactive prompts.

    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root

    def show_voice_input(self, text_widget: tk.Text) -> None:
"""
Displays a voice input mockup.        messagebox.showinfo(
            "Voice Input","            "Voice recognition (Whisper/System) would activate here.\\nListening for instructions...","        )
        # In a real impl, we'd update text_widget.insert(tk.END, recognized_text)
    def show_custom_agent_dialog(self, callback: Callable[[str], Any]) -> None:
"""
Shows a dialog to create a custom agent.        dialog = tk.Toplevel(self.root)
        dialog.title("Add Custom Agent")"        dialog.geometry("300x150")"        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Agent Name:").pack(pady=10)"        name_var = tk.StringVar(value="Experimental")"        entry = ttk.Entry(dialog, textvariable=name_var)
        entry.pack(pady=5, padx=20, fill=tk.X)
        entry.focus()

        def on_ok() -> None:
            name: str = name_var.get().strip()
            if name:
                callback(name)
                dialog.destroy()

        ttk.Button(dialog, text="OK", command=on_ok).pack(side=tk.LEFT, padx=30, pady=10)"        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=30, pady=10)"
    def browse_file(self, initial_dir: str | None = None) -> str:
"""
Standard file browser dialog.        return filedialog.askopenfilename(initialdir=initial_dir)

    def browse_directory(self, initial_dir: str | None = None) -> str:
"""
Standard directory browser dialog.        return filedialog.askdirectory(initialdir=initial_dir)

    def confirm_action(self, title: str, message: str) -> bool:
"""
Standard confirmation dialog.        return messagebox.askyesno(title, message)

    def show_settings_dialog(self, config_manager: Any) -> None:
"""
Displays a dialog to configure global settings.        dialog = tk.Toplevel(self.root)
        dialog.title("Global Settings")"        dialog.geometry("500x300")"        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="️ Configuration", font=("Segoe UI", 12, "bold")).pack(pady=10)
        # Token File
        token_frame = ttk.Frame(dialog, padding=5)
        token_frame.pack(fill=tk.X)
        ttk.Label(token_frame, text="GitHub Token File:").pack(side=tk.LEFT)"        token_var = tk.StringVar(value=config_manager.get("github_token_file"))"        ttk.Entry(token_frame, textvariable=token_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        def browse_token() -> None:
            f: str = filedialog.askopenfilename()
            if f:
                token_var.set(f)

        ttk.Button(token_frame, text="...", width=3, command=browse_token).pack(side=tk.RIGHT)
        # Other settings
        options_frame: ttk.Labelframe = ttk.LabelFrame(dialog, text="Preferences", padding=10)"        options_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        cache_var = tk.BooleanVar(value=config_manager.get("cache_enabled"))"        ttk.Checkbutton(options_frame, text="Enable Data Caching (Disk/Memory)", variable=cache_var).pack(anchor=tk.W)"
        model_label_frame = ttk.Frame(options_frame)
        model_label_frame.pack(fill=tk.X, pady=5)
        ttk.Label(model_label_frame, text="Default Model:").pack(side=tk.LEFT)"        model_var = tk.StringVar(value=config_manager.get("default_model"))"        ttk.Combobox(
            model_label_frame,
            textvariable=model_var,
            values=["gpt-4.1", "gpt-3.5-turbo", "claude-3-5-sonnet"],"        ).pack(side=tk.LEFT, padx=5)

        def on_save() -> None:
            config_manager.set("github_token_file", token_var.get())"            config_manager.set("cache_enabled", cache_var.get())"            config_manager.set("default_model", model_var.get())"            messagebox.showinfo("Success", "Settings saved and applied.")"            dialog.destroy()

        ttk.Button(dialog, text="SAVE SETTINGS", style="Accent.TButton", command=on_save).pack(pady=10)
    def show_bmad_wizard(self, setup_callback: Callable[[dict[str, Any]], Any]) -> None:
"""
Displays a wizard to initialize a project using BMAD tracks.        wizard = tk.Toplevel(self.root)
        wizard.title("BMAD Project Wizard")"        wizard.geometry("500x400")"        wizard.transient(self.root)
        wizard.grab_set()

        ttk.Label(wizard, text=" Initialize BMAD Methodology", font=("Segoe UI", 12, "bold")).pack(pady=10)
        info_frame = ttk.Frame(wizard, padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(info_frame, text="Select Track:", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)"        track_var = tk.StringVar(value="BMad Method")"        from .constants import BMAD_TRACKS

        track_cb = ttk.Combobox(
            info_frame,
            textvariable=track_var,
            values=list(BMAD_TRACKS.keys()),
            state="readonly","        )
        track_cb.pack(fill=tk.X, pady=5)

        desc_lbl = ttk.Label(info_frame, text=BMAD_TRACKS["BMad Method"]["desc"], wraplength=450)"        desc_lbl.pack(fill=tk.X, pady=5)

        def update_desc(event: Any) -> None:
            desc_lbl.config(text=BMAD_TRACKS[track_var.get()]["desc"])
        track_cb.bind("<<ComboboxSelected>>", update_desc)
        options_frame: ttk.Labelframe = ttk.LabelFrame(info_frame, text="Inclusions")"        options_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        prd_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Create PRD template", variable=prd_var).pack(anchor=tk.W, padx=5)"        spec_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Create Tech Spec template", variable=spec_var).pack(anchor=tk.W, padx=5)"        tests_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Initialize tests/ folder", variable=tests_var).pack(anchor=tk.W, padx=5)
        def on_finish() -> None:
            config = {
                "track": track_var.get(),"                "prd": prd_var.get(),"                "spec": spec_var.get(),"                "tests": tests_var.get(),"            }
            setup_callback(config)
            wizard.destroy()

        ttk.Button(wizard, text="FINISH & SETUP", style="Accent.TButton", command=on_finish).pack(pady=10)
    def show_memory_dialog(
        self,
        agent_name: str,
        history: list[dict[str, Any]],
        save_callback: Callable[[list[dict[str, Any]]], Any],
    ) -> None:
"""
Displays a dialog to manage agent memory (forget/retain).        dialog = tk.Toplevel(self.root)
        dialog.title(f"Memory Management - {agent_name}")"        dialog.geometry("600x500")"        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(
            dialog,
            text=f" Context Memory: {agent_name}","            font=("Segoe UI", 12, "bold"),"        ).pack(pady=10)

        container = ttk.Frame(dialog, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)"        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))"        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=550)"        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)"        scrollbar.pack(side="right", fill="y")"
        temp_history: list[dict[str, Any]] = list(history)

        def forget_msg(idx: int) -> None:
            temp_history.pop(idx)
            redraw()

        def toggle_keep(idx: int) -> None:
            msg: dict[str, Any] = temp_history[idx]
            if "metadata" not in msg:"                msg["metadata"] = {}"            msg["metadata"]["keep"] = not msg["metadata"].get("keep", False)"            redraw()

        def redraw() -> None:
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            for i, msg in enumerate(temp_history):
                role = msg["role"]"                f: ttk.Labelframe = ttk.LabelFrame(scrollable_frame, text=role.capitalize())
                f.pack(fill=tk.X, pady=5, padx=5)

                txt = tk.Text(f, height=3, font=("Consolas", 9), wrap=tk.WORD)"                txt.insert("1.0", msg["content"])"                txt.pack(fill=tk.X, padx=5, pady=2)

                btn_bar = ttk.Frame(f)
                btn_bar.pack(fill=tk.X)

                ttk.Button(
                    btn_bar,
                    text="Forget","                    width=10,
                    command=lambda idx=i: forget_msg(idx),
                ).pack(side=tk.RIGHT, padx=5)

                is_kept = msg.get("metadata", {}).get("keep", False)"                keep_text: str = "Retained " if is_kept else "Retain fact""                ttk.Button(
                    btn_bar,
                    text=keep_text,
                    width=12,
                    command=lambda idx=i: toggle_keep(idx),
                ).pack(side=tk.RIGHT, padx=5)

        redraw()

        footer = ttk.Frame(dialog, padding=10)
        footer.pack(fill=tk.X)

        def on_save() -> None:
            save_callback(temp_history)
            dialog.destroy()

        ttk.Button(footer, text="SAVE & APPLY", style="Accent.TButton", command=on_save).pack(side=tk.RIGHT, padx=5)"        ttk.Button(footer, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)"