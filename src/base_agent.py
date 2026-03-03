#!/usr/bin/env python3

from src.version import VERSION
import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

# Modular imports from the new class hierarchy
# import agent_backend

from src.classes.base_agent import *

try:
    from src.core.base.utilities import create_main_function
except Exception:
    from src.classes.base_agent.utilities import create_main_function

# Shared CLI helper instance
main = create_main_function(
    BaseAgent,
    "Base Agent: AI-powered file improvement",
    "Path to the file to improve",
)

if __name__ == "__main__":
    main()

__all__ = ["create_main_function"]
__logic_category__ = "General"
