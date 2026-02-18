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
except ImportError:
    import pytest

try:
    from core.base.logic.tts_service import TTSEngine, CoquiTTSEngine, TTSService, text_to_speech
except ImportError:
    from core.base.logic.tts_service import TTSEngine, CoquiTTSEngine, TTSService, text_to_speech



def test_ttsengine_basic():
    assert TTSEngine is not None


def test_coquittsengine_basic():
    assert CoquiTTSEngine is not None


def test_ttsservice_basic():
    assert TTSService is not None


def test_text_to_speech_basic():
    assert callable(text_to_speech)
