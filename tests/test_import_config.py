#!/usr/bin/env python
"""Test the importer.config module."""
import asyncio
from pathlib import Path

from importer import config


def test_parse_manifest(tmp_path: Path) -> None:
    """Test that parse_manifest can read a simple manifest file."""

    async def inner() -> None:
        """Inner async function to test parse_manifest."""
        manifest = tmp_path / "github.md"
        manifest.write_text("foo/bar\n")

        repos = await config.parse_manifest(manifest)
        assert repos == [("foo", "bar")]

    asyncio.run(inner())
