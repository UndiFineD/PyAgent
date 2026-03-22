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
"""Tests for tools.pm.email module (prj0000021)."""
import pytest
from tools.pm.email import render


@pytest.mark.asyncio
async def test_render_simple_substitution():
    result = await render("Hello {{name}}!", {"name": "Alice"})
    assert result == "Hello Alice!"


@pytest.mark.asyncio
async def test_render_multiple_keys():
    tpl = "{{greeting}} {{name}}, your sprint is {{status}}."
    ctx = {"greeting": "Hi", "name": "Bob", "status": "green"}
    result = await render(tpl, ctx)
    assert result == "Hi Bob, your sprint is green."


@pytest.mark.asyncio
async def test_render_missing_key_leaves_placeholder():
    result = await render("Hello {{name}}!", {})
    assert "{{name}}" in result


@pytest.mark.asyncio
async def test_render_empty_template():
    result = await render("", {"key": "val"})
    assert result == ""
