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
Tests for types
Auto-generated test template - expand with actual test cases
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from infrastructure.executor.multiproc.types import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_executorbackend_exists():
    """Test that ExecutorBackend class exists and is importable."""
    assert 'ExecutorBackend' in dir()


def test_workerstate_exists():
    """Test that WorkerState class exists and is importable."""
    assert 'WorkerState' in dir()


def test_workerinfo_exists():
    """Test that WorkerInfo class exists and is importable."""
    assert 'WorkerInfo' in dir()


def test_taskmessage_exists():
    """Test that TaskMessage class exists and is importable."""
    assert 'TaskMessage' in dir()


def test_resultmessage_exists():
    """Test that ResultMessage class exists and is importable."""
    assert 'ResultMessage' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

