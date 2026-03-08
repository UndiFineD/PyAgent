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
    """Root llms.txt should contain pointers and some repo context."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    # create a README and a small architecture file so we can assert they
    # appear in the root file
    (repo_root / "README.md").write_text("Hello PyAgent", encoding="utf-8")
    arch_dir = repo_root / "docs" / "architecture"
    arch_dir.mkdir(parents=True)
    (arch_dir / "foo.md").write_text("Arch details", encoding="utf-8")

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
    assert "Hello PyAgent" in text
    assert "Arch details" in text
    # should not exceed the 32k byte limit
    assert len(text.encode("utf-8")) <= 32000


def test_llms_root_truncates_large_body(tmp_path: Path) -> None:
    """Very large README should be trimmed but pointers preserved."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    # create an oversized README
    big = "A" * 50000
    (repo_root / "README.md").write_text(big, encoding="utf-8")

    config = consolidate_llm_context.ConsolidationConfig(
        repo_root=repo_root,
        output_dir=repo_root,
        apply=False,
        migrate_docstrings=False,
    )
    consolidate_llm_context.run(config)
    text = (repo_root / "llms.txt").read_text(encoding="utf-8")
    assert text.endswith("llms-improvements.txt\n")
    assert len(text.encode("utf-8")) <= 32000
