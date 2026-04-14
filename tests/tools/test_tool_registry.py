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
"""Tests for prj0000017: tool_registry and __main__ utilities."""

import pytest

from src.tools.tool_registry import (
    _REGISTRY,
    Tool,
    get_tool,
    list_tools,
    register_tool,
    run_tool,
)


@pytest.fixture(autouse=True)
def _clean_registry():
    """Isolate each test from global registry side-effects."""
    snapshot = dict(_REGISTRY)
    yield
    _REGISTRY.clear()
    _REGISTRY.update(snapshot)


def test_register_and_retrieve() -> None:
    def my_main(args=None):
        return 0

    register_tool("test-tool-a", my_main, "A test tool")
    t = get_tool("test-tool-a")
    assert t is not None
    assert t.name == "test-tool-a"
    assert t.description == "A test tool"


def test_register_duplicate_same_description_is_idempotent() -> None:
    def my_main(args=None):
        return 0

    register_tool("test-dup", my_main, "desc")
    register_tool("test-dup", my_main, "desc")  # should not raise
    assert get_tool("test-dup") is not None


def test_register_duplicate_different_description_raises() -> None:
    def my_main(args=None):
        return 0

    register_tool("test-conflict", my_main, "first")
    with pytest.raises(ValueError, match="already registered"):
        register_tool("test-conflict", my_main, "second")


def test_list_tools_sorted() -> None:
    register_tool("zzz-last", lambda a: 0, "z-tool")
    register_tool("aaa-first", lambda a: 0, "a-tool")
    names = [t.name for t in list_tools() if t.name in {"zzz-last", "aaa-first"}]
    assert names == sorted(names)


def test_run_tool_int_result() -> None:
    register_tool("int-tool", lambda a: 42, "returns 42")
    assert run_tool("int-tool") == 42


def test_run_tool_unknown_raises() -> None:
    with pytest.raises(KeyError, match="Unknown tool"):
        run_tool("no-such-tool")


def test_tool_frozen_dataclass() -> None:
    def fn(a=None):
        return 0

    register_tool("frozen-test", fn, "desc")
    t = get_tool("frozen-test")
    assert isinstance(t, Tool)
    with pytest.raises(Exception):
        t.name = "other"  # type: ignore[misc]


def test_main_cli_list(capsys) -> None:
    """Calling __main__.main() with no args prints available tools."""
    from src.tools.__main__ import main

    register_tool("listed-tool", lambda a: 0, "shows up in list")
    rc = main([])
    assert rc == 0
    out = capsys.readouterr().out
    assert "listed-tool" in out


def test_main_cli_run() -> None:
    """Calling __main__.main() with a tool name runs it."""
    from src.tools.__main__ import main

    register_tool("run-me", lambda a: 7, "returns 7")
    rc = main(["run-me"])
    assert rc == 7


def test_main_cli_unknown_tool(capsys) -> None:
    """Calling __main__.main() with unknown tool name returns 1."""
    from src.tools.__main__ import main

    rc = main(["definitely-not-a-tool"])
    assert rc == 1
