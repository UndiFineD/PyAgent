#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.base_agent import create_main_function
from src.classes.changes import *

# Create main function using the helper
main = create_main_function(
    ChangesAgent,
    'Changes Agent: Updates code file changelogs',
    'Path to the changes file (e.g., file.changes.md)'
)

if __name__ == '__main__':
    main()
