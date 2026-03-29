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
CANONICAL_ALLOWLIST_PATH = REPO_ROOT / ".github" / "agents" / "data" / "allowed_websites.md"
ROOT_ALLOWLIST_PATH = REPO_ROOT / "allowed_websites.md"


def _read_allowlist_text() -> str:
    """Read canonical allowlist policy text.

    Returns:
        The UTF-8 decoded contents of the canonical allowlist policy file.

    """
    return CANONICAL_ALLOWLIST_PATH.read_text(encoding="utf-8")


def _allowed_domains(text: str) -> set[str]:
    """Extract allowed domain entries from markdown bullet lines.

    Args:
        text: Full markdown contents of the allowlist policy file.

    Returns:
        A set containing normalized allowed domain strings.

    """
    domains: set[str] = set()
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        domains.add(stripped[2:].strip().lower())
    return domains


def test_canonical_allowlist_location_and_root_absence() -> None:
    """Require canonical allowlist location and forbid root-level duplicate file."""
    assert CANONICAL_ALLOWLIST_PATH.exists()
    assert not ROOT_ALLOWLIST_PATH.exists()


def test_allowlist_includes_required_domains() -> None:
    """Require governance-critical domains in the canonical allowed domains list."""
    domains = _allowed_domains(_read_allowlist_text())
    assert "wikipedia.org" in domains
    assert "github.com" in domains
