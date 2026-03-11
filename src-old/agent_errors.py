#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""LLM_CONTEXT_START

## Source: src-old/agent_errors.description.md

# Description: `agent_errors.py`

## Module purpose

Agent specializing in analyzing, documenting, and suggesting fixes for errors.

## Location
- Path: `src\agent_errors.py`

## Public surface
- Classes: (none)
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `sys`, `pathlib`, `src.base_agent`, `src.classes.errors`

## Metadata

- SHA256(source): `736844ce587a88f4`
- Last updated: `2026-01-08 22:51:33`
- File: `src\agent_errors.py`
## Source: src-old/agent_errors.improvements.md

# Improvements: `agent_errors.py`

## Suggested improvements

- No obvious improvements detected by the lightweight scan

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\agent_errors.py`

LLM_CONTEXT_END
"""

"""Agent specializing in analyzing, documenting, and suggesting fixes for errors."""

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.base_agent import create_main_function
from src.classes.errors import *

# Create main function using the helper
main = create_main_function(
    ErrorsAgent,
    "Errors Agent: Updates code file error reports",
    "Path to the errors file (e.g., file.errors.md)",
)

if __name__ == "__main__":
    main()
