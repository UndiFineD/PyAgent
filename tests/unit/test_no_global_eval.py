#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""Test to ensure no usage of Python builtins.eval across the codebase."""

import re
from pathlib import Path

PATTERN = re.compile(r"(?<!\.)\beval\s*\(")


def test_no_global_eval_use():
    root = Path("src")
    matches = []
    for p in root.rglob("*.py"):
        # Skip generated or vendored directories if any
        if any(x in p.parts for x in ["generated", "rust_core", "rust_lib", "external_candidates"]):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (PermissionError, OSError):
            continue
        for m in PATTERN.finditer(text):
            # Record file and surrounding line
            line_no = text.count("\n", 0, m.start()) + 1
            snippet = text.splitlines()[line_no - 1].strip()
            # Allow intentional references (e.g., analyzer rules or documented warnings)
            if "Use of eval() is highly insecure" in snippet or "# nosec" in snippet:
                continue
            
            # Allow known safe usages in core logic and exploits
            if 'src\\core\\base\\logic\\core\\exploit_crafting_core.py' in str(p):
                continue
            if 'src\\logic\\agents\\interpreter\\safe_executor.py' in str(p):
                continue
            if 'example_infer' in str(p): # Ingested code
                continue

            matches.append((str(p), line_no, snippet))

    assert not matches, f"Found unsafe eval usage in files: {matches}"
