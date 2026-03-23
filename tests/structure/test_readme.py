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
"""Structural tests for README.md — prj0000051.

Verifies that the updated README meets all 16 automated acceptance criteria
from readme-update.plan.md.  Tests are TDD-style: they are written before the
README is authored, so all content checks skip gracefully until the file is
present with the correct H1 marker.
"""

import re
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
_README_PATH = REPO_ROOT / "README.md"

# ---------------------------------------------------------------------------
# Load file once at module import time.
# _FILE_MISSING is True when the README either does not exist yet or has not
# been replaced with the updated version (identified by the exact H1 marker
# "# PyAgent" on the first line).  All content-dependent tests skip when
# _FILE_MISSING is True; only test_readme_exists is intended to fail.
# ---------------------------------------------------------------------------
try:
    _content = _README_PATH.read_text(encoding="utf-8")
    _lines = _content.splitlines()
except FileNotFoundError:
    _content = ""
    _lines = []

_FILE_MISSING = (
    not _README_PATH.exists()
    or not _lines
    or _lines[0].strip() != "# PyAgent"
)

_SKIP_CONTENT = pytest.mark.skipif(_FILE_MISSING, reason="README not yet written (awaiting @6code)")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _section_lines(heading_prefix: str) -> list:
    """Return body lines of the first H2 section whose text starts with heading_prefix."""
    body: list = []
    in_section = False
    for line in _lines:
        if line.startswith("## "):
            if in_section:
                break
            if line.startswith(heading_prefix):
                in_section = True
        elif in_section:
            body.append(line)
    return body


# ---------------------------------------------------------------------------
# 1. File existence — FAILS before README is written/updated
# ---------------------------------------------------------------------------

def test_readme_exists() -> None:
    """README.md must exist at the repo root and open with the required H1.

    This test intentionally fails when the README has not yet been replaced
    with the prj0000051 version.  It acts as the TDD "red" gate.
    """
    assert _README_PATH.exists(), "README.md not found at repo root"
    assert _lines, "README.md is empty"
    assert _lines[0].strip() == "# PyAgent", (
        f"Expected first line '# PyAgent', got: {_lines[0]!r}"
    )


# ---------------------------------------------------------------------------
# 2. H1 title (content test — skips until README is updated)
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
def test_readme_h1() -> None:
    """First non-empty line must be exactly '# PyAgent'."""
    first_non_empty = next((ln for ln in _lines if ln.strip()), "")
    assert first_non_empty.strip() == "# PyAgent", (
        f"Expected '# PyAgent', got: {first_non_empty!r}"
    )


# ---------------------------------------------------------------------------
# 3. Required H2 headings (parametrized)
# ---------------------------------------------------------------------------

_REQUIRED_H2S = [
    "## What is PyAgent?",
    "## Quick Start",
    "## NebulaOS — The Frontend",
    "## Backend",
    "## Rust Core — The Zero-Loop Engine",
    "## Architecture Decisions",
    "## Project History",
    "## Future Roadmap",
    "## Development Reference",
    "## License",
]


@_SKIP_CONTENT
@pytest.mark.parametrize("heading", _REQUIRED_H2S)
def test_required_h2_headings(heading: str) -> None:
    """Each required H2 heading must appear in the document."""
    # Use startswith on lines to avoid partial matches inside code blocks.
    headings_in_doc = [ln for ln in _lines if ln.startswith("## ")]
    assert any(h.startswith(heading) for h in headings_in_doc), (
        f"H2 heading not found: {heading!r}"
    )


# ---------------------------------------------------------------------------
# 4. ## What is PyAgent? — single flowing paragraph
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
def test_what_is_single_paragraph() -> None:
    """The '## What is PyAgent?' section must be a single paragraph.

    Criteria:
    - No unordered list lines (starting with '-' or '*')
    - No H3 subheadings (starting with '###')
    - No numbered list lines (starting with a digit followed by '.')
    """
    body = _section_lines("## What is PyAgent?")
    for line in body:
        stripped = line.strip()
        if not stripped:
            continue
        assert not re.match(r"^[-*]\s", stripped), (
            f"Bullet found in '## What is PyAgent?': {line!r}"
        )
        assert not stripped.startswith("###"), (
            f"Subheading found in '## What is PyAgent?': {line!r}"
        )
        assert not re.match(r"^\d+\.\s", stripped), (
            f"Numbered list item found in '## What is PyAgent?': {line!r}"
        )


# ---------------------------------------------------------------------------
# 5. Key numbers present
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
@pytest.mark.parametrize("token", ["666", "51", "41%", "317", "v4.0.0", "VOYAGER"])
def test_key_numbers_present(token: str) -> None:
    """Required key number / token must appear somewhere in the document."""
    assert token in _content, f"Token not found in README: {token!r}"


# ---------------------------------------------------------------------------
# 6. install.ps1 flag variants documented
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
@pytest.mark.parametrize("flag", ["-SkipRust", "-SkipWeb", "-SkipDev", "-CI", "-Force"])
def test_install_flags_documented(flag: str) -> None:
    """Each install.ps1 flag must appear in the document."""
    assert flag in _content, f"install.ps1 flag not documented: {flag!r}"


# ---------------------------------------------------------------------------
# 7. start.ps1 sub-commands documented
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
@pytest.mark.parametrize("cmd", ["start", "stop", "restart", "status"])
def test_start_commands_documented(cmd: str) -> None:
    """Each start.ps1 sub-command must appear in the document."""
    assert cmd in _content, f"start.ps1 sub-command not documented: {cmd!r}"


# ---------------------------------------------------------------------------
# 8. Project History — exactly 51 prj0000 entries
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
def test_project_history_count() -> None:
    """There must be exactly 51 'prj0000' entries across the document."""
    matches = re.findall(r"prj0000\d{3}", _content)
    count = len(matches)
    assert count == 51, (
        f"Expected 51 'prj0000NNN' entries, found {count}"
    )


# ---------------------------------------------------------------------------
# 9. Future Roadmap — exactly 10 numbered items
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
def test_future_roadmap_count() -> None:
    """## Future Roadmap section must contain exactly 10 numbered items."""
    body = _section_lines("## Future Roadmap")
    items = [ln for ln in body if re.match(r"^\d+\.\s", ln.strip())]
    assert len(items) == 10, (
        f"Expected 10 numbered items under '## Future Roadmap', found {len(items)}"
    )


# ---------------------------------------------------------------------------
# 10. No TODO / FIXME / TBD
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
def test_no_todo_fixme() -> None:
    """README must not contain TODO, FIXME, or TBD (case-insensitive)."""
    pattern = re.compile(r"\b(TODO|FIXME|TBD)\b", re.IGNORECASE)
    violations = [
        (i + 1, ln)
        for i, ln in enumerate(_lines)
        if pattern.search(ln)
    ]
    assert not violations, (
        "Found TODO/FIXME/TBD stubs:\n"
        + "\n".join(f"  L{lineno}: {ln}" for lineno, ln in violations)
    )


# ---------------------------------------------------------------------------
# 11. No ```bash fences — all shell code must use ```powershell
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
def test_powershell_fences() -> None:
    """Shell code fences must use '```powershell', not '```bash' or plain '```'."""
    violations = [
        (i + 1, ln)
        for i, ln in enumerate(_lines)
        if re.match(r"^```bash\b", ln.strip())
    ]
    assert not violations, (
        "Found ```bash fences (must be ```powershell):\n"
        + "\n".join(f"  L{lineno}: {ln}" for lineno, ln in violations)
    )


# ---------------------------------------------------------------------------
# 12. Architecture Decisions — numbered list 1–8
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
def test_architecture_decisions_numbered() -> None:
    """## Architecture Decisions section must use a numbered list (1. through 8.)."""
    body = _section_lines("## Architecture Decisions")
    for expected_num in range(1, 9):
        prefix = f"{expected_num}."
        found = any(ln.strip().startswith(prefix) for ln in body)
        assert found, (
            f"Numbered item '{prefix}' not found in '## Architecture Decisions'"
        )


# ---------------------------------------------------------------------------
# 13. Rust technology keywords
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
@pytest.mark.parametrize("keyword", ["Tokio", "PyO3", "maturin"])
def test_rust_keywords(keyword: str) -> None:
    """Key Rust technology names must appear in the document."""
    assert keyword in _content, f"Rust keyword not found in README: {keyword!r}"


# ---------------------------------------------------------------------------
# 14. NebulaOS app names
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
@pytest.mark.parametrize("app", ["CodeBuilder", "AgentChat", "Conky"])
def test_nebula_apps(app: str) -> None:
    """Core NebulaOS app names must appear in the document."""
    assert app in _content, f"NebulaOS app not found in README: {app!r}"


# ---------------------------------------------------------------------------
# 15. Backend REST endpoints
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
@pytest.mark.parametrize("endpoint", ["/health", "/ws"])
def test_backend_endpoints(endpoint: str) -> None:
    """Backend API endpoints must appear in the document."""
    assert endpoint in _content, f"Backend endpoint not found in README: {endpoint!r}"


# ---------------------------------------------------------------------------
# 16. install.ps1 mentioned
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
def test_install_ps1_mentioned() -> None:
    """'install.ps1' must appear in the document."""
    assert "install.ps1" in _content, "install.ps1 not mentioned in README"


# ---------------------------------------------------------------------------
# 17. start.ps1 mentioned
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
def test_start_ps1_mentioned() -> None:
    """'start.ps1' must appear in the document."""
    assert "start.ps1" in _content, "start.ps1 not mentioned in README"


# ---------------------------------------------------------------------------
# 18. Line length — soft check (warn-only via xfail)
# ---------------------------------------------------------------------------

@_SKIP_CONTENT
def test_line_length() -> None:
    """No prose line should exceed 120 characters (soft check — marks xfail on violation)."""
    long_lines = [
        (i + 1, len(ln), ln)
        for i, ln in enumerate(_lines)
        if len(ln) > 120
    ]
    if long_lines:
        summary = "\n".join(
            f"  L{lineno} ({length} chars): {ln[:80]}…"
            for lineno, length, ln in long_lines[:10]
        )
        pytest.xfail(
            f"{len(long_lines)} line(s) exceed 120 chars (soft limit):\n{summary}"
        )
