#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

from src.core.base.version import VERSION
"""
Search Agent: Perform deep research and search operations across the workspace.
"""

__version__ = VERSION

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

    from src.logic.agents.intelligence.SearchAgent import SearchAgent

if __name__ == "__main__":
    main = create_main_function(SearchAgent, "Research Agent", "Topic/File to research")
    main()
