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
"""Tests for src/plugins/PluginManager.py."""

from __future__ import annotations

import pytest

from plugins.PluginManager import Plugin, PluginManager, PluginMetadata


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class EchoPlugin(Plugin):
    """Plugin that echoes kwargs back as a dict."""

    setup_called = False
    teardown_called = False

    @property
    def name(self) -> str:
        return "echo"

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(name="echo", version="2.0.0", tags=["io", "debug"])

    def setup(self) -> None:
        EchoPlugin.setup_called = True

    def teardown(self) -> None:
        EchoPlugin.teardown_called = True

    def execute(self, **kwargs):
        return dict(kwargs)


class AddPlugin(Plugin):
    """Plugin that adds two numbers."""

    @property
    def name(self) -> str:
        return "add"

    def execute(self, a: int = 0, b: int = 0):
        return a + b


# ---------------------------------------------------------------------------
# PluginMetadata
# ---------------------------------------------------------------------------

def test_plugin_metadata_defaults() -> None:
    m = PluginMetadata(name="test_plugin")
    assert m.name == "test_plugin"
    assert m.version == "1.0.0"
    assert m.description == ""
    assert m.author == ""
    assert m.tags == []


def test_plugin_metadata_custom() -> None:
    m = PluginMetadata(name="p", version="3.1.0", description="d", author="a", tags=["x"])
    assert m.version == "3.1.0"
    assert m.tags == ["x"]


# ---------------------------------------------------------------------------
# Plugin base
# ---------------------------------------------------------------------------

def test_plugin_default_metadata() -> None:
    p = EchoPlugin()
    assert p.metadata.name == "echo"
    assert p.metadata.version == "2.0.0"


def test_add_plugin_default_metadata() -> None:
    p = AddPlugin()
    # AddPlugin doesn't override metadata — uses default
    assert p.metadata.name == "add"
    assert p.metadata.version == "1.0.0"


# ---------------------------------------------------------------------------
# PluginManager — registration
# ---------------------------------------------------------------------------

def test_register_and_has() -> None:
    pm = PluginManager()
    pm.register(EchoPlugin())
    assert pm.has("echo")
    assert len(pm) == 1


def test_register_calls_setup() -> None:
    EchoPlugin.setup_called = False
    pm = PluginManager()
    pm.register(EchoPlugin())
    assert EchoPlugin.setup_called


def test_register_replaces_plugin_calls_teardown() -> None:
    EchoPlugin.teardown_called = False
    pm = PluginManager()
    pm.register(EchoPlugin())
    pm.register(EchoPlugin())   # second time — should teardown old first
    assert EchoPlugin.teardown_called


def test_unregister_calls_teardown() -> None:
    EchoPlugin.teardown_called = False
    pm = PluginManager()
    pm.register(EchoPlugin())
    pm.unregister("echo")
    assert EchoPlugin.teardown_called
    assert not pm.has("echo")


def test_unregister_unknown_raises() -> None:
    pm = PluginManager()
    with pytest.raises(KeyError):
        pm.unregister("nonexistent")


# ---------------------------------------------------------------------------
# PluginManager — discovery
# ---------------------------------------------------------------------------

def test_list_plugins_sorted() -> None:
    pm = PluginManager()
    pm.register(AddPlugin())
    pm.register(EchoPlugin())
    names = [m.name for m in pm.list_plugins()]
    assert names == ["add", "echo"]  # sorted


def test_find_by_tag() -> None:
    pm = PluginManager()
    pm.register(EchoPlugin())
    pm.register(AddPlugin())
    tagged = pm.find_by_tag("debug")
    assert len(tagged) == 1
    assert tagged[0].name == "echo"


def test_find_by_tag_no_match() -> None:
    pm = PluginManager()
    pm.register(AddPlugin())
    assert pm.find_by_tag("nonexistent") == []


def test_get_unknown_raises() -> None:
    pm = PluginManager()
    with pytest.raises(KeyError, match="unknown"):
        pm.get("unknown")


# ---------------------------------------------------------------------------
# PluginManager — execution
# ---------------------------------------------------------------------------

def test_execute_echo() -> None:
    pm = PluginManager()
    pm.register(EchoPlugin())
    result = pm.execute("echo", foo="bar", num=42)
    assert result == {"foo": "bar", "num": 42}


def test_execute_add() -> None:
    pm = PluginManager()
    pm.register(AddPlugin())
    assert pm.execute("add", a=3, b=4) == 7


def test_execute_unknown_raises() -> None:
    pm = PluginManager()
    with pytest.raises(KeyError):
        pm.execute("missing_plugin")


# ---------------------------------------------------------------------------
# PluginManager — lifecycle
# ---------------------------------------------------------------------------

def test_shutdown_calls_teardown_all() -> None:
    EchoPlugin.teardown_called = False
    pm = PluginManager()
    pm.register(EchoPlugin())
    pm.register(AddPlugin())
    pm.shutdown()
    assert EchoPlugin.teardown_called
    assert len(pm) == 0


def test_repr() -> None:
    pm = PluginManager()
    pm.register(EchoPlugin())
    assert "echo" in repr(pm)
