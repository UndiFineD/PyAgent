#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""
LLM_CONTEXT_START

## Source: src-old/agent_improvements.description.md

# Description: `agent_improvements.py`

## Module purpose

(No module docstring found)

## Location
- Path: `src\agent_improvements.py`

## Public surface
- Classes: (none)
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `sys`, `pathlib`, `src.base_agent`, `src.classes.improvements`

## Metadata

- SHA256(source): `5fd72dd1a089f72f`
- Last updated: `2026-01-08 08:25:39`
- File: `src\agent_improvements.py`
## Source: src-old/agent_improvements.improvements.md

# Improvements: `agent_improvements.py`

## Suggested improvements

- Add a concise module docstring describing purpose / usage.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\agent_improvements.py`

LLM_CONTEXT_END
"""

"""
Improvements Agent: Maintains and improves improvement suggestions.
"""

from src.version import VERSION
import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.base_agent import create_main_function
from src.classes.improvements import *

# Create main function using the helper
main = create_main_function(
    ImprovementsAgent,
    "Improvements Agent: Maintains and improves improvement suggestions",
    "Path to the improvements file (e.g., file.improvements.md)",
)

if __name__ == "__main__":
    main()
