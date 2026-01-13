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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""
Agent specializing in voice-based interaction and thought-to-speech conversion.
Part of Phase 127 Swarm UX.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from pathlib import Path
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

__version__ = VERSION

class VoiceInteractionAgent(BaseAgent):
    """Voice interface for the swarm, supporting STT and TTS."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Voice Interaction Agent. "
            "You process audio streams into text and convert agent thoughts into speech. "
            "Your goal is to provide a seamless natural language audio interface."
        )

    @as_tool
    def synthesize_speech(self, text: str, voice_profile: str = "neutral") -> str:
        """Converts text into an audio file path (Simulation/gTTS)."""
        logging.info(f"VoiceAgent: Synthesizing speech with profile {voice_profile}...")
        audio_dir = Path("data/audio")
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        target_path = audio_dir / f"speech_{abs(hash(text))}.mp3"
        
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='en')
            tts.save(str(target_path))
            return str(target_path)
        except ImportError:
            logging.warning("gTTS not installed. Returning simulation path.")
            return f"data/audio/simulation_{abs(hash(text))}.wav"

    @as_tool
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribes audio file to text using speech recognition."""
        logging.info(f"VoiceAgent: Transcribing {audio_path}...")
        
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = r.record(source)
            text = r.recognize_google(audio)
            return text
        except (ImportError, Exception) as e:
            logging.error(f"Transcription failed: {str(e)}")
            return "### Transcription Unavailable (Check dependencies)"

    def think_aloud(self, thought: str) -> str:
        """Standard Swarm UX: Agents can broadcast their 'internal' monologue via voice."""
        audio_file = self.synthesize_speech(thought)
        logging.info(f"Agent {self.id} Thinking Aloud: '{thought}' (Audio: {audio_file})")
        return audio_file