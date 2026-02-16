#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Utils: Common utilities for agent and backend unit tests.
"""

from __future__ import annotations

import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from src.core.base.lifecycle.version import VERSION
from src.infrastructure.services.dev.test_utils import (FileSystemIsolator,
                                                        LogCapturer,
                                                        MockAIBackend,
                                                        ModuleLoader,
                                                        SnapshotManager)

# Ensure project root and src are in path for modular imports
root = Path(__file__).resolve().parents[3]
if str(root) not in sys.path:
    sys.path.append(str(root))
if str(root / "src") not in sys.path:
    sys.path.append(str(root / "src"))

# Modular imports
__version__ = VERSION

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
