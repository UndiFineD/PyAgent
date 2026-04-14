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
"""Tests for the plugin marketplace backend endpoint.

prj0000059 — plugin-marketplace-browser.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def _get_plugins(client_ip: str):
    """Fetch /api/plugins using a test-specific forwarded IP to avoid cross-test rate-limit coupling."""
    return client.get("/api/plugins", headers={"x-forwarded-for": client_ip})


def test_plugins_endpoint_returns_200():
    """GET /api/plugins returns HTTP 200."""
    response = _get_plugins("plugins-test-1")
    assert response.status_code == 200


def test_plugins_response_has_plugins_key():
    """Response body contains a 'plugins' key."""
    response = _get_plugins("plugins-test-2")
    data = response.json()
    assert "plugins" in data


def test_plugins_registry_is_non_empty():
    """Plugin registry has at least one entry."""
    response = _get_plugins("plugins-test-3")
    plugins = response.json()["plugins"]
    assert len(plugins) > 0


def test_plugin_has_required_fields():
    """Each plugin entry contains all required fields."""
    response = _get_plugins("plugins-test-4")
    plugins = response.json()["plugins"]
    required = {"id", "name", "description", "author", "version", "tags", "installed"}
    for plugin in plugins:
        missing = required - set(plugin.keys())
        assert not missing, f"Plugin {plugin.get('id')!r} missing fields: {missing}"


def test_plugins_without_auth_returns_200():
    """Endpoint is accessible without an Authorization header (public route)."""
    response = _get_plugins("plugins-test-5")
    assert response.status_code == 200
