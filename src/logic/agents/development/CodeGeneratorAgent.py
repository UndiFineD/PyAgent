#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""Agent specializing in code generation, refactoring, and style enforcement."""

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.logic.coder import *
from src.logic.agents.development.CoderAgent import CoderAgent
from src.core.base.entrypoint import create_main_function

# Create main function using the helper
main = create_main_function(
    CoderAgent,
    'Coder Agent: Updates code files',
    'Path to the code file'
)

if __name__ == '__main__':
    main()
