#!/usr/bin/env python3
"""Compile architecture descriptors into a single file."""
from pathlib import Path
from typing import List, Dict


def compile_architecture(descriptors: List[Dict], out_path: Path) -> None:
    """Compile architecture descriptors into a single file."""
    out_path = Path(out_path)
    with open(out_path, "w", encoding="utf-8") as f:
        for d in descriptors:
            f.write(f"{d.get('path')}\n")
