#!/usr/bin/env python3
"""
Fix slash command imports by converting absolute imports to relative ones.
"""
import os

DIR_PATH = r"c:\DEV\PyAgent\src\interface\slash_commands\commands"
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
