#!/usr/bin/env python
"""Test the end-to-end importer flow using stubs."""

import asyncio
from pathlib import Path


def test_importer_flow(tmp_path: Path) -> None:
    """Test the end-to-end importer flow using stubs."""
    # end-to-end smoke using stubs
    from src.importer.compile import compile_architecture
    from src.importer.config import parse_manifest
    from src.importer.describe import describe_file
    from src.importer.downloader import download_repo

    manifest = tmp_path / "github.md"
    manifest.write_text("a/b\n")

    repos = asyncio.run(parse_manifest(manifest))
    assert repos == [("a", "b")]

    target = tmp_path / "a" / "b"
    download_repo("a/b", target)

    readme = target / "README.md"
    assert readme.exists(), "download_repo should create a README.md"

    info = describe_file(readme)
    assert info["size"] >= 0  # file was created; size may be > 0

    out = tmp_path / "architecture.md"
    asyncio.run(compile_architecture([info], out))
    assert out.exists()
    assert "README.md" in out.read_text()
