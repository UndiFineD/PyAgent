#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""LLM_CONTEXT_START

## Source: src-old/agent_test_utils.description.md

# Description: `agent_test_utils.py`

## Module purpose

(No module docstring found)

## Location
- Path: `src\agent_test_utils.py`

## Public surface
- Classes: (none)
- Functions: agent_dir_on_path, agent_sys_path

## Behavior summary
- Pure module (no obvious CLI / side effects).

## Key dependencies
- Top imports: `sys`, `pathlib`, `contextlib`, `typing`, `src.classes.test_utils`

## Metadata

- SHA256(source): `8326f0ed88346597`
- Last updated: `2026-01-08 08:25:40`
- File: `src\agent_test_utils.py`
## Source: src-old/agent_test_utils.improvements.md

# Improvements: `agent_test_utils.py`

## Suggested improvements

- Add a concise module docstring describing purpose / usage.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\agent_test_utils.py`

LLM_CONTEXT_END
"""

"""
Test Utils: Common utilities for agent and backend unit tests.
"""

import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

# Ensure project root and src are in path for modular imports
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

# Modular imports
from src.classes.test_utils import *

# Shared loader for constants
_loader = ModuleLoader()
AGENT_DIR = _loader.agent_dir

# Re-expose methods as expected by legacy tests
load_module_from_path = _loader.load_module_from_path


@contextmanager
def agent_dir_on_path() -> Iterator[None]:
    with _loader.agent_dir_on_path():
        yield


@contextmanager
def agent_sys_path() -> Iterator[None]:
    with _loader.agent_sys_path():
        yield


# Aliases for legacy compatibility
MockBackend = MockAIBackend
FileSystemIsolation = FileSystemIsolator
SnapshotTester = SnapshotManager
LoggingCapture = LogCapturer
