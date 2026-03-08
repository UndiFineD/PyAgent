#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""
LLM_CONTEXT_START

## Source: src-old/agent_changes.description.md

# Description: `agent_changes.py`

## Module purpose

Agent specializing in tracking, summarizing, and documenting code changes.

## Location
- Path: `src\agent_changes.py`

## Public surface
- Classes: (none)
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `sys`, `pathlib`, `src.base_agent`, `src.classes.changes`

## Metadata

- SHA256(source): `df17572a05d1c855`
- Last updated: `2026-01-08 22:51:32`
- File: `src\agent_changes.py`
## Source: src-old/agent_changes.improvements.md

# Improvements: `agent_changes.py`

## Suggested improvements

- No obvious improvements detected by the lightweight scan

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\agent_changes.py`

LLM_CONTEXT_END
"""

"""Agent specializing in tracking, summarizing, and documenting code changes."""

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
from src.classes.changes import *

# Create main function using the helper
main = create_main_function(
    ChangesAgent,
    "Changes Agent: Updates code file changelogs",
    "Path to the changes file (e.g., file.changes.md)",
)

if __name__ == "__main__":
    main()
