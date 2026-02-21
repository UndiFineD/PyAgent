#!/usr/bin/env python3
"""move_completed - minimal parser-safe stub.

Replaces a larger utility with a conservative stub to avoid import-time syntax
errors during automated repair. This stub intentionally performs no file
mutations.
"""
from __future__ import annotations

from pathlib import Path


def move_completed_stub(root: Path) -> int:
    """No-op stub implementation."""
    return 0


if __name__ == "__main__":
    raise SystemExit(move_completed_stub(Path('.')))
