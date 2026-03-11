#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""LLM_CONTEXT_START

## Source: src-old/agent_tests.description.md

# Description: `agent_tests.py`

## Module purpose

(No module docstring found)

## Location
- Path: `src\agent_tests.py`

## Public surface
- Classes: (none)
- Functions: (none)

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `sys`, `pathlib`, `src.base_agent`, `src.classes.agent_tests`

## Metadata

- SHA256(source): `a2b9362fca2bd80c`
- Last updated: `2026-01-08 08:25:40`
- File: `src\agent_tests.py`
## Source: src-old/agent_tests.improvements.md

# Improvements: `agent_tests.py`

## Suggested improvements

- Add a concise module docstring describing purpose / usage.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\agent_tests.py`

LLM_CONTEXT_END
"""

"""
Tests Agent: Maintains and updates test suites for the workspace.
"""

import sys
from pathlib import Path

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

from src.base_agent import create_main_function
from src.classes.agent_tests import *

# Create main function using the helper
main = create_main_function(
    TestsAgent,
    "Tests Agent: Updates code file test suites",
    "Path to the test file (e.g., test_file.py)",
)

if __name__ == "__main__":
    main()
