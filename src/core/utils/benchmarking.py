#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""
Test Utils: Common utilities for agent and backend unit tests.
"""

from src.core.base.version import VERSION
import sys
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator

# Ensure project root and src are in path for modular imports
root = Path(__file__).resolve().parents[3]
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

# Modular imports
from src.infrastructure.dev.test_utils import *

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
