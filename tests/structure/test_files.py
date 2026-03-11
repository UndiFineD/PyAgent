#!/usr/bin/env python3
"""Tests for important files in the project."""
import os
import pathlib as Path


def test_important_files_exist(tmp_path: Path) -> None:
    """Important files should exist after setup."""
    # run setup in tmp_path then check
    from scripts.setup_structure import create_core_structure
    create_core_structure(str(tmp_path))
    files = [
        "project/llms-architecture.txt",
        "project/llms-improvements.txt",
        "project/PyAgent.md",
        "project/todolist.md",
        "project/config/pyproject.toml",
        "project/config/.gitignore",
        "project/config/environment.yaml",
    ]
    for f in files:
        assert os.path.exists(os.path.join(tmp_path, f))
