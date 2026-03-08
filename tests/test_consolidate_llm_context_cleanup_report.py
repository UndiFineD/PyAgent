#!/usr/bin/env python3
"""Cleanup and reporting tests for consolidate_llm_context utility."""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from pathlib import Path

from scripts import consolidate_llm_context


def test_dry_run_keeps_sources_and_writes_report(tmp_path: Path) -> None:
    """Dry-run should not delete sources but must produce a report."""
    repo_root = tmp_path / "repo"
    (repo_root / "docs" / "architecture").mkdir(parents=True)

    source = repo_root / "docs" / "architecture" / "shape.md"
    source.write_text("shape architecture", encoding="utf-8")

    config = consolidate_llm_context.ConsolidationConfig(
        repo_root=repo_root,
        output_dir=repo_root,
        apply=False,
        migrate_docstrings=False,
    )

    consolidate_llm_context.run(config)

    assert source.exists()
    report = repo_root / "consolidation_report.txt"
    assert report.exists()
    text = report.read_text(encoding="utf-8")
    assert "merged_count" in text
    assert "deleted_count" in text


def test_apply_deletes_merged_sources(tmp_path: Path) -> None:
    """Apply mode should delete merged source markdown files only after writing outputs."""
    repo_root = tmp_path / "repo"
    (repo_root / "src" / "pkg").mkdir(parents=True)

    source = repo_root / "src" / "pkg" / "unit.improvements.md"
    source.write_text("unit improvements", encoding="utf-8")

    config = consolidate_llm_context.ConsolidationConfig(
        repo_root=repo_root,
        output_dir=repo_root,
        apply=True,
        migrate_docstrings=False,
    )

    consolidate_llm_context.run(config)

    assert not source.exists()
    report = (repo_root / "consolidation_report.txt").read_text(encoding="utf-8")
    assert "deleted_count: 1" in report
    assert "src/pkg/unit.improvements.md" in report
