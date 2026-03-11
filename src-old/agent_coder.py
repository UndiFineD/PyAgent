#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""LLM_CONTEXT_START

## Source: src-old/agent_coder.description.md

# Description: `agent_coder.py`

## Module purpose

Agent specializing in code generation, refactoring, and style enforcement.

## Location
- Path: `src\agent_coder.py`

## Public surface
- Classes: (none)
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `sys`, `pathlib`, `src.base_agent`, `src.classes.coder`

## Metadata

- SHA256(source): `81be42c55f767d56`
- Last updated: `2026-01-08 22:51:33`
- File: `src\agent_coder.py`
## Source: src-old/agent_coder.improvements.md

# Improvements: `agent_coder.py`

## Suggested improvements

- No obvious improvements detected by the lightweight scan

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\agent_coder.py`

LLM_CONTEXT_END
"""

"""Agent specializing in code generation, refactoring, and style enforcement."""

import sys
from pathlib import Path

from src.classes.base_agent import create_main_function
from src.logic.agents.development.coder_agent import CoderAgent

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))


# Create main function using the helper
main = create_main_function(
    CoderAgent, "Coder Agent: Updates code files", "Path to the code file"
)

if __name__ == "__main__":
    main()
