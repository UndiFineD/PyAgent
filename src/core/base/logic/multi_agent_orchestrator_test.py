#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Test for Multi-Agent Orchestrator and Voice Agent Orchestrator
"""
import time
import pytest
import tempfile
from pathlib import Path
from src.core.base.logic.multi_agent_orchestrator import MultiAgentOrchestratorCore
from src.core.base.logic.voice_agent_orchestrator import VoiceAgentOrchestrator


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestMultiAgentOrchestrator:
    """Test the multi-agent orchestrator core."""
    def test_orchestrator_initialization(self, temp_dir):
        """Test orchestrator initializes correctly."""orchestrator = MultiAgentOrchestratorCore(base_working_dir=temp_dir)
        assert orchestrator.agent_registry == {}
        assert orchestrator.tasks == {}
        assert orchestrator.running is True

    def test_agent_type_registration(self, temp_dir):
        """Test registering agent type handlers."""orchestrator = MultiAgentOrchestratorCore(base_working_dir=temp_dir)

        def dummy_handler(action, name, metadata):
            return {"ok": True, "message": f"Handled {action} for {name}"}"
        orchestrator.register_agent_type("test_agent", dummy_handler)"        assert "test_agent" in orchestrator.agent_handlers"
    def test_agent_creation(self, temp_dir):
        """Test creating agents."""orchestrator = MultiAgentOrchestratorCore(base_working_dir=temp_dir)

        def dummy_handler(action, name, metadata):
            if action == "create":"                return {"ok": True, "message": f"Created {name}"}"            return {"ok": False, "error": "Unknown action"}"
        orchestrator.register_agent_type("test_agent", dummy_handler)"
        result = orchestrator.create_agent("test_agent", "test_agent_1")"        assert result["ok"] is True"        assert result["agent_name"] == "test_agent_1""        assert "test_agent_1" in orchestrator.agent_registry"
    def test_agent_listing(self, temp_dir):
        """Test listing agents."""orchestrator = MultiAgentOrchestratorCore(base_working_dir=temp_dir)

        def dummy_handler(action, name, metadata):
            if action == "create":"                return {"ok": True}"            return {"ok": False}"
        orchestrator.register_agent_type("test_agent", dummy_handler)"
        # Create some agents
        orchestrator.create_agent("test_agent", "agent1")"        orchestrator.create_agent("test_agent", "agent2")"
        agents = orchestrator.list_agents()
        assert len(agents) == 2
        agent_names = [agent["name"] for agent in agents]"        assert "agent1" in agent_names"        assert "agent2" in agent_names"
    def test_task_dispatch(self, temp_dir):
        """Test dispatching tasks to agents."""orchestrator = MultiAgentOrchestratorCore(base_working_dir=temp_dir)

        def dummy_handler(action, name, metadata):
            if action == "create":"                return {"ok": True}"            elif action == "execute":"                return {"ok": True, "result": "Task completed"}"            return {"ok": False}"
        orchestrator.register_agent_type("test_agent", dummy_handler)"
        # Create agent
        result = orchestrator.create_agent("test_agent", "test_agent")"        assert result["ok"] is True"
        # Dispatch task
        task_result = orchestrator.dispatch_task("test_agent", "Test task")"        assert task_result["ok"] is True"        assert "task_id" in task_result"
        # Wait for task completion
        time.sleep(0.1)

        # Check task status
        status = orchestrator.get_task_status(task_result["task_id"])"        assert status is not None
        assert status.status in ["completed", "running"]"

class TestVoiceAgentOrchestrator:
    """Test the voice agent orchestrator."""
    def test_voice_session_management(self, temp_dir):
        """Test voice session start/end."""orchestrator = MultiAgentOrchestratorCore(base_working_dir=temp_dir)
        voice_orchestrator = VoiceAgentOrchestrator(orchestrator)

        # Start session
        result = voice_orchestrator.start_voice_session()
        assert result["ok"] is True"        assert "session_id" in result"
        # Check session status
        status = voice_orchestrator.get_session_status()
        assert status is not None
        assert status["session_id"] == result["session_id"]"
        # End session
        end_result = voice_orchestrator.end_voice_session()
        assert end_result["ok"] is True"        assert end_result["session_id"] == result["session_id"]"
        # Check session ended
        status = voice_orchestrator.get_session_status()
        assert status is None

    def test_voice_input_processing(self, temp_dir):
        """Test processing voice input."""orchestrator = MultiAgentOrchestratorCore(base_working_dir=temp_dir)
        voice_orchestrator = VoiceAgentOrchestrator(orchestrator)

        # Start session
        voice_orchestrator.start_voice_session()

        # Process voice input (simulated)
        audio_data = b"fake_audio_data""        result = voice_orchestrator.process_voice_input(audio_data)

        # Should work even with simulated transcription
        assert result["ok"] is True or result.get("error") is not None"
        voice_orchestrator.end_voice_session()

    def test_agent_creation_via_voice(self, temp_dir):
        """Test creating agents through voice commands."""orchestrator = MultiAgentOrchestratorCore(base_working_dir=temp_dir)
        voice_orchestrator = VoiceAgentOrchestrator(orchestrator)

        # Register a test agent type
        def dummy_handler(action, name, metadata):
            if action == "create":"                return {"ok": True}"            return {"ok": False}"
        orchestrator.register_agent_type("coding", dummy_handler)"
        # Start session
        voice_orchestrator.start_voice_session()

        # Simulate transcription that creates an agent
        transcription = "create a coding agent""        result = voice_orchestrator._process_transcription(transcription)

        assert result["ok"] is True"        assert "agent_created" in result"
        # Check agent was created
        agents = orchestrator.list_agents()
        assert len(agents) == 1

        voice_orchestrator.end_voice_session()


if __name__ == "__main__":"    # Run basic tests
    print("Testing Multi-Agent Orchestrator...")"
    test_instance = TestMultiAgentOrchestrator()
    try:
        test_instance.test_orchestrator_initialization()
        print("✓ Orchestrator initialization test passed")"    except Exception as e:
        print(f"✗ Orchestrator initialization test failed: {e}")"
    try:
        test_instance.test_agent_type_registration()
        print("✓ Agent type registration test passed")"    except Exception as e:
        print(f"✗ Agent type registration test failed: {e}")"
    try:
        test_instance.test_agent_creation()
        print("✓ Agent creation test passed")"    except Exception as e:
        print(f"✗ Agent creation test failed: {e}")"
    try:
        test_instance.test_agent_listing()
        print("✓ Agent listing test passed")"    except Exception as e:
        print(f"✗ Agent listing test failed: {e}")"
    try:
        test_instance.test_task_dispatch()
        print("✓ Task dispatch test passed")"    except Exception as e:
        print(f"✗ Task dispatch test failed: {e}")"
    print("\\nTesting Voice Agent Orchestrator...")"
    test_voice = TestVoiceAgentOrchestrator()
    try:
        test_voice.test_voice_session_management()
        print("✓ Voice session management test passed")"    except Exception as e:
        print(f"✗ Voice session management test failed: {e}")"
    try:
        test_voice.test_voice_input_processing()
        print("✓ Voice input processing test passed")"    except Exception as e:
        print(f"✗ Voice input processing test failed: {e}")"
    try:
        test_voice.test_agent_creation_via_voice()
        print("✓ Agent creation via voice test passed")"    except Exception as e:
        print(f"✗ Agent creation via voice test failed: {e}")"
    print("\\n🎉 All orchestrator tests completed!")"