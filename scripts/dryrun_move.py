#!/usr/bin/env python3
"""Dry run script to simulate moving files to a new directory structure."""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import json
from pathlib import Path

MAPPINGS = {
    "old_scripts": ["scripts/*.py"],
}


def dryrun(root: Path = Path(".")) -> dict[str, list[str]]:
    """Simulate the file moves based on MAPPINGS and return a mapping of old patterns to new locations."""
    # Very small example: list top-level scripts and map to target folders
    result: dict[str, list[str]] = {}
    for pattern in ["scripts/*.py"]:
        files = [str(p.relative_to(root)) for p in root.glob(pattern)]
        result[pattern] = files
    return result


def main() -> None:
    """Main function to perform the dry run and output results."""
    root = Path(".")
    mapping = dryrun(root)
    out = Path("migration_dryrun.json")
    out.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
