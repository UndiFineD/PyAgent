#!/usr/bin/env python3
"""Tests for base directory structure."""


def test_root_project_dir_exists(tmp_path) -> None:
    """The root project directory should exist after setup."""
    # run the setup helper inside the temporary path
    from scripts.setup_structure import create_core_structure

    create_core_structure(str(tmp_path))
    root = tmp_path / "project"
    assert root.exists()
