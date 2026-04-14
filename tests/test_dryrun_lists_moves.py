#!/usr/bin/env python3
"""Test the dry run of file moves to ensure the mapping is generated correctly."""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import os
from pathlib import Path

from scripts import dryrun_move


def test_dryrun_writes_mapping(tmp_path: Path) -> None:
    """Ensure dryrun_move writes migration_dryrun.json containing the scripts pattern."""
    out_dir = tmp_path / "repo"
    out_dir.mkdir()
    prev = os.getcwd()
    try:
        os.chdir(out_dir)
        dryrun_move.main()
        out = out_dir / "migration_dryrun.json"
        assert out.exists()
        content = out.read_text(encoding="utf-8")
        assert "scripts/*.py" in content
    finally:
        os.chdir(prev)
