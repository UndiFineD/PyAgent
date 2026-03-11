#!/usr/bin/env python
"""Test the downloader module."""

from pathlib import Path

from importer import downloader


def test_download_repo(tmp_path: Path) -> None:
    """Test that download_repo can download a simple public repo."""
    target = tmp_path / "foo" / "bar"
    downloader.download_repo("foo/bar", target)
    assert target.exists()
    assert (target / "README.md").exists()
