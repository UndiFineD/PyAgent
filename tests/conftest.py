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

"""Pytest configuration for PyAgent tests."""
import pytest
import tempfile
from pathlib import Path
from src.infrastructure.fleet.AgentRegistry import AgentRegistry

@pytest.fixture
def agent_sandbox():
    """Provides a clean, temporary src/ and data/ environment for agent tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        src_dir = temp_path / "src"
        data_dir = temp_path / "data"
        src_dir.mkdir()
        data_dir.mkdir()
        
        # Initialize basic structure
        (src_dir / "__init__.py").touch()
        
        yield temp_path

@pytest.fixture
def agent_registry():
    """Provides a central AgentRegistry for test use."""
    workspace_root = Path(__file__).parent.parent
    return AgentRegistry.get_agent_map(workspace_root)
