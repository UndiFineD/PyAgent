#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Project Explorer component for the PyAgent GUI."""

import os
import tkinter as tk
from tkinter import ttk
import logging

class ProjectExplorer:
    """A tree-view based file explorer for the PyAgent workspace."""
    def __init__(self, parent, project_root_var, on_double_click_callback) -> None:
        self.parent = parent
        self.project_root_var = project_root_var
        self.on_double_click_callback = on_double_click_callback
        
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        
    def setup_ui(self):
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(header_frame, text="Project Explorer").pack(side=tk.LEFT)
        
        # Search Bar
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill=tk.X, padx=5, pady=2)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_tree())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        ttk.Label(search_frame, text="🔍").pack(side=tk.RIGHT)
        
        self.tree = ttk.Treeview(self.frame, selectmode="browse")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tree_scroll = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<<TreeviewOpen>>", self.on_tree_open)
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_tree).pack(fill=tk.X)
        
        self.refresh_tree()

    def show_context_menu(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            menu = tk.Menu(self.parent, tearoff=0)
            menu.add_command(label="Send to Agent", command=self.send_to_agent)
            menu.add_command(label="Copy Path", command=self.copy_path)
            menu.tk_popup(event.x_root, event.y_root)

    def send_to_agent(self):
        selected = self.tree.selection()
        if selected:
            abspath = self.tree.item(selected[0], "values")[0]
            if not os.path.isdir(abspath):
                self.on_double_click_callback(abspath)

    def copy_path(self):
        selected = self.tree.selection()
        if selected:
            abspath = self.tree.item(selected[0], "values")[0]
            self.parent.clipboard_clear()
            self.parent.clipboard_append(abspath)

    def refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        root_path = self.project_root_var.get()
        if os.path.exists(root_path):
            self.populate_tree("", root_path)

    def populate_tree(self, parent, path):
        try:
            items = sorted(os.listdir(path), key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
            for item in items:
                abspath = os.path.join(path, item)
                is_dir = os.path.isdir(abspath)
                
                if item in {'__pycache__', 'node_modules', '.git', '.venv', '.pytest_cache', '.agent_cache'}:
                    continue
                    
                node = self.tree.insert(parent, "end", text=item, values=[abspath], open=False)
                if is_dir:
                    self.tree.insert(node, "end")
        except Exception as e:
            logging.error(f"Error populating tree: {e}")

    def on_tree_open(self, event):
        item_id = self.tree.focus()
        abspath = self.tree.item(item_id, "values")[0]
        if os.path.isdir(abspath):
            for child in self.tree.get_children(item_id):
                self.tree.delete(child)
            self.populate_tree(item_id, abspath)

    def on_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item_id = selected[0]
        abspath = self.tree.item(item_id, "values")[0]
        self.on_double_click_callback(abspath)

    def get_selected_path(self):
        """Returns the absolute path of the currently selected item in the tree."""
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0], "values")[0]

    def filter_tree(self):
        query = self.search_var.get().lower()
        if not query:
            self.refresh_tree()
            return
            
        if len(query) < 3:
            return
            
        root_path = self.project_root_var.get()
        if not os.path.exists(root_path):
            return
            
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        count = 0
        for root, dirs, files in os.walk(root_path):
            dirs[:] = [d for d in dirs if d not in {'__pycache__', 'node_modules', '.git', '.venv', '.pytest_cache', '.agent_cache'}]
            for f in files:
                if query in f.lower():
                    abspath = os.path.join(root, f)
                    relpath = os.path.relpath(abspath, root_path)
                    self.tree.insert("", "end", text=relpath, values=[abspath])
                    count += 1
                if count > 100:
                    break
            if count > 100:
                break
