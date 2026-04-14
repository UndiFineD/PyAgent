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

import pytest

from scripts.changelog import generate_entry


def test_generate_entry_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that generate_entry returns an empty string when there are no commits since the last tag."""
    monkeypatch.setattr("subprocess.check_output", lambda *args, **kwargs: "".encode())
    assert generate_entry() == ""


def test_generate_entry_various(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that generate_entry correctly categorizes commits based on their prefixes."""
    # simulate git output with feat, fix and other
    output = "feat: add foo\nfix: correct bar\nchore: cleanup\n"
    monkeypatch.setattr("subprocess.check_output", lambda *args, **kwargs: output)
    result = generate_entry()
    assert "### Added" in result
    assert "feat: add foo" in result
    assert "### Fixed" in result
    assert "fix: correct bar" in result
    # chore should fall into Changed section because it doesn't start with feat or fix
    assert "### Changed" in result
    assert "chore: cleanup" in result
