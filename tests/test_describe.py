#!/usr/bin/env python
"""Test the describe module."""

from pathlib import Path

from src.importer import describe


def test_describe_file(tmp_path: Path) -> None:
    """Test that describe_file returns correct info for a simple file."""
    f = tmp_path / "hello.txt"
    f.write_text("abc")
    info = describe.describe_file(f)
    assert info["path"] == str(f)
    assert info["size"] == 3
