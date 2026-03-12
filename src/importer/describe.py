#!/usr/bin/env python3
"""Describe architecture components from files."""
from pathlib import Path


def describe_file(path: Path) -> dict[str, object]:
    """Describe a file by its path and size."""
    stat = path.stat()
    return {"path": str(path), "size": stat.st_size}
