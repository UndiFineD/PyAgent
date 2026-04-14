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

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
COPILOT_INSTRUCTIONS_PATH = REPO_ROOT / ".github" / "copilot-instructions.md"


def _read_copilot_instructions() -> str:
    """Read repository Copilot instruction text.

    Returns:
        UTF-8 decoded instruction markdown content.

    """
    return COPILOT_INSTRUCTIONS_PATH.read_text(encoding="utf-8")


def test_copilot_instructions_reference_local_search_first() -> None:
    """Require local search-first language in Copilot instructions."""
    text = _read_copilot_instructions().lower()
    assert "local code search first" in text
    assert "search_subagent" in text
    assert "rg" in text


def test_copilot_instructions_reference_canonical_allowlist_path() -> None:
    """Require canonical allowlist path reference in Copilot instructions."""
    text = _read_copilot_instructions()
    assert ".github/agents/data/allowed_websites.md" in text
