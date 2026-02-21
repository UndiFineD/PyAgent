#!/usr/bin/env python3
"""prepare_refactor_patches - minimal parser-safe stub.

Safe placeholder used during automated repair runs.
"""
from __future__ import annotations

from pathlib import Path


def prepare_refactor_patches_stub(root: Path) -> int:
    """No-op stub used during automated repairs."""
    return 0


if __name__ == "__main__":
    raise SystemExit(prepare_refactor_patches_stub(Path('.')))
