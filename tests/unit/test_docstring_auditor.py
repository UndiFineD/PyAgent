#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

"""Tests for the docstring auditor utilities."""

from pathlib import Path
from src.maintenance.docstring_auditor import parse_prompt_file, generate_next_batch


def test_parse_prompt_file_non_empty():
    prompt = Path("docs/prompt/prompt4.txt")
    files = parse_prompt_file(prompt)
    assert isinstance(files, list)
    assert len(files) > 0


def test_generate_next_batch_writes_file(tmp_path):
    prompt = Path("docs/prompt/prompt4.txt")
    out = tmp_path / "next_batch.txt"
    modules = generate_next_batch(prompt, out, max_entries=5)
    assert out.exists()
    assert len(modules) <= 5
    # Each entry should look like a module path
    assert all("." in m for m in modules)
