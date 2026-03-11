#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/base_agent.description.md

# Description: `base_agent.py`

## Module purpose

(No module docstring found)

## Location
- Path: `src\base_agent.py`

## Public surface
- Classes: (none)
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `sys`, `pathlib`, `agent_backend`, `src.classes.base_agent`

## Metadata

- SHA256(source): `6b12b82893acd349`
- Last updated: `2026-01-08 08:25:40`
- File: `src\base_agent.py`
## Source: src-old/base_agent.improvements.md

# Improvements: `base_agent.py`

## Suggested improvements

- Add a concise module docstring describing purpose / usage.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\base_agent.py`

LLM_CONTEXT_END
"""

"""Base Agent: Provides core functionality for AI-powered file improvement."""

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
from src.classes.base_agent import BaseAgent

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
