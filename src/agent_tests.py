#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""
Tests Agent: Maintains and updates test suites for the workspace.
"""

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.base_agent import create_main_function
from src.classes.agent_tests import *

# Create main function using the helper
main = create_main_function(
    TestsAgent,
    'Tests Agent: Updates code file test suites',
    'Path to the test file (e.g., test_file.py)'
)

if __name__ == '__main__':
    main()
