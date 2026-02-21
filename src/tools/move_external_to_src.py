#!/usr/bin/env python3
"""move_external_to_src - minimal parser-safe stub.

Safe placeholder used during automated repair runs. This file intentionally
performs no filesystem mutations so automated parsing and test collection can
continue.
"""
from __future__ import annotations

from pathlib import Path


def move_external_to_src_stub(root: Path) -> int:
    """No-op stub used during automated repairs."""
    return 0


if __name__ == "__main__":
    raise SystemExit(move_external_to_src_stub(Path('.')))
