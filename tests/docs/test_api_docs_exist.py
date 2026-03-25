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
"""Canary tests for prj0000073 — verify that all API docs files exist, are non-empty,
and contain required structural sections."""

import os

_API_DOCS_ROOT = "docs/api"

_REQUIRED_FILES = [
    "index.md",
    "authentication.md",
    "rest-endpoints.md",
    "websocket.md",
    "errors.md",
]

_MIN_SIZE_BYTES = 1024  # each file must be ≥ 1 KB


def test_api_docs_files_exist() -> None:
    """All five required API docs files must be present."""
    for filename in _REQUIRED_FILES:
        path = os.path.join(_API_DOCS_ROOT, filename)
        assert os.path.isfile(path), f"Missing API docs file: {path}"


def test_api_docs_files_non_empty() -> None:
    """All API docs files must be at least 1 KB."""
    for filename in _REQUIRED_FILES:
        path = os.path.join(_API_DOCS_ROOT, filename)
        size = os.path.getsize(path)
        assert size >= _MIN_SIZE_BYTES, f"{path} is too small ({size} bytes, expected ≥ {_MIN_SIZE_BYTES})"


def test_api_docs_no_todo_markers() -> None:
    """No file should contain unresolved TODO markers."""
    for filename in _REQUIRED_FILES:
        path = os.path.join(_API_DOCS_ROOT, filename)
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        assert "TODO" not in content, f"Unresolved TODO found in {path}"


def test_index_contains_required_sections() -> None:
    """index.md must link to all four sibling pages."""
    path = os.path.join(_API_DOCS_ROOT, "index.md")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    for link in ("authentication.md", "rest-endpoints.md", "websocket.md", "errors.md"):
        assert link in content, f"index.md is missing a link to {link}"


def test_authentication_contains_required_sections() -> None:
    """authentication.md must cover API Key, JWT, and DEV_MODE."""
    path = os.path.join(_API_DOCS_ROOT, "authentication.md")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    for keyword in ("API Key", "JWT", "DEV_MODE", "PYAGENT_API_KEY", "PYAGENT_JWT_SECRET"):
        assert keyword in content, f"authentication.md missing required content: {keyword!r}"


def test_rest_endpoints_covers_all_methods() -> None:
    """rest-endpoints.md must include GET, POST, PATCH, and DELETE endpoint docs."""
    path = os.path.join(_API_DOCS_ROOT, "rest-endpoints.md")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    for method in ("GET", "POST", "PATCH", "DELETE"):
        assert method in content, f"rest-endpoints.md missing HTTP method: {method}"


def test_websocket_contains_mermaid_and_close_codes() -> None:
    """websocket.md must contain a Mermaid diagram and the 4401 close code."""
    path = os.path.join(_API_DOCS_ROOT, "websocket.md")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    assert "mermaid" in content, "websocket.md is missing the Mermaid diagram"
    assert "4401" in content, "websocket.md is missing the 4401 close code"


def test_errors_contains_rate_limit_and_close_codes() -> None:
    """errors.md must document 429, 4401, and the Retry-After header."""
    path = os.path.join(_API_DOCS_ROOT, "errors.md")
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    for marker in ("429", "4401", "Retry-After"):
        assert marker in content, f"errors.md missing required content: {marker!r}"
