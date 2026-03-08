#!/usr/bin/env python3
"""Docstring migration tests for consolidate_llm_context utility."""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from pathlib import Path

from scripts import consolidate_llm_context


def test_migrate_docstrings_injects_marker_block(tmp_path: Path) -> None:
    """With --migrate-docstrings enabled, matching module should receive context block."""
    repo_root = tmp_path / "repo"
    (repo_root / "src" / "mod").mkdir(parents=True)

    module_file = repo_root / "src" / "mod" / "thing.py"
    module_file.write_text(
        "#!/usr/bin/env python3\n"
        "# Copyright 2026 PyAgent Authors\n"
        "# Licensed under the Apache License, Version 2.0 (the \"License\");\n\n"
        "def do_work() -> int:\n"
        "    return 1\n",
        encoding="utf-8",
    )

    description_file = repo_root / "src" / "mod" / "thing.description.md"
    description_file.write_text("Thing doc details", encoding="utf-8")

    config = consolidate_llm_context.ConsolidationConfig(
        repo_root=repo_root,
        output_dir=repo_root,
        apply=False,
        migrate_docstrings=True,
    )

    consolidate_llm_context.run(config)
    updated = module_file.read_text(encoding="utf-8")

    assert "LLM_CONTEXT_START" in updated
    assert "Thing doc details" in updated
    assert updated.startswith("#!/usr/bin/env python3\n# Copyright 2026 PyAgent Authors\n")


def test_migrate_docstrings_is_idempotent(tmp_path: Path) -> None:
    """Running migration twice should not duplicate marker blocks."""
    repo_root = tmp_path / "repo"
    (repo_root / "src").mkdir(parents=True)

    module_file = repo_root / "src" / "demo.py"
    module_file.write_text("def demo() -> str:\n    return 'ok'\n", encoding="utf-8")

    md_file = repo_root / "src" / "demo.improvements.md"
    md_file.write_text("Demo improvement", encoding="utf-8")

    config = consolidate_llm_context.ConsolidationConfig(
        repo_root=repo_root,
        output_dir=repo_root,
        apply=False,
        migrate_docstrings=True,
    )

    consolidate_llm_context.run(config)
    consolidate_llm_context.run(config)

    updated = module_file.read_text(encoding="utf-8")
    assert updated.count("LLM_CONTEXT_START") == 1
    assert updated.count("LLM_CONTEXT_END") == 1
