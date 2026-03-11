#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""LLM_CONTEXT_START

## Source: src-old/agent_strategies.description.md

# Description: `agent_strategies.py`

## Module purpose

(No module docstring found)

## Location
- Path: `src\agent_strategies.py`

## Public surface
- Classes: (none)
- Functions: (none)

## Behavior summary
- Pure module (no obvious CLI / side effects).

## Key dependencies
- Top imports: `sys`, `pathlib`, `typing`, `src.classes.strategies`

## Metadata

- SHA256(source): `d38bab173f1f6979`
- Last updated: `2026-01-08 08:25:40`
- File: `src\agent_strategies.py`
## Source: src-old/agent_strategies.improvements.md

# Improvements: `agent_strategies.py`

## Suggested improvements

- Add a concise module docstring describing purpose / usage.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\agent_strategies.py`

LLM_CONTEXT_END
"""

"""
Strategies Module: Unified interface for agent decision-making strategies.
"""

import sys
from pathlib import Path

# from typing import Any, Dict, List, Optional, Callable


# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

# Modular imports
from src.classes.strategies import *

# Type alias for functional compatibility
BackendFunction = Callable[[str, Optional[str], Optional[List[Dict[str, str]]]], str]
