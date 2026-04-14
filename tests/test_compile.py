#!/usr/bin/env python
"""Tests for the architecture compilation function."""

import asyncio
import importlib
from pathlib import Path
from typing import Protocol, cast


class CompileModuleProtocol(Protocol):
    """Protocol for importer.compile module surface used by this test."""

    async def compile_architecture(self, descs: list[dict[str, str]], out: Path) -> None:
        """Compile architecture documentation from descriptors into an output file."""


def test_compile_architecture(tmp_path: Path) -> None:
    """Compile architecture docs and verify paths appear in the generated output."""
    importer_module = importlib.import_module("importer")
    compile_module = cast(CompileModuleProtocol, importer_module.compile)

    async def inner() -> None:
        descs = [{"path": "a/b"}, {"path": "c/d"}]
        out = tmp_path / "architecture.md"
        await compile_module.compile_architecture(descs, out)
        assert out.exists()
        text = out.read_text()
        assert "a/b" in text and "c/d" in text

    asyncio.run(inner())
