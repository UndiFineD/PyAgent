__logic_category__ = "General"
#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""
Base Agent Module: Core agent functionality and CLI entry points.
"""


from src.core.base.version import VERSION
import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).resolve().parents[2]
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

# Modular imports from the new class hierarchy
import src.infrastructure.backend.execution_engine as agent_backend

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import create_main_function

# Shared CLI helper instance
main = create_main_function(
    BaseAgent,
    "Base Agent: AI-powered file improvement",
    "Path to the file to improve"
)

if __name__ == "__main__":
    main()
