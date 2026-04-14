#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the importer configuration helpers."""

from __future__ import annotations

import asyncio
from pathlib import Path


def test_parse_manifest(tmp_path: Path) -> None:
    """Test that parse_manifest can read a simple manifest file."""
    from src.importer.config import parse_manifest

    # create a temporary manifest file with comments, blanks, and valid entries
    data = """
    # this is a comment

    user1/repo1
    user2/repo2
    invalidline
    user3/repo3
    """
    p = tmp_path / "manifest.txt"
    p.write_text(data)

    result = asyncio.run(parse_manifest(p))
    assert result == [("user1", "repo1"), ("user2", "repo2"), ("user3", "repo3")]
