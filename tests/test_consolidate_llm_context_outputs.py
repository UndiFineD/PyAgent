#!/usr/bin/env python3
"""Output scaffold tests for consolidate_llm_context utility."""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from pathlib import Path

from scripts import consolidate_llm_context


def test_generates_tiered_llms_files(tmp_path: Path) -> None:
    """Run should generate root and tiered llms files in output_dir."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    output_dir = repo_root / "out"
    output_dir.mkdir()

    config = consolidate_llm_context.ConsolidationConfig(
        repo_root=repo_root,
        output_dir=output_dir,
        apply=False,
        migrate_docstrings=False,
    )

    exit_code = consolidate_llm_context.run(config)
    assert exit_code == 0

    assert (output_dir / "llms.txt").exists()
    assert (output_dir / "llms-architecture.txt").exists()
    assert (output_dir / "llms-improvements.txt").exists()


def test_llms_root_contains_pointers(tmp_path: Path) -> None:
    """Root llms.txt should contain pointers to secondary tiered files."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    config = consolidate_llm_context.ConsolidationConfig(
        repo_root=repo_root,
        output_dir=repo_root,
        apply=False,
        migrate_docstrings=False,
    )

    consolidate_llm_context.run(config)

    text = (repo_root / "llms.txt").read_text(encoding="utf-8")
    assert "llms-architecture.txt" in text
    assert "llms-improvements.txt" in text
