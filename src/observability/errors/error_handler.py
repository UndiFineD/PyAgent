#!/usr/bin/env python3
from __future__ import annotations
# Copyright (c) 2025 PyAgent contributors


































from src.core.base.version import VERSION
__version__ = VERSION

"""Agent specializing in analyzing, documenting, and suggesting fixes for errors."""

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.core.base.entrypoint import create_main_function
from src.observability.errors import ErrorsAgent, DEFAULT_ERROR_PATTERNS
from src.observability.errors import *

# Create main function using the helper
main = create_main_function(
    ErrorsAgent,
    'Errors Agent: Updates code file error reports',
    'Path to the errors file (e.g., file.errors.md)'
)

if __name__ == '__main__':
    main()
