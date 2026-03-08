#!/usr/bin/env python3
"""CLI contract tests for consolidate_llm_context utility."""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from scripts.consolidate_llm_context import parse_args


def test_default_mode_is_dry_run() -> None:
    """Default CLI mode should be dry-run."""
    config = parse_args([])
    assert config.apply is False


def test_apply_flag_sets_apply_true() -> None:
    """--apply should enable mutating mode."""
    config = parse_args(["--apply"])
    assert config.apply is True


def test_repo_root_and_output_dir_are_honored() -> None:
    """Explicit path arguments should be preserved in config."""
    config = parse_args(
        ["--repo-root", "C:/repo", "--output-dir", "C:/out"]
    )
    assert str(config.repo_root).replace("\\", "/") == "C:/repo"
    assert str(config.output_dir).replace("\\", "/") == "C:/out"
