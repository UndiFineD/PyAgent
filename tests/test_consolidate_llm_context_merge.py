#!/usr/bin/env python3
"""Merge behavior tests for consolidate_llm_context utility."""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from pathlib import Path

from scripts import consolidate_llm_context


def test_merges_architecture_and_improvement_sources(tmp_path: Path) -> None:
    """Architecture and improvement files should be merged into their respective tiers."""
    repo_root = tmp_path / "repo"
    (repo_root / "docs" / "architecture").mkdir(parents=True)
    (repo_root / "src" / "mod").mkdir(parents=True)

    arch_file = repo_root / "docs" / "architecture" / "core.md"
    arch_file.write_text("Core architecture decisions", encoding="utf-8")

    desc_file = repo_root / "src" / "mod" / "thing.description.md"
    desc_file.write_text("Thing description details", encoding="utf-8")

    imp_file = repo_root / "src" / "mod" / "thing.improvements.md"
    imp_file.write_text("Thing improvement notes", encoding="utf-8")

    config = consolidate_llm_context.ConsolidationConfig(
        repo_root=repo_root,
        output_dir=repo_root,
        apply=False,
        migrate_docstrings=False,
    )

    consolidate_llm_context.run(config)

    architecture_text = (repo_root / "llms-architecture.txt").read_text(encoding="utf-8")
    improvements_text = (repo_root / "llms-improvements.txt").read_text(encoding="utf-8")

    assert "Core architecture decisions" in architecture_text
    assert "docs/architecture/core.md" in architecture_text

    assert "Thing description details" in improvements_text
    assert "Thing improvement notes" in improvements_text
    assert "src/mod/thing.description.md" in improvements_text
    assert "src/mod/thing.improvements.md" in improvements_text
