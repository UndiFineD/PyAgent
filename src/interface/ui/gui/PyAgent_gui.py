#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""
GUI Agent: Provides a graphical user interface for PyAgent.
"""

import sys
import tkinter as tk
from pathlib import Path

# Ensure project root is in path for modular imports
# Path(__file__) is src/interface/ui/gui/PyAgent_gui.py
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.interface.ui.gui.MainApp import PyAgentGUI

def main() -> None:
    root = tk.Tk()
    app = PyAgentGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
