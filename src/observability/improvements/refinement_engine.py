#!/usr/bin/env python3
from __future__ import annotations
# Copyright (c) 2025 PyAgent contributors


































from src.core.base.version import VERSION
__version__ = VERSION

"""
Improvements Agent: Maintains and improves improvement suggestions.
"""

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.core.base.entrypoint import create_main_function
from src.observability.improvements import *

# Create main function using the helper
main = create_main_function(
    ImprovementsAgent,
    'Improvements Agent: Maintains and improves improvement suggestions',
    'Path to the improvements file (e.g., file.improvements.md)'
)

if __name__ == '__main__':
    main()
