#!/usr/bin/env python3
"""
Fix slash command imports by converting absolute imports to relative ones.
"""
import os
from pathlib import Path

# Robustly find the repository root
current_path = Path(__file__).resolve()
project_root = current_path
while project_root.name != 'src' and project_root.parent != project_root:
    project_root = project_root.parent
if project_root.name == 'src':
    project_root = project_root.parent

DIR_PATH = project_root / "src/interface/slash_commands/commands"

if not DIR_PATH.exists():
    print(f"Directory not found: {DIR_PATH}")
    exit(1)

for filename in os.listdir(DIR_PATH):
    if filename.endswith(".py") and filename != "__init__.py":
        filepath = os.path.join(DIR_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace absolute imports with relative ones
        new_content = content.replace("from src.interface.slash_commands.core import", "from ..core import")
        new_content = new_content.replace("from src.interface.slash_commands.registry import", "from ..registry import")
        new_content = new_content.replace("from src.interface.slash_commands.loader import", "from ..loader import")

        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {filename}")
