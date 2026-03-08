#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""
LLM_CONTEXT_START

## Source: src-old/agent_gui.description.md

# Description: `agent_gui.py`

## Module purpose

(No module docstring found)

## Location
- Path: `src\agent_gui.py`

## Public surface
- Classes: (none)
- Functions: main

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `sys`, `tkinter`, `pathlib`, `src.classes.gui.MainApp`

## Metadata

- SHA256(source): `aefdda2127d72ec9`
- Last updated: `2026-01-08 08:25:39`
- File: `src\agent_gui.py`
## Source: src-old/agent_gui.improvements.md

# Improvements: `agent_gui.py`

## Suggested improvements

- Add a concise module docstring describing purpose / usage.
- Function `main` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\agent_gui.py`

LLM_CONTEXT_END
"""

"""
GUI Agent: Provides a graphical user interface for PyAgent.
"""

from src.version import VERSION
import sys
import tkinter as tk
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.classes.gui.MainApp import PyAgentGUI


def main() -> None:
    root = tk.Tk()
    app = PyAgentGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
