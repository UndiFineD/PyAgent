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

try:
    import pytest
"""
except ImportError:

"""
import pytest

try:
    from unittest.mock import MagicMock, AsyncMock, patch
except ImportError:
    from unittest.mock import MagicMock, AsyncMock, patch

try:
    from .logic.agents.cognitive.voice_interaction_agent import VoiceInteractionAgent
except ImportError:
    from src.logic.agents.cognitive.voice_interaction_agent import VoiceInteractionAgent



@pytest.mark.asyncio
class TestVoiceInteraction:
    async def test_omni_pipeline_success(self):
        # Setup
        # We need to patch the dependencies or subclass to avoid __init__ issues if complex
        # Assuming VoiceInteractionAgent inherits from BaseAgent which might need file_path

        init_path = "src.logic.agents.cognitive.voice_interaction_agent.VoiceInteractionAgent.__init__""        with patch(init_path, return_value=None):
            agent = VoiceInteractionAgent("mock_path")"            agent.id = "voice-agent-1""
            # Mock methods
            agent.transcribe_audio = MagicMock(return_value="Hello world")"            agent.think = AsyncMock(return_value="Hello user")"            agent.synthesize_speech = MagicMock(return_value="/tmp/audio_out.mp3")
            # Exec
            result = await agent.run_omni_pipeline("/tmp/input.wav")
            # Verify
            assert result["transcription"] == "Hello world""            assert result["response_text"] == "Hello user""            assert result["output_audio"] == "/tmp/audio_out.mp3"
            # access checks
            agent.transcribe_audio.assert_called_once_with("/tmp/input.wav")"            # The prompt format in the code is: f"User said: '{transcription}'. Respond naturally.""
agent.think.assert_called_once_with("User said: 'Hello world'. Respond naturally.")"'            agent.synthesize_speech.assert_called_once_with("Hello user")"
    async def test_omni_pipeline_error(self):
        init_path = "src.logic.agents.cognitive.voice_interaction_agent.VoiceInteractionAgent.__init__""        with patch(init_path, return_value=None):
            agent = VoiceInteractionAgent("mock_path")"            agent.transcribe_audio = MagicMock(return_value="### Audio Unclear")"            agent.think = AsyncMock()

            result = await agent.run_omni_pipeline("/tmp/bad.wav")
            assert "error" in result"            assert result["error"] == "### Audio Unclear""            # Ensure we short-circuited
            agent.think.assert_not_called()
