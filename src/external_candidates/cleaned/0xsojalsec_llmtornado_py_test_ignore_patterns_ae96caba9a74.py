# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_llmtornado.py\src.py\llmtornado.py\llmtornado.py\tests.py\test_ignore_patterns_ae96caba9a74.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-LLMTornado\src\LlmTornado.FsKb\LlmTornado.FsKb\tests\test_ignore_patterns.py

"""Tests for ignore pattern matching."""

import os

import tempfile

from pathlib import Path

import pytest

from fskb.utils import IgnorePatternMatcher


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""

    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_default_ignores(temp_dir):
    """Test default ignore patterns."""

    matcher = IgnorePatternMatcher(temp_dir)

    # Should ignore .git

    assert matcher.should_ignore(temp_dir / ".git" / "config")

    # Should ignore __pycache__

    assert matcher.should_ignore(temp_dir / "__pycache__" / "test.pyc")

    # Should not ignore normal files

    assert not matcher.should_ignore(temp_dir / "test.py")


def test_gitignore_patterns(temp_dir):
    """Test .gitignore pattern matching."""

    # Create .gitignore

    gitignore = temp_dir / ".gitignore"

    gitignore.write_text("*.log\nnode_modules/\n")

    matcher = IgnorePatternMatcher(temp_dir, use_gitignore=True)

    # Should ignore .log files

    assert matcher.should_ignore(temp_dir / "test.log")

    # Should ignore node_modules

    assert matcher.should_ignore(temp_dir / "node_modules" / "package.json")

    # Should not ignore other files

    assert not matcher.should_ignore(temp_dir / "test.py")


def test_fskbignore_patterns(temp_dir):
    """Test .fskbignore pattern matching."""

    # Create .fskbignore

    fskbignore = temp_dir / ".fskbignore"

    fskbignore.write_text("*.bak\ntemp/\n")

    matcher = IgnorePatternMatcher(temp_dir, use_fskbignore=True)

    # Should ignore .bak files

    assert matcher.should_ignore(temp_dir / "test.bak")

    # Should ignore temp directory

    assert matcher.should_ignore(temp_dir / "temp" / "file.txt")


def test_pattern_reload(temp_dir):
    """Test reloading patterns."""

    matcher = IgnorePatternMatcher(temp_dir)

    # Initially should not ignore .custom files

    assert not matcher.should_ignore(temp_dir / "test.custom")

    # Add .gitignore

    gitignore = temp_dir / ".gitignore"

    gitignore.write_text("*.custom\n")

    # Reload patterns

    matcher.reload()

    # Now should ignore .custom files

    assert matcher.should_ignore(temp_dir / "test.custom")
