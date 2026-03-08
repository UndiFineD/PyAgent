#!/usr/bin/env python3
"""End-to-end integration tests for consolidate_llm_context utility."""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from pathlib import Path

from scripts import consolidate_llm_context


def test_integration_dry_run_then_apply(tmp_path: Path) -> None:
    """Dry-run should preserve sources; apply should clean merged sources and keep outputs."""
    repo_root = tmp_path / "repo"
    (repo_root / "docs" / "architecture").mkdir(parents=True)
    (repo_root / "src" / "mod").mkdir(parents=True)

    arch_file = repo_root / "docs" / "architecture" / "layout.md"
    arch_file.write_text("layout architecture", encoding="utf-8")

    md_file = repo_root / "src" / "mod" / "tool.improvements.md"
    md_file.write_text("tool improvements", encoding="utf-8")

    module_file = repo_root / "src" / "mod" / "tool.py"
    module_file.write_text("def run() -> int:\n    return 7\n", encoding="utf-8")

    dry_config = consolidate_llm_context.ConsolidationConfig(
        repo_root=repo_root,
        output_dir=repo_root,
        apply=False,
        migrate_docstrings=True,
    )
    consolidate_llm_context.run(dry_config)

    assert arch_file.exists()
    assert md_file.exists()
    assert (repo_root / "llms.txt").exists()
    assert (repo_root / "llms-architecture.txt").exists()
    assert (repo_root / "llms-improvements.txt").exists()

    module_text = module_file.read_text(encoding="utf-8")
    assert "LLM_CONTEXT_START" in module_text

    apply_config = consolidate_llm_context.ConsolidationConfig(
        repo_root=repo_root,
        output_dir=repo_root,
        apply=True,
        migrate_docstrings=True,
    )
    consolidate_llm_context.run(apply_config)

    assert not arch_file.exists()
    assert not md_file.exists()
    assert (repo_root / "consolidation_report.txt").exists()
