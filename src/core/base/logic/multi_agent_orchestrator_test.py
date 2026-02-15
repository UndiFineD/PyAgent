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
Test for Multi-Agent Orchestrator and Voice Agent Orchestrator
"""

import time
import pytest
import tempfile
from pathlib import Path
from src.core.base.logic.multi_agent_orchestrator import MultiAgentOrchestratorCore
from src.core.base.logic.voice_agent_orchestrator import VoiceAgentOrchestrator


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestMultiAgentOrchestrator:
    """Test the multi-agent orchestrator core."""

    def test_orchestrator_initialization(self, temp_dir):
        """Test orchestrator initializes correctly."""
        orchestrator = MultiAgentOrchestratorCore(base_working_dir=temp_dir)
        assert orchestrator.agent_registry == {}
    # ...existing code...
    pass
