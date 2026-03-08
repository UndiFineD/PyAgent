#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""
LLM_CONTEXT_START

## Source: src-old/agent_search.description.md

# Description: `agent_search.py`

## Module purpose

(No module docstring found)

## Location
- Path: `src\agent_search.py`

## Public surface
- Classes: (none)
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `sys`, `pathlib`, `src.classes.search.SearchAgent`, `src.base_agent`

## Metadata

- SHA256(source): `e1d1fb30828c2daf`
- Last updated: `2026-01-08 08:25:39`
- File: `src\agent_search.py`
## Source: src-old/agent_search.improvements.md

# Improvements: `agent_search.py`

## Suggested improvements

- Add a concise module docstring describing purpose / usage.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\agent_search.py`

LLM_CONTEXT_END
"""

"""
Search Agent: Perform deep research and search operations across the workspace.
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

from src.classes.search.SearchAgent import SearchAgent
from src.base_agent import create_main_function

if __name__ == "__main__":
    main = create_main_function(SearchAgent, "Research Agent", "Topic/File to research")
    main()
