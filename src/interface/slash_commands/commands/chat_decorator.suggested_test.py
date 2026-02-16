#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from interface.slash_commands.commands.chat_decorator.suggested import cmd_human, cmd_ai, cmd_system_message, cmd_thinking, cmd_codeblock, cmd_chat, cmd_chat_theme, cmd_chat_preview


def test_cmd_human_basic():
    assert callable(cmd_human)


def test_cmd_ai_basic():
    assert callable(cmd_ai)


def test_cmd_system_message_basic():
    assert callable(cmd_system_message)


def test_cmd_thinking_basic():
    assert callable(cmd_thinking)


def test_cmd_codeblock_basic():
    assert callable(cmd_codeblock)


def test_cmd_chat_basic():
    assert callable(cmd_chat)


def test_cmd_chat_theme_basic():
    assert callable(cmd_chat_theme)


def test_cmd_chat_preview_basic():
    assert callable(cmd_chat_preview)
