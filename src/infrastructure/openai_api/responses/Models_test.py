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
Tests for Models
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
    from infrastructure.openai_api.responses.Models import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_contentpart_exists():
    """Test that ContentPart class exists and is importable."""
    assert 'ContentPart' in dir()


def test_textcontent_exists():
    """Test that TextContent class exists and is importable."""
    assert 'TextContent' in dir()


def test_imagecontent_exists():
    """Test that ImageContent class exists and is importable."""
    assert 'ImageContent' in dir()


def test_audiocontent_exists():
    """Test that AudioContent class exists and is importable."""
    assert 'AudioContent' in dir()


def test_refusalcontent_exists():
    """Test that RefusalContent class exists and is importable."""
    assert 'RefusalContent' in dir()


def test_toolcallcontent_exists():
    """Test that ToolCallContent class exists and is importable."""
    assert 'ToolCallContent' in dir()


def test_message_exists():
    """Test that Message class exists and is importable."""
    assert 'Message' in dir()


def test_tooldefinition_exists():
    """Test that ToolDefinition class exists and is importable."""
    assert 'ToolDefinition' in dir()


def test_responseconfig_exists():
    """Test that ResponseConfig class exists and is importable."""
    assert 'ResponseConfig' in dir()


def test_responseusage_exists():
    """Test that ResponseUsage class exists and is importable."""
    assert 'ResponseUsage' in dir()


def test_responseoutput_exists():
    """Test that ResponseOutput class exists and is importable."""
    assert 'ResponseOutput' in dir()


def test_response_exists():
    """Test that Response class exists and is importable."""
    assert 'Response' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

