#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors

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

def main():
    root = tk.Tk()
    app = PyAgentGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
