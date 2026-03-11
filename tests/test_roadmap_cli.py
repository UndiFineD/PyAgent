#!/usr/bin/env python3
"""Test the roadmap CLI."""

from pathlib import Path

from roadmap import cli


def test_roadmap_cli(tmp_path: Path) -> None:
    """Test the roadmap CLI."""
    outdir = tmp_path / "output"
    outdir.mkdir()
    cli.generate(outdir)
    files = list(outdir.iterdir())
    assert files, "No file produced by CLI"
