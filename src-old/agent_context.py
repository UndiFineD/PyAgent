#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""LLM_CONTEXT_START

## Source: src-old/agent_context.description.md

# Description: `agent_context.py`

## Module purpose

(No module docstring found)

## Location
- Path: `src\agent_context.py`

## Public surface
- Classes: (none)
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `sys`, `pathlib`, `src.base_agent`, `src.classes.context`

## Metadata

- SHA256(source): `05e2c257c4707a8f`
- Last updated: `2026-01-08 08:25:38`
- File: `src\agent_context.py`
## Source: src-old/agent_context.improvements.md

# Improvements: `agent_context.py`

## Suggested improvements

- Add a concise module docstring describing purpose / usage.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\agent_context.py`

LLM_CONTEXT_END
"""

"""
Context Agent: Maintains and improves context/description files.
"""

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))
from src.classes.base_agent import create_main_function
from src.logic.agents.cognitive.ContextAgent import ContextAgent

# Create main function using the helper
main = create_main_function(
    ContextAgent,
    "Context Agent: Maintains and improves context/description files",
    "Path to the context file (e.g., file.description.md)",
)

if __name__ == "__main__":
    main()
