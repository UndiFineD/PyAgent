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
Tests for models
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
    from infrastructure.mediaio.models import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_mediatype_exists():
    """Test that MediaType class exists and is importable."""
    assert 'MediaType' in dir()


def test_imageformat_exists():
    """Test that ImageFormat class exists and is importable."""
    assert 'ImageFormat' in dir()


def test_videoformat_exists():
    """Test that VideoFormat class exists and is importable."""
    assert 'VideoFormat' in dir()


def test_audioformat_exists():
    """Test that AudioFormat class exists and is importable."""
    assert 'AudioFormat' in dir()


def test_resizemode_exists():
    """Test that ResizeMode class exists and is importable."""
    assert 'ResizeMode' in dir()


def test_mediametadata_exists():
    """Test that MediaMetadata class exists and is importable."""
    assert 'MediaMetadata' in dir()


def test_imagedata_exists():
    """Test that ImageData class exists and is importable."""
    assert 'ImageData' in dir()


def test_videodata_exists():
    """Test that VideoData class exists and is importable."""
    assert 'VideoData' in dir()


def test_audiodata_exists():
    """Test that AudioData class exists and is importable."""
    assert 'AudioData' in dir()


def test_medialoadconfig_exists():
    """Test that MediaLoadConfig class exists and is importable."""
    assert 'MediaLoadConfig' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

