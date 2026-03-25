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
"""Tests for scripts/AgentDocFrequency.py.

prj0000030 — agent doc frequency.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

# Make scripts/ importable
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from AgentDocFrequency import DocStats, analyse_docs, format_table  # type: ignore[import]  # noqa: E402


# ─── Unit: DocStats ────────────────────────────────────────────────────────

def test_docstats_defaults():
    """DocStats must default to 0 commits, None last_updated, 1.0 staleness."""
    stats = DocStats(name="foo.md", path=Path("foo.md"))
    assert stats.commit_count == 0
    assert stats.last_updated is None
    assert stats.staleness == 1.0


def test_docstats_fields_assignable():
    """DocStats fields must be mutable."""
    stats = DocStats(name="x.md", path=Path("x.md"))
    stats.commit_count = 5
    stats.staleness = 0.3
    assert stats.commit_count == 5
    assert stats.staleness == 0.3


# ─── Unit: format_table ───────────────────────────────────────────────────

def test_format_table_contains_header():
    """format_table must include a Markdown pipe header."""
    table = format_table([])
    assert "| File |" in table
    assert "| Commits |" in table


def test_format_table_contains_separator():
    """format_table must include a Markdown separator row."""
    table = format_table([])
    assert "|---" in table


def test_format_table_includes_doc_name():
    """format_table must include each DocStats name in the output."""
    stats = DocStats(name="0master.memory.md", path=Path("0master.memory.md"))
    stats.commit_count = 7
    stats.last_updated = datetime(2026, 1, 15, tzinfo=timezone.utc)
    stats.staleness = 0.5
    table = format_table([stats])
    assert "0master.memory.md" in table
    assert "7" in table
    assert "0.50" in table


def test_format_table_never_for_no_last_updated():
    """format_table must show 'never' for files with no git history."""
    stats = DocStats(name="new.md", path=Path("new.md"))
    table = format_table([stats])
    assert "never" in table


# ─── Integration: analyse_docs against real repo ─────────────────────────

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / ".github" / "agents" / "data"


@pytest.mark.skipif(not DOCS_DIR.exists(), reason="docs/agents not present")
def test_analyse_docs_returns_all_memory_files():
    """analyse_docs must return one entry per *.memory.md file."""
    expected = list(DOCS_DIR.glob("*.memory.md"))
    result = analyse_docs(DOCS_DIR, repo_root=REPO_ROOT)
    assert len(result) == len(expected)


@pytest.mark.skipif(not DOCS_DIR.exists(), reason="docs/agents not present")
def test_analyse_docs_sorted_by_staleness_desc():
    """analyse_docs must return entries sorted staleness descending."""
    result = analyse_docs(DOCS_DIR, repo_root=REPO_ROOT)
    scores = [s.staleness for s in result]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.skipif(not DOCS_DIR.exists(), reason="docs/agents not present")
def test_analyse_docs_staleness_in_range():
    """Each staleness score must be in [0.0, 1.0]."""
    result = analyse_docs(DOCS_DIR, repo_root=REPO_ROOT)
    for s in result:
        assert 0.0 <= s.staleness <= 1.0, f"{s.name}: staleness={s.staleness}"


@pytest.mark.skipif(not DOCS_DIR.exists(), reason="docs/agents not present")
def test_analyse_docs_commit_count_non_negative():
    """Commit counts must be non-negative integers."""
    result = analyse_docs(DOCS_DIR, repo_root=REPO_ROOT)
    for s in result:
        assert s.commit_count >= 0


@pytest.mark.skipif(not DOCS_DIR.exists(), reason="docs/agents not present")
def test_analyse_docs_full_table_output():
    """format_table on real results must be a non-empty string."""
    result = analyse_docs(DOCS_DIR, repo_root=REPO_ROOT, days_stale=30)
    table = format_table(result)
    assert len(table) > 0
    assert "memory.md" in table


# ─── CLI smoke test ───────────────────────────────────────────────────────

def test_main_runs_without_error(capsys):
    """CLI main() must print a table and summary without raising."""
    import sys
    import AgentDocFrequency  # type: ignore[import]

    old_argv = sys.argv
    sys.argv = ["AgentDocFrequency.py", "--docs-dir", str(DOCS_DIR), "--days-stale", "30"]
    try:
        AgentDocFrequency.main()
    except SystemExit:
        pass  # acceptable exit
    finally:
        sys.argv = old_argv
    captured = capsys.readouterr()
    assert "memory.md" in captured.out or "Total docs" in captured.out
