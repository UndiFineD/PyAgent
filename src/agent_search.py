#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.classes.search.SearchAgent import SearchAgent
from src.base_agent import create_main_function

if __name__ == "__main__":
    main = create_main_function(SearchAgent, "Research Agent", "Topic/File to research")
    main()
